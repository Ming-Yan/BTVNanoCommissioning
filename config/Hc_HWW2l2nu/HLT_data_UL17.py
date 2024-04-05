from Hpluscharm.workflows import workflows as hplusc_wf
import numpy as np

cfg = {
    "dataset": {
        "jsons": [
            "MET_2017.json",
            "src/Hpluscharm/input_json/UL17_data.json"
        ],
        "campaign": "2017_UL",
        "year": "2017",
        
    },
    # Input and output files
    "workflow": hplusc_wf["HLT"],
    "output": "data_HLT_UL17",
    "run_options": {
        "executor": "parsl/condor/naf_lite",
        # "executor":"iterative",
        "workers": 2,
        "scaleout": 400,
        "walltime": "03:00:00",
        "mem_per_worker": 2,  # GB
        "chunk":100000,
        "skipbadfiles": True,
        "retries": 60,
        "index": "0,0",
         "sample_size": 150,
        #     "voms": None,
        # "splitjobs": False,
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
            "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
            "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
        ],
        "METhlt":[
            "PFMET200_HBHECleaned",
            "PFMET200_HBHE_BeamHaloCleaned",
            "PFMETTypeOne200_HBHE_BeamHaloCleaned",
            "PFMET120_PFMHT120_IDTight",
            "PFMETNoMu_120_PFMHTNoMu_120_IDTight",
            "PFMET120_PFMHT120_IDTight_PFHT60",
            "PFMETNoMu_120_PFMHTNoMu_120_IDTight_PFHT60", 
            "PFHT500_PFMET100_PFMHT100_IDTight",
            "PFHT700_PFMET85_PFMHT85_IDTight",
            "PFHT800_PFMET75_PFMHT75_IDTight",
        ]
    },
    ## weights
    "weights": {
        "common": {
            "inclusive": {
                "lumiMask": "Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                "PU": None,
                "roccor": None,
                "JME": "jec_compiled.pkl.gz",
                
            },
        },
    },
    "systematic": {
        "JERC": False,
        "weights": False,
        "roccor": False,
    },
}
