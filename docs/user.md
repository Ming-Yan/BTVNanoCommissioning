## Preparation for commissioning/SFs tasks

1. Is the `.json` file ready? If not, create it following the instructions in the [Make the json files](#make-the-dataset-json-files) section. Please use the correct naming scheme
2. Add the `lumiMask`, correction files (SFs, pileup weight), and JER, JEC files under the dict entry in `utils/AK4_parameters.py`. See details in [Correction files configurations](#correction-files-configurations). When adding new files in `data/` subfolders, please create `__init__.py` for modules to find the path
3. If the JERC file `jec_compiled.pkl.gz` is missing in the `data/JME/${campaign}` directory, create it through [Create compiled JERC file](#create-compiled-jerc-filepklgz)
4. If selections and output histogram/arrays need to be changed, modify the dedicated `workflows`
5. Run the workflow with dedicated input and campaign name. For first usage, the JERC file needs to be recompiled first, see [Create compiled JERC file](#create-compiled-jerc-filepklgz). You can also specify `--isArray` to store the skimmed root files.
6. Fetch the failed files to obtain events that have been processed and events that have to be resubmitted using `scripts/dump_processed.py`. Check the luminosity of the processed dataset used for the plotting script and re-run failed jobs if needed (details in [get procssed info](#get-processed-information))
7. Once you obtain the `.coffea` file(s), you can make plots using the [plotting scripts](#plotting-code) under `scripts/`, if the xsection for your sample is missing, please add it to `src/BTVNanoCommissioning/helpers/xsection.py`

### Make the dataset json files

Use `fetch.py` in folder `scripts/` to obtain your samples json files. `$input_DAS_list` is the name of your samples in CMS DAS, and `$output_json_name$` is the name of your output samples json file.

```
python fetch.py --input ${input_DAS_list} --output ${output_json_name} --site ${site}
```
The `output_json_name` must contain the BTV name tag (e.g. `BTV_Run3_2022_Comm_v1`).

You might need to rename the json key name with following name scheme:

<details><summary> details </summary>
<p>
For the data sample please use the naming scheme,

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

>  [!Caution]
> Do not make the file list greater than 4k files to avoid scaleout issues in various site



### Correction files configurations

If the correction files are not supported yet by jsonpog-integration, you can still try with custom input data.

#### Options with custom input data

All the `lumiMask`, correction files (SFs, pileup weight), and JEC, JER files are under  `BTVNanoCommissioning/src/data/` following the substructure `${type}/${campaign}/${files}`(except `lumiMasks` and `Prescales`)

| Type        | File type |  Comments|
| :---:   | :---: | :---: |
| `lumiMasks` |`.json` | Masked good lumi-section used for physics analysis|
| `Prescales` | `.txt` | HLT paths for prescaled triggers|
| `PU`  | `.pkl.gz` or `.histo.root` | Pileup reweight files, matched MC to data| 
| `LSF` | `.histo.root` | Lepton ID/Iso/Reco/Trigger SFs|
| `BTV` | `.csv` or `.root` | b-tagger, c-tagger SFs|
| `JME` | `.txt` | JER, JEC files|

Create a `dict` entry under `correction_config` with dedicated campaigns in `BTVNanoCommissioning/src/utils/AK4_parameters.py`.


  ```python
  # specify campaign
  "Rereco17_94X": 
  {
        ##Load files with dedicated type:filename
          "lumiMask": "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt",
          "PU": "94XPUwei_corrections.pkl.gz",
          "JME": "jec_compiled.pkl.gz",
        ## Btag SFs- create dict specifying SFs for DeepCSV b-tag(DeepCSVB),  DeepJet b-tag(DeepJetB),DeepCSV c-tag(DeepCSVC),  DeepJet c-tag(DeepJetC),
          "BTV": {
              ### b-tag 
              "DeepCSVB": "DeepCSV_94XSF_V5_B_F.csv",
              "DeepJetB": "DeepFlavour_94XSF_V4_B_F.csv",
              ### c-tag
              "DeepCSVC": "DeepCSV_ctagSF_MiniAOD94X_2017_pTincl_v3_2_interp.root",
              "DeepJetC": "DeepJet_ctagSF_MiniAOD94X_2017_pTincl_v3_2_interp.root",
          },
          ## lepton SF - create dict specifying SFs for electron/muon ID/ISO/RECO SFs
          "LSF": {
              ### Following the scheme "${SF_name} ${histo_name_in_root_file}": "${file}"
              "ele_Trig TrigSF": "Ele32_L1DoubleEG_TrigSF_vhcc.histo.root",
              "ele_ID EGamma_SF2D": "ElectronIDSF_94X_MVA80WP.histo.root",
              "ele_Rereco EGamma_SF2D": "ElectronRecoSF_94X.histo.root",
              "mu_ID NUM_TightID_DEN_genTracks_pt_abseta": "RunBCDEF_MuIDSF.histo.root",
              "mu_ID_low NUM_TightID_DEN_genTracks_pt_abseta": "RunBCDEF_MuIDSF_lowpT.histo.root",
              "mu_Iso NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta": "RunBCDEF_MuISOSF.histo.root",
          },
      },
  ```

 

#### Use central maintained jsonpog-integration
  
The official correction files collected in [jsonpog-integration](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration) is updated by POG, except `lumiMask` and `JME` still updated by by the BTVNanoCommissioning framework user/developer.  For centrally maintained correction files, no input files have to be defined anymore in the `correction_config`.  


  ```python
    "2017_UL": {
          # Same with custom config
          "lumiMask": "Cert_294927-306462_13TeV_UL2017_Collisions17_MuonJSON.txt",
          "JME": "jec_compiled.pkl.gz",
          # no config need to be specify for PU weights
          "PU": None,
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
          # WPs : ['NUM_GlobalMuons_DEN_genTracks', 'NUM_HighPtID_DEN_TrackerMuons', 'NUM_HighPtID_DEN_genTracks', 'NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoTight', 'NUM_LooseID_DEN_TrackerMuons', 'NUM_LooseID_DEN_genTracks', 'NUM_LooseRelIso_DEN_LooseID', 'NUM_LooseRelIso_DEN_MediumID', 'NUM_LooseRelIso_DEN_MediumPromptID', 'NUM_LooseRelIso_DEN_TightIDandIPCut', 'NUM_LooseRelTkIso_DEN_HighPtIDandIPCut', 'NUM_LooseRelTkIso_DEN_TrkHighPtIDandIPCut', 'NUM_MediumID_DEN_TrackerMuons', 'NUM_MediumID_DEN_genTracks', 'NUM_MediumPromptID_DEN_TrackerMuons', 'NUM_MediumPromptID_DEN_genTracks', 'NUM_Mu50_or_OldMu100_or_TkMu100_DEN_CutBasedIdGlobalHighPt_and_TkIsoLoose', 'NUM_SoftID_DEN_TrackerMuons', 'NUM_SoftID_DEN_genTracks', 'NUM_TightID_DEN_TrackerMuons', 'NUM_TightID_DEN_genTracks', 'NUM_TightRelIso_DEN_MediumID', 'NUM_TightRelIso_DEN_MediumPromptID', 'NUM_TightRelIso_DEN_TightIDandIPCut', 'NUM_TightRelTkIso_DEN_HighPtIDandIPCut', 'NUM_TightRelTkIso_DEN_TrkHighPtIDandIPCut', 'NUM_TrackerMuons_DEN_genTracks', 'NUM_TrkHighPtID_DEN_TrackerMuons', 'NUM_TrkHighPtID_DEN_genTracks']

              "mu_Reco 2017_UL": "NUM_TrackerMuons_DEN_genTracks",
              "mu_HLT 2017_UL": "NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoTight",
              "mu_ID 2017_UL": "NUM_TightID_DEN_TrackerMuons",
              "mu_Iso 2017_UL": "NUM_TightRelIso_DEN_TightIDandIPCut",
          },
      },
  ```


### Create compiled JERC file(`pkl.gz`)

  >  [!Caution]
> In case existing correction file doesn't work for you due to the incompatibility of `cloudpickle` in different python versions. Please recompile the file to get new pickle file.

  Under `compile_jec.py` you need to create dedicated jet factory files with different campaigns. Following the name scheme with `mc` for MC and `data${run}` for data.

  Compile correction pickle files for a specific JEC campaign by changing the dict of jet_factory, and define the MC campaign and the output file name by passing it as arguments to the python script:

  ```bash
  python -m BTVNanoCommissioning.utils.compile_jec ${campaign} jec_compiled
  e.g. python -m BTVNanoCommissioning.utils.compile_jec Winter22Run3 jec_compiled
  ```
