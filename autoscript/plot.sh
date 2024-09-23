python -W ignore scripts/plotdataMC.py -i hists_ttdilep_sf_promptd.coffea,hists_ttdilep_sf_bpix_tt.coffea --ext "Prompt2023D" -v all -p ttdilep_sf --lumi 9525&
python -W ignore scripts/plotdataMC.py -i hists_ttdilep_sf_rerecod.coffea,hists_ttdilep_sf_bpix_tt.coffea --ext "Rereco2023D" -v all -p ttdilep_sf --lumi 9525&
python -W ignore scripts/plotdataMC.py -i hists_ttdilep_sf_prompt2023.coffea,hists_ttdilep_sf_summer23tt.coffea --ext "Prompt2023BC" -v all -p ttdilep_sf --lumi 17682&
python -W ignore scripts/plotdataMC.py -i hists_ttdilep_sf_rereco2023.coffea,hists_ttdilep_sf_summer23tt.coffea --ext "Rereco2023BC" -v all -p ttdilep_sf --lumi 17682&

python -W ignore scripts/plotdataMC.py -i hists_ttdilep_sf_MC_Summer22EE_Run3_2022_BTV_Comm_v2_NanoV12_noPF/hists_ttdilep_sf_MC_Summer22EE_Run3_2022_BTV_Comm_v2_NanoV12_noPF.coffea,hists_ttdilep_sf_data_Summer22EE_Run3_2022_em_BTV_Comm_v2_NanoV12_noPF/hists_ttdilep_sf_data_Summer22EE_Run3_2022_em_BTV_Comm_v2_NanoV12_noPF.coffea --ext "Prompt2022FG" -v jet* -p ttdilep_sf --lumi 21100&

python -W ignore scripts/plotdataMC.py -i hists_ctag_Wc_sf_data_Summer22_Run3_2022_mu_BTV_Comm_v2_NanoV12_noPF.coffea,hists_ctag_Wc_sf_MC_Summer22_Run3_2022_BTV_Comm_v2_NanoV12_noPF.coffea --ext "Rereco2022CD" -v btagPNetCv* -p ctag_Wc_sf --lumi 8100 --log  --autorebin 2 --flow none&
python -W ignore scripts/plotdataMC.py -i hists_ctag_Wc_sf_data_Summer22EE_Run3_2022_mu_BTV_Comm_v2_NanoV12_noPF.coffea,hists_ctag_Wc_sf_MC_Summer22EE_Run3_2022_BTV_Comm_v2_NanoV12_noPF.coffea --ext "Prompt2022FG" -v btagPNetC* -p ctag_Wc_sf --lumi 21100 --log --autorebin 2 --flow none& 

### W+c
# 2022 prompt/rereco
python -W ignore scripts/comparison.py -i testfile/hists_ctag_Wc_sf_data_Winter22_mu_BTV_Run3_2022_Comm_v1.coffea,hists_ctag_Wc_sf_data_Summer22_Run3_2022_mu_BTV_Comm_v2_NanoV12_noPF.coffea --ext "2022CD" -v btagDeepFlav* -p ctag_Wc_sf --mergemap '{"Prompt2022CD":["Muon_Run2022C-PromptReco-v1", "SingleMuon_Run2022C-PromptReco-v1", "Muon_Run2022D-PromptReco-v1", "Muon_Run2022D-PromptReco-v2"],"Rereco2022CD":["MuonRun2022D-27Jun2023-v2", "MuonRun2022C-27Jun2023-v1", "DoubleMuonRun2022C-27Jun2023-v1", "SingleMuonRun2022C-27Jun2023-v1"]}'  -r Prompt2022CD -c Rereco2022CD --norm&
## 2022 pre/postEE
python -W ignore scripts/comparison.py -i hists_ctag_Wc_sf_data_Summer22EE_Run3_2022_mu_BTV_Comm_v2_NanoV12_noPF.coffea,hists_ctag_Wc_sf_data_Summer22_Run3_2022_mu_BTV_Comm_v2_NanoV12_noPF.coffea --ext "2022" -v btag* -p ctag_Wc_sf --mergemap '{"Rereco2022CD":["MuonRun2022D-27Jun2023-v2", "MuonRun2022C-27Jun2023-v1", "DoubleMuonRun2022C-27Jun2023-v1", "SingleMuonRun2022C-27Jun2023-v1"],"Prompt2022FG":["Muon_Run2022G-PromptReco-v1", "Muon_Run2022F-PromptReco-v1"]}' -r Rereco2022CD -c Prompt2022FG --flow none --norm --autorebin 2 &

 python -W ignore scripts/plotdataMC.py -i hists_ttdilep_sf_MC_SummerEE_JEC.coffea,hists_ttdilep_sf_data_Summer22EE_Run3_2022_em_BTV_Comm_v2_NanoV12_noPF/hists_ttdilep_sf_data_Summer22EE_Run3_2022_em_BTV_Comm_v2_NanoV12_noPF.coffea --ext "Prompt2022FG" -v btagPNet* -p ttdilep_sf --lumi 21100 --norm&
#### ttdilep 
## 2022 prompt/rereco
python -W ignore scripts/comparison.py -i hists_ttdilep_sf_prompt2022.coffea,hists_ttdilep_sf_data_Summer22_Run3_2022_em_BTV_Comm_v2_NanoV12_noPF.coffea --ext "2022CD" -v btagDeepFlavCv* -p ttdilep_sf --mergemap '{"Prompt2022CD":[ "MuonEGRun2022D-PromptNanoAODv10_v1-v1", "MuonEGRun2022C-PromptNanoAODv10-v1","MuonEGRun2022D-PromptNanoAODv10_v2-v1"],"Rereco2022CD":["MuonEGRun2022D-27Jun2023-v2", "MuonEGRun2022C-27Jun2023-v1"]}' -r Prompt2022CD -c Rereco2022CD --flow none  --norm&
## 2022 pre/postEE & 2023 pre/postPBix
python -W ignore scripts/comparison.py -i hists_ttdilep_sf_prompt_NANO.coffea,hists_ttdilep_sf_data_Summer22_Run3_2022_em_BTV_Comm_v2_NanoV12_noPF.coffea,hists_ttdilep_sf_rereco2023.coffea,hists_ttdilep_sf_rerecod.coffea --ext "" -v btagPNett* -p ttdilep_sf --mergemap '{"Rereco2022CD":["MuonEGRun2022D-27Jun2023-v2", "MuonEGRun2022C-27Jun2023-v1"],"Prompt2022FG":["MuonEGRun2022F-22Sep2023-v1", "MuonEGRun2022G-22Sep2023-v1"],"Rereco2023BC":["MuonEGRun2023C-22Sep2023_v1", "MuonEGRun2023C-22Sep2023_v3", "MuonEGRun2023B-22Sep2023", "MuonEGRun2023C-22Sep2023_v4", "MuonEGRun2023C-22Sep2023_v2"],"Rereco2023D":["MuonEGRun2023D-22Sep2023_v2", "MuonEGRun2023D-22Sep2023_v1"]}' -r Rereco2022CD -c Prompt2022FG,Rereco2023BC,Rereco2023D --flow none --norm &
# 2023 preBpix prompt_rereco
python -W ignore scripts/comparison.py -i hists_ttdilep_sf_prompt2023.coffea,hists_ttdilep_sf_rereco2023.coffea --ext "2023BC" -v jet* -p ttdilep_sf --mergemap '{"Prompt2023BC":["MuonEGRun2023B-PromptNanoAODv11p9_v1-v", "MuonEGRun2023C-PromptNanoAODv12_v2-v2", "MuonEGRun2023C-PromptNanoAODv12_v4-v", "MuonEGRun2023C-PromptNanoAODv11p9_v1-v1", "MuonEGRun2023C-PromptNanoAODv12_v3-v"],"Rereco2023BC":["MuonEGRun2023C-22Sep2023_v1", "MuonEGRun2023C-22Sep2023_v3", "MuonEGRun2023B-22Sep2023", "MuonEGRun2023C-22Sep2023_v4", "MuonEGRun2023C-22Sep2023_v2"]}' -r Prompt2023BC -c Rereco2023BC --flow none &
# 2023 postBpix prompt_rereco
python -W ignore scripts/comparison.py -i hists_ttdilep_sf_promptd.coffea,hists_ttdilep_sf_rerecod.coffea --ext "2023D" -v btag* -p ttdilep_sf --mergemap '{"Rereco2023D":["MuonEGRun2023D-22Sep2023_v2", "MuonEGRun2023D-22Sep2023_v1"],"Prompt2023D":["MuonEGRun2023D-PromptReco-v2", "MuonEGRun2023D-PromptReco-v1"]}' -r Prompt2023D -c Rereco2023D --flow none &



