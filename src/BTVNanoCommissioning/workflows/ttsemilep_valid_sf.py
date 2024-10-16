import collections, gc
import os
import uproot
import numpy as np, awkward as ak

from coffea import processor
from coffea.analysis_tools import Weights

from BTVNanoCommissioning.utils.correction import (
    load_lumi,
    load_SF,
    weight_manager,
    common_shifts,
)

from BTVNanoCommissioning.helpers.func import update, dump_lumi, PFCand_link
from BTVNanoCommissioning.helpers.update_branch import missing_branch
from BTVNanoCommissioning.utils.histogrammer import histogrammer, histo_writter
from BTVNanoCommissioning.utils.array_writer import array_writer
from BTVNanoCommissioning.utils.selection import (
    HLT_helper,
    jet_id,
    btag_mu_idiso,
    MET_filters,
)


class NanoProcessor(processor.ProcessorABC):
    # Define histograms
    def __init__(
        self,
        year="2022",
        campaign="Summer22Run3",
        name="",
        isSyst=False,
        isArray=False,
        noHist=False,
        chunksize=75000,
    ):
        self._year = year
        self._campaign = campaign
        self.name = name
        self.isSyst = isSyst
        self.isArray = isArray
        self.noHist = noHist
        self.lumiMask = load_lumi(self._campaign)
        self.chunksize = chunksize
        ## Load corrections
        self.SF_map = load_SF(self._year, self._campaign)

    @property
    def accumulator(self):
        return self._accumulator

    def process(self, events):
        events = missing_branch(events)
        shifts = common_shifts(self, events)

        return processor.accumulate(
            self.process_shift(update(events, collections), name)
            for collections, name in shifts
        )

    def process_shift(self, events, shift_name):
        dataset = events.metadata["dataset"]
        isRealData = not hasattr(events, "genWeight")
        _hist_event_dict = (
            {"": None} if self.noHist else histogrammer(events, "ttsemilep_sf")
        )

        output = {
            "sumw": processor.defaultdict_accumulator(float),
            **_hist_event_dict,
        }

        if shift_name is None:
            if isRealData:
                output["sumw"] = len(events)
            else:
                output["sumw"] = ak.sum(events.genWeight)
        ####################
        #    Selections    #
        ####################
        ## Lumimask
        req_lumi = np.ones(len(events), dtype="bool")
        if isRealData:
            req_lumi = self.lumiMask(events.run, events.luminosityBlock)
        # only dump for nominal case
        if shift_name is None:
            output = dump_lumi(events[req_lumi], output)

        ## HLT
        triggers = ["IsoMu24"]
        req_trig = HLT_helper(events, triggers)

        ## Muon cuts
        # muon twiki: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2
        event_muon = events.Muon[
            (events.Muon.pt > 30) & btag_mu_idiso(events, self._campaign)
        ]
        # event_muon = ak.pad_none(events.Muon, 1, axis=1)
        req_muon = ak.count(event_muon.pt, axis=1) == 1

        ## Jet cuts
        event_jet = events.Jet[
            ak.fill_none(
                jet_id(events, self._campaign)
                & (
                    ak.all(
                        events.Jet.metric_table(events.Muon) > 0.4,
                        axis=2,
                        mask_identity=True,
                    )
                ),
                False,
                axis=-1,
            )
        ]
        req_jets = ak.num(event_jet.pt) >= 4

        ## store jet index for PFCands, create mask on the jet index
        jetindx = ak.mask(
            ak.local_index(events.Jet.pt),
            (
                jet_id(events, self._campaign)
                & (
                    ak.all(
                        events.Jet.metric_table(events.Muon) > 0.4,
                        axis=2,
                        mask_identity=True,
                    )
                )
            )
            == 1,
        )
        jetindx = ak.pad_none(jetindx, 4)
        jetindx = jetindx[:, :4]

        ## other cuts

        MET = ak.zip(
            {
                "pt": events.MET.pt,
                "eta": ak.zeros_like(events.MET.pt),
                "phi": events.MET.phi,
                "mass": ak.zeros_like(events.MET.pt),
            },
            with_name="PtEtaPhiMLorentzVector",
        )

        req_MET = MET.pt > 50

        req_metfilter = MET_filters(events, self._campaign)
        event_level = ak.fill_none(
            req_trig & req_jets & req_muon & req_MET & req_lumi & req_metfilter, False
        )
        if len(events[event_level]) == 0:
            if self.isArray:
                array_writer(
                    self,
                    events[event_level],
                    events,
                    "nominal",
                    dataset,
                    isRealData,
                    empty=True,
                )
            return {dataset: output}
        ####################
        # Selected objects #
        ####################

        # Find the PFCands associate with selected jets. Search from jetindex->JetPFCands->PFCand
        if "PFCands" in events.fields:
            jetindexall = collections.defaultdict(dict)
            spfcands = collections.defaultdict(dict)
            for i in range(4):
                jetindexall[i] = jetindx[:, i]
                spfcands[i] = events[event_level].PFCands[
                    events[event_level]
                    .JetPFCands[
                        events[event_level].JetPFCands.jetIdx
                        == jetindexall[i][event_level]
                    ]
                    .pFCandsIdx
                ]

        # Keep the structure of events and pruned the object size
        pruned_ev = events[event_level]
        pruned_ev["SelJet"] = event_jet[event_level][:, :4]
        pruned_ev["SelMuon"] = event_muon[event_level][:, 0]
        pruned_ev["njet"] = ak.count(event_jet[event_level].pt, axis=1)
        if "PFCands" in events.fields:
            pruned_ev.PFCands = spfcands

        for i in range(4):
            pruned_ev[f"dr_mujet{i}"] = pruned_ev.Muon.delta_r(pruned_ev.Jet[:, i])
        ####################
        #     Output       #
        ####################
        # Configure SFs
        weights = weight_manager(pruned_ev, self.SF_map, self.isSyst)
        # Configure systematics
        if shift_name is None:
            systematics = ["nominal"] + list(weights.variations)
        else:
            systematics = [shift_name]
        if not isRealData:
            pruned_ev["weight"] = weights.weight()
            for ind_wei in weights.weightStatistics.keys():
                pruned_ev[f"{ind_wei}_weight"] = weights.partial_weight(
                    include=[ind_wei]
                )
        # Configure histograms
        if not self.noHist:
            output = histo_writter(
                pruned_ev, output, weights, systematics, self.isSyst, self.SF_map
            )
        # Output arrays
        if self.isArray:
            array_writer(self, pruned_ev, events, systematics[0], dataset, isRealData)
        return {dataset: output}

    def postprocess(self, accumulator):
        return accumulator
