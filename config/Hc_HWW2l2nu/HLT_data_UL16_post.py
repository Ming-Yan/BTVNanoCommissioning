from Hpluscharm.workflows import workflows as hplusc_wf
import numpy as np

cfg = {
    "dataset": {
        "jsons": [
            "MET_2016_post.json",
            "src/Hpluscharm/input_json/UL16_postVFP_data.json",
        ],
        "campaign": "2016postVFP_UL",
        "year": "2016",
    },
    # Input and output files
    "workflow": hplusc_wf["HLT"],
    "output": "data_HLT_postVFP_UL16",
    "run_options": {
        "executor": "parsl/condor/naf_lite",
        #"executor": "futures",
        # "executor":"iterative",
        "workers": 2,
        "scaleout": 200,
        "walltime": "03:00:00",
        "mem_per_worker": 2,  # GB
        "chunk": 100000,
        "retries":  80,
        # "limit":1,
        "index": "0,0",
        "sample_size": 150,
        #     "voms": None,
        "splitjobs": False,
    },
    ## selections
    "categories": {"cats": [], "cats2": []},
    "preselections": {
        "mu1hlt": ["IsoMu27"],
        "mu2hlt": [
            "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
            "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
        ],
        "e1hlt": ["Ele35_WPTight_Gsf"],
        "e2hlt": ["Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"],
        "emuhlt": [
            "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
            "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
            "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
            "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
            "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
        ],
        "METhlt":[
            "PFMET300",
            "MET200",
            "PFHT300_PFMET110",
            "PFMET170_HBHECleaned",
            "PFMET120_PFMHT120_IDTight",
            "PFMETNoMu_120_PFMHTNoMu_120_IDTight" 
        ]
    },
    ## weights
    "weights": {
        "common": {
            "inclusive": {
                "lumiMask": "Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                "PU": None,
                "roccor": None,
                "JME": "jec_compiled.pkl.gz",
                "BTV": {"deepJet": "shape"},
                "LSF": {
                    "ele_ID 2016postVFP": "wp90iso",
                    "ele_Reco 2016postVFP": "RecoAbove20",
                    "ele_Reco_low 2016postVFP": "RecoBelow20",
                    "mu_Reco 2016postVFP_UL": "NUM_TrackerMuons_DEN_genTracks",
                    "mu_ID 2016postVFP_UL": "NUM_TightID_DEN_TrackerMuons",
                    "mu_Iso 2016postVFP_UL": "NUM_TightRelIso_DEN_TightIDandIPCut",
                    "mu_ID_low NUM_TightID_DEN_TrackerMuons": "Efficiency_muon_trackerMuon_Run2016postVFP_UL_ID.histo.json",
                    "mu_Reco_low NUM_TrackerMuons_DEN_genTracks": "Efficiency_muon_generalTracks_Run2016postVFP_UL_trackerMuon.histo.json",
                },
            },
        },
    },
    "systematic": {"JERC": False, "weights": False, "roccor": False},
}
