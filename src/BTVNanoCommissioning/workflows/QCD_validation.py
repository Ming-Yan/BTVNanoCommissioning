import collections, numpy as np, awkward as ak
from coffea import processor
from coffea.analysis_tools import Weights
from BTVNanoCommissioning.helpers.func import flatten, update, dump_lumi
from BTVNanoCommissioning.utils.histogrammer import histogrammer, histo_writter
from BTVNanoCommissioning.utils.array_writer import array_writer
from BTVNanoCommissioning.helpers.update_branch import missing_branch
from BTVNanoCommissioning.utils.correction import (
    load_lumi,
    load_SF,
    weight_manager,
    common_shifts,
)
from BTVNanoCommissioning.utils.selection import jet_cut, HLT_helper

import correctionlib


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
        isRealData = not hasattr(events, "genWeight")
        dataset = events.metadata["dataset"]
        _hist_event_dict = {"": None} if self.noHist else histogrammer(events, "QCD")
        if _hist_event_dict == None:
            _hist_event_dict[""]
        output = {
            "sumw": processor.defaultdict_accumulator(float),
            **_hist_event_dict,
        }

        if isRealData:
            output["sumw"] = len(events)
        else:
            output["sumw"] = ak.sum(events.genWeight)

        ####################
        #    Selections    #
        ####################
        ## HLT
        triggers = [
            "PFJet140",
        ]
        req_trig = HLT_helper(events, triggers)
        req_lumi = np.ones(len(events), dtype="bool")
        if isRealData:
            req_lumi = self.lumiMask(events.run, events.luminosityBlock)
        if shift_name is None:
            output = dump_lumi(events[req_lumi], output)
        ## Jet cuts
        event_jet = events.Jet[jet_cut(events, self._campaign)]
        req_jets = ak.count(event_jet.pt, axis=1) >= 1

        event_level = ak.fill_none(req_lumi & req_trig & req_jets, False)
        if len(events[event_level]) == 0:
            return {dataset: output}

        ####################
        # Selected objects #
        ####################
        pruned_ev = events[event_level]
        pruned_ev["SelJet"] = event_jet[event_level][:, 0]
        pruned_ev["njet"] = ak.count(event_jet[event_level].pt, axis=-1)
        ###############
        # Selected SV #
        ###############
        if "JetSVs" in events.Jet.fields:
            matched_JetSVs = pruned_ev.Jet[pruned_ev.JetSVs.jetIdx]
            lj_matched_JetSVs = matched_JetSVs[pruned_ev.JetSVs.jetIdx == 0]
            lj_SVs = pruned_ev.JetSVs[pruned_ev.JetSVs.jetIdx == 0]
            nJetSVs = ak.count(lj_SVs.pt, axis=1)

        ####################
        #     Output       #
        ####################
        # Configure SFs
        weights = weight_manager(pruned_ev, self.SF_map, self.isSyst)
        if isRealData:
            if self._year == "2022":
                run_num = "355374_362760"
            elif self._year == "2023":
                run_num = "366727_370790"
            pseval = correctionlib.CorrectionSet.from_file(
                f"src/BTVNanoCommissioning/data/Prescales/ps_weight_{triggers[0]}_run{run_num}.json"
            )
            # if 369869 in pruned_ev.run: continue
            psweight = pseval["prescaleWeight"].evaluate(
                pruned_ev.run,
                f"HLT_{triggers[0]}",
                ak.values_astype(pruned_ev.luminosityBlock, np.float32),
            )
            weights.add("psweight", psweight)
            if "JetSVs" in events.Jet.fields:
                lj_matched_JetSVs_genflav = ak.zeros_like(
                    lj_matched_JetSVs.pt, dtype=int
                )
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
