## Selections for different phase spaces
  After a small test, you can run the full campaign for a dedicated phase space, separately for data and for MC.

#### b-SFs

Dileptonic $t\bar{t}$ phase space: check performance for btag SFs, e$\mu$ channel

```bash
python runner.py --workflow ttdilep_sf --json metadata/data_Winter22_emu_BTV_Run3_2022_Comm_v1.json  --campaign Winter22Run3 --year 2022 --isJERC --isCorr  (--executor ${scaleout_site}) 
```

Semileptonic $t\bar{t}$ phase space : check performance for btag SFs, muon channel

```bash
python runner.py --workflow ttsemilep_sf --json metadata/data_Winter22_mu_BTV_Run3_2022_Comm_v1.json --campaign Winter22Run3 --year 2022 --isJERC --isCorr  (--executor ${scaleout_site})
```

#### c-SFs

Dileptonic ttbar phase space : check performance for charm SFs, bjets enriched SFs, muon channel

```bash
python runner.py --workflow ctag_ttdilep_sf --json metadata/data_Winter22_mumu_BTV_Run3_2022_Comm_v1.json --campaign Winter22Run3 --year 2022 --isJERC --isCorr (--executor ${scaleout_site})
```

Semileptonic ttbar phase space : check performance for charm SFs, bjets enriched SFs, muon channel

```bash
python runner.py --workflow ctag_ttsemilep_sf --json metadata/data_Winter22_mu_BTV_Run3_2022_Comm_v1.json --campaign Winter22Run3 --year 2022 --isJERC --isCorr (--executor ${scaleout_site})
```

W+c phase space : check performance for charm SFs, cjets enriched SFs, muon channel

```bash
python runner.py --workflow ctag_Wc_sf --json metadata/data_Winter22_mu_BTV_Run3_2022_Comm_v1.json --campaign Winter22Run3 --year 2022 --isJERC --isCorr (--executor ${scaleout_site})
```

DY phase space : check performance for charm SFs, light jets enriched SFs, muon channel

```bash
python runner.py --workflow ctag_DY_sf --json metadata/data_Winter22_mumu_BTV_Run3_2022_Comm_v1.json --campaign Winter22Run3 --year 2022 --isJERC --isCorr (--executor ${scaleout_site})
```

#### BTA - BTagAnalyzer Ntuple producer

Based on Congqiao's [development](notebooks/BTA_array_producer.ipynb) to produce BTA ntuples based on PFNano.

> [!Caution]
> Only the newest version [BTV_Run3_2022_Comm_MINIAODv4](https://github.com/cms-btv-pog/btvnano-prod) ntuples work. Example files are given in [this](metadata/test_bta_run3.json) json. Optimize the chunksize(`--chunk`) in terms of the memory usage. This depends on sample, if the sample has huge jet collection/b-c hardons. The more info you store, the more memory you need. I would suggest to test with `iterative` to estimate the size.




Run with the nominal `BTA` workflow to include the basic event variables, jet observables, and GEN-level quarks, hadrons, leptons, and V0 variables. 
```
python runner.py --wf BTA --json metadata/test_bta_run3.json --campaign Summer22EERun3 --isJERC
```

Run with the `BTA_addPFMuons` workflow to additionally include the `PFMuon` and `TrkInc` collection, used by the b-tag SF derivation with the QCD(μ) methods.
```
python runner.py --wf BTA_addPFMuons --json metadata/test_bta_run3.json --campaign Summer22EERun3 --isJERC
```

Run with the `BTA_addAllTracks` workflow to additionally include the `Tracks` collection, used by the JP variable calibration.
```
python runner.py --wf BTA_addAllTracks --json metadata/test_bta_run3.json --campaign Summer22EERun3 --isJERC
```



### Prompt data/MC checks (prompt_dataMC campaign)

To quickly check the data/MC quickly, run part data/MC files, no SFs/JEC are applied, only the lumimasks.

1. Get the file list from DAS, use the `scripts/fetch.py` scripts to obtain the jsons
2. Replace the lumimask name in prompt_dataMC in `AK4_parameters.py` , you can do `sed -i 's/$LUMIMASK_DATAMC/xxx.json/g`
3. Run through the dataset to obtained the `coffea` files
4. Dump the lumi information via `dump_processed.py`, then use `brilcalc` to get the dedicated luminosity info
5. Obtained data MC plots

### Validation workflow
