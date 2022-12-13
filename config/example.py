# Local Variables:
# python-indent-offset: 4
# End:

from test_wf import NanoProcessor as test_wf

cfg = {
    "dataset": {
        "jsons": ["metadata/test.json"],
        "campaign": "UL17",
        "year": "2017",
        "filter": {
            "samples": [
                "GluGluHToWWTo2L2Nu_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8",
                "SingleMuon_Run2017B-UL2017_MiniAODv2_NanoAODv9-v1",
            ],
            "samples_exclude": ["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8"],
        },
    },
    # Input and output files
    "workflow": test_wf,
    "output": "output_test",
    "run_options": {
        # "executor": "parsl/condor",
        "executor": "futures",
        "workers": 10,
        "scaleout": 40,
        "walltime": "03:00:00",
        "mem_per_worker": 2,  # GB
        "chunk": 500000,
        "max": None,
        "skipbadfiles": None,
        "voms": None,
        "limit": 2,
        "retries": 20,
        "splitjobs": False,
    },
    ## weights
    "weights": {
        "common": {
            "inclusive": {
                "lumiMask": "Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
            }
        }
    },
}