# For user : Running the workflows

![structure](figs/comm_wf.png)


All the steps are summarized in the [`suball.py`](#all-in-one-script--scriptssuballpy) scripts for the existing workflows. You can simply just run

```python
python scripts/suball.py --scheme ${SCHEME_FOR_STUDY} --campaign ${CAMPAIGN_FOR_SF} --year ${YEAR}  --DAS_campaign "$DATA_CAMPAIGN_RGX,$MC_CAMPAIGN_RGX"
#Example with 2023 Summer23 campaign
python scripts/suball.py --scheme default_comissioning --campaign Summer23 --year 2023  --DAS_campaign "*Run2023D*Sep2023*,*Run3Summer23BPixNanoAODv12-130X*" 
```

Each steps are also explained in detailed below, this can be obtain by 


1. Is the `.json` file ready? If not, create it following the instructions in the [Make the json files](#make-the-dataset-json-files) section. Please use the correct naming scheme
2. Add the `lumiMask`, correction files (SFs, pileup weight), and JER, JEC files under the dict entry in `utils/AK4_parameters.py`. See details in [Correction files configurations](#correction-files-configurations). When adding new files in `data/` subfolders, please create `__init__.py` for modules to find the path
3. If selections and output histogram/arrays need to be changed, modify the dedicated `workflows`
4. Run the workflow with dedicated input and campaign name. You can also specify `--isArray` to store the skimmed root files.
5. Fetch the failed files to obtain events that have been processed and events that have to be resubmitted using `scripts/dump_processed.py`. Check the luminosity of the processed dataset used for the plotting script and re-run failed jobs if needed (details in [get procssed info](#get-processed-information))
6. Once you obtain the `.coffea` file(s), you can make plots using the [plotting scripts](#plotting-code) under `scripts/`, if the xsection for your sample is missing, please add it to `src/BTVNanoCommissioning/helpers/xsection.py`


## All in one script : `scripts/suball.py`

The scripts put the steps to run the workflow in one place except 


## 0.  Make the dataset json files 

Use `fetch.py` in folder `scripts/` to obtain your samples json files. 
`$input_DAS_list` is the name of your samples in CMS DAS, and `$output_json_name$` is the name of your output samples json file. `${campaign}` is the campaign name for the 

```
python fetch.py --input ${input_DAS_list} --output ${output_json_name} --campaign ${campaign}
```


The `fetch.py`  scripts follow the naming scheme as following:

In case you want to make the `json` file yourself, please follow the rules:

For the data sample

```
$dataset_$Run
#i.e.
SingleMuon_Run2022C-PromptReco-v1
```
For MC, please be consistent with the dataset name in CMS DAS, as it cannot be mapped to the cross section otherwise.
```
$dataset
#i.e.
WW_TuneCP5_13p6TeV-pythia8
```

:::{caution}
Do not make the file list greater than 4k files to avoid scaleout issues in various site (file open limit)
:::

## Correction files configurations 

If the correction files are not supported yet by jsonpog-integration, you can still try with custom input data.

### Options with custom input data

All the `lumiMask`, correction files (SFs, pileup weight), and JEC, JER files are under  `BTVNanoCommissioning/src/data/` following the substructure `${type}/${campaign}/${files}`(except `lumiMasks` and `Prescales`)

| Type        | File type |  Comments|
| :---:   | :---: | :---: |
| `lumiMasks` |`.json` | Masked good lumi-section used for physics analysis|
| `Prescales` | `.json.` | HLT paths for prescaled triggers|
| `PU`  | `.pkl.gz` or `.histo.root` | Pileup reweight files, matched MC to data| 
| `LSF` | `.histo.root` | Lepton ID/Iso/Reco/Trigger SFs|
| `BTV` | `.csv` or `.root` | b-tagger, c-tagger SFs|
| `JME` | `.txt` | JER, JEC files|
| `JPCalib` | `.root` | Jet probablity calibration, used in LTSV methods|

Create a `dict` entry under `correction_config` with dedicated campaigns in `BTVNanoCommissioning/src/utils/AK4_parameters.py`.


  
  
The official correction files collected in [jsonpog-integration](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration) is updated by POG, except `lumiMask` and `JME` still updated by by the BTVNanoCommissioning framework user/developer.  For centrally maintained correction files, no input files have to be defined anymore in the `correction_config`. The example to implemented new corrections from POG can be found in [git](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/blob/master/examples/), and the contents of the correction files are in the [summary](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/)


  ```python
    "2017_UL": {
          # Same with custom config
          "lumiMask": "Cert_294927-306462_13TeV_UL2017_Collisions17_MuonJSON.json",

          "JME": {
             "MC": "Summer19UL17_V5_MC",
            "Run2017F": "Summer19UL17_RunF_V5_DATA",
          },
          ### Alternatively, take the txt files in  https://github.com/cms-jet/JECDatabase/tree/master/textFiles
          "JME": {
                      # specified the name of JEC
                      "name": "V1_AK4PFPuppi",
                      # dictionary of jec text files
                      "MC": [
                          "Summer23Prompt23_V1_MC_L1FastJet_AK4PFPuppi",
                          "Summer23Prompt23_V1_MC_L2Relative_AK4PFPuppi",
                          "Summer23Prompt23_V1_MC_L2Residual_AK4PFPuppi",
                          "Summer23Prompt23_V1_MC_L3Absolute_AK4PFPuppi",
                          "Summer23Prompt23_V1_MC_UncertaintySources_AK4PFPuppi",
                          "Summer23Prompt23_V1_MC_Uncertainty_AK4PFPuppi",
                          "Summer23Prompt23_JRV1_MC_SF_AK4PFPuppi",
                          "Summer23Prompt23_JRV1_MC_PtResolution_AK4PFPuppi",
                      ],
                      "dataCv123": [
                          "Summer23Prompt23_RunCv123_V1_DATA_L1FastJet_AK4PFPuppi",
                          "Summer23Prompt23_RunCv123_V1_DATA_L2Relative_AK4PFPuppi",
                          "Summer23Prompt23_RunCv123_V1_DATA_L3Absolute_AK4PFPuppi",
                          "Summer23Prompt23_RunCv123_V1_DATA_L2L3Residual_AK4PFPuppi",
                      ],
                      "dataCv4": [
                          "Summer23Prompt23_RunCv4_V1_DATA_L1FastJet_AK4PFPuppi",
                          "Summer23Prompt23_RunCv4_V1_DATA_L2Relative_AK4PFPuppi",
                          "Summer23Prompt23_RunCv4_V1_DATA_L3Absolute_AK4PFPuppi",
                          "Summer23Prompt23_RunCv4_V1_DATA_L2L3Residual_AK4PFPuppi",
                      ],
                  },
          ###
          # no config need to be specify for PU weights
          "PU": None,
          # Alternatively, take root file as input
          "PU": "puwei_Summer23.histo.root",
          # Btag SFs - specify $TAGGER : $TYPE-> find [$TAGGER_$TYPE] in json file
          "BTV": {"deepCSV": "shape", "deepJet": "shape"},
          "roccor": None,
          # JMAR, IDs from JME- Following the scheme: "${SF_name}": "${WP}"
          "JMAR": {"PUJetID_eff": "L"},
          "LSF": {
          # Electron SF - Following the scheme: "${SF_name} ${year}": "${WP}"
          # https://github.com/cms-egamma/cms-egamma-docs/blob/master/docs/EgammaSFJSON.md
              "ele_ID 2017": "wp90iso",
              "ele_Reco 2017": "RecoAbove20",

          # Muon SF - Following the scheme: "${SF_name} ${year}": "${WP}"

              "mu_Reco 2017_UL": "NUM_TrackerMuons_DEN_genTracks",
              "mu_HLT 2017_UL": "NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoTight",
              "mu_ID 2017_UL": "NUM_TightID_DEN_TrackerMuons",
              "mu_Iso 2017_UL": "NUM_TightRelIso_DEN_TightIDandIPCut",
          },
          # use for BTA production, jet probablity
        "JPCalib": {
            "Run2022E": "calibeHistoWrite_Data2022F_NANO130X_v1.root",
            "Run2022F": "calibeHistoWrite_Data2022F_NANO130X_v1.root",
            "Run2022G": "calibeHistoWrite_Data2022G_NANO130X_v1.root",
            "MC": "calibeHistoWrite_MC2022EE_NANO130X_v1.root",
        },
      },
  ```


## Reading coffea `hist` &  convert to ROOT TH1 