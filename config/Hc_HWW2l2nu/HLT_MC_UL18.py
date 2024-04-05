from Hpluscharm.workflows import workflows as hplusc_wf
import numpy as np

cfg = {
    "dataset": {
        "jsons": [
          "src/Hpluscharm/input_json/UL18_MC.json"    
        ],
        "campaign": "2018_UL",
        "year": "2018",
        "filter":
        {"samples_exclude":['GluGluHToWWTo2L2Nu_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8', 'GluGluZH_HToWWTo2L2Nu_M-125_TuneCP5_13TeV-powheg-pythia8', 'VBFHToWWTo2L2Nu_M125_TuneCP5_13TeV_powheg2_JHUGenV714_pythia8', 'HWplusJ_HToWWTo2L2Nu_WTo2L_M-125_TuneCP5_13TeV-powheg-pythia8', 'HWminusJ_HToWW_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8', 'HZJ_HToWWTo2L2Nu_ZTo2L_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8', 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8', 'GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8', 'VBF_HToZZTo4L_M125_TuneCP5_withDipoleRecoil_13TeV-powheg2-jhugenv7011-pythia8']}
    },
    # Input and output files
    "workflow": hplusc_wf["HLT"],
    "output": "MC_HLT_UL18",
    "run_options": {
        "executor": "parsl/condor/naf_lite",
        # "executor":"iterative",
        "workers": 2,
        "scaleout": 500,
        "walltime": "03:00:00",
        "mem_per_worker": 2,  # GB
        "chunk":100000,
        "skipbadfiles": False,
        "retries": 80,
        "index": "0,0",
        "sample_size": 100,
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
                "lumiMask": "Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                "PU": None,
                "roccor": None,
                "JME": "jec_compiled.pkl.gz",
                "BTV": {"deepJet": "shape"},
                "JMAR": {"PUJetID_eff": "L"},
                "LSF": {
                "ele_ID 2018": "wp90iso",
                    "ele_Reco 2018": "RecoAbove20",
                    "ele_Reco_low 2018": "RecoBelow20",
                    "mu_Reco 2018_UL": "NUM_TrackerMuons_DEN_genTracks",
                    "mu_ID 2018_UL": "NUM_TightID_DEN_TrackerMuons",
                    "mu_Iso 2018_UL": "NUM_TightRelIso_DEN_TightIDandIPCut",
                    "mu_ID_low NUM_TightID_DEN_TrackerMuons": "Efficiency_muon_trackerMuon_Run2018_UL_ID.histo.json",
                    "mu_Reco_low NUM_TrackerMuons_DEN_genTracks": "Efficiency_muon_generalTracks_Run2018_UL_trackerMuon.histo.json",
                },
            },
        },
    },
    "systematic": {
        "JERC": False,
        "weights": False,
        "roccor": False,
    },
}
