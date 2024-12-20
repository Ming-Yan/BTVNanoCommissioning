## For developers: Add new workflow


The BTV tutorial for coffea part is under [`notebooks`](https://github.com/cms-btv-pog/BTVNanoCommissioning/tree/master/notebooks) and the template to construct new workflow is [`src/BTVNanoCommissioning/workflows/example.py`](https://github.com/cms-btv-pog/BTVNanoCommissioning/blob/master/src/BTVNanoCommissioning/workflows/example.py)

The BTV tutorial for coffea part is `notebooks/BTV_commissiong_tutorial-coffea.ipynb` and the template to construct new workflow is `src/BTVNanoCommissioning/workflows/example.py`.


Use the `example.py` as template to develope new workflow.

### 0. Add new workflow info to `__init__.py` in `workflows` directory.


```python
# if the workflow is in a new files, you need to import your workflow.py
from BTVNanoCommissioning.workflows.new_workflow import (
  NanoProcessor as new_WORKFLOWProcessor
)
# And then include the processor into the modules with the name of workflow. The name is used when specifying --workflow when running the jobs
workflows["name_workflow"] = new_WORKFLOWProcessor
# IF the workflow is based on the modifier to existing workflow, put the selectionModifier used in the existing workflow
workflows["ctag_ttsemilep_sf"] = partial(
    CTAGWcTTValidSFProcessor, selectionModifier="semittM"
)
```
Notice that if you are working on a WP SFs, please put **WP** in the name.

### 1. Add histogram collections to `utils/histogrammer.py`

The histograms are use the [`hist`](https://hist.readthedocs.io/en/latest/) in this framework. This can be easily to convert to root histogram by `uproot` or numpy histograms.  For quick start of hist can be found [here](https://hist.readthedocs.io/en/latest/user-guide/quickstart.html)

There are a few axes are predefined and commonly used for all the workflows, notice that the `name` should be consistent with the info in the tree if it is stored.
```python
pt_axis = Hist.axis.Regular(60, 0, 300, name="pt", label=" $p_{T}$ [GeV]")
eta_axis = Hist.axis.Regular(25, -2.5, 2.5, name="eta", label=" $\eta$")
phi_axis = Hist.axis.Regular(30, -3, 3, name="phi", label="$\phi$")
```
The histograms are wrapped as `dict`, it should contains **syst_axis (at first axis)**,  **Hist.storage.Weight() (in last axis)** and axis for your variable. The key is suggest to use the format of `$OBJECT_$VAR` in case the variable `$VAR` is in the tree. 

```python
_hist_dict["mujet_pt"] = Hist.Hist(
            syst_axis, flav_axis, dr_axis, Hist.storage.Weight()
        )  # create cutstomize histogram
```

The kinematic variables/workflow specific variables are defined first, then it takes the common collections of input variables from the common defintion. 
In case you want to add common variables use for all the workflow, you can go to [`helper/definition.py`](#add-new-common-variables)
###  2. Selections: Implemented selections on events

Create `boolean` arrays along event axis. Also check whether some common selctions already in `utils/selection.py`

```python
      ## HLT- put trigger paths
      triggers = [
          "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
          "Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
          "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
      ]
      req_trig = HLT_helper(events, triggers)

      ##### Add some selections
      ## Muon cuts
      # muon twiki: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2

      muon_sel = (events.Muon.pt > 15) & (mu_idiso(events, self._campaign)) # applied selection on pT, and `mu_idiso` is predefined selection in `selection.py` which refers to cut-based tight muon ID+Iso
      event_mu = events.Muon[muon_sel] # Pruned the muon collections with the selection
      req_muon = ak.num(event_mu.pt) == 1 # Check each event has exact one muon
      .... # other selections
      ## Apply all selections
      event_level = (
          req_trig & req_lumi & req_jet & req_muon & req_ele & req_leadlep_pt
      )
```

In case you are modifying exist workflow, you need to add to  `__init__` and in the selections 

```python
# in init
self.selMod = selectionModifier
# In selection 
if self.selMod=="WcM":
  event_level = req_trig & req_lumi & req_jet & req_muon & req_ele & req_leadlep_pt& req_Wc
```

###  3. Selected objects: Pruned objects with reduced event_level
Store the selected objects to event-based arrays. The selected object must contains **Sel**, for the muon-enriched jet and soft muon is **MuonJet** and **SoftMu**, the kinematics will store. The cross-object variables need to create entry specifically. 

```python
  # Keep the structure of events and pruned the object size
  pruned_ev = events[event_level]
  pruned_ev["SelJet"] = event_jet[event_level][:, 0]
  pruned_ev["SelMuon"] = event_mu[event_level][:, 0]
  pruned_ev["mujet_ptratio"] = event_mu[event_level].pt / pruned_ev.SelJet.pt # notice that the cross-object need to be created specificaly
  pruned_ev["mujet_dr"] =  event_mu[event_level].delta_r(pruned_ev.SelJet) 
```


 The pruned information are then proceed to store into histograms, output arrays and use to evaluate the weight. In case you have customize object for [corrections](#add-additional-weight-or-uncertainty-information), new common [variables](#add-new-common-variables) need to add, please go to dedicated section.
 
See the details below for the usage of `pruned_ev`

<details><summary>output section</summary>
<p>

```python
####################
#     Output       #
####################
# Configure SFs - read pruned objects from the pruned_ev and apply SFs and call the systematics
weights = weight_manager(pruned_ev, self.SF_map, self.isSyst)
# Configure systematics shifts 
if shift_name is None:
    systematics = ["nominal"] + list(weights.variations) # nominal + weight variation systematics
else:
    systematics = [shift_name] # JES/JER systematics

# Fill the weight to output arrys
if not isRealData:
    pruned_ev["weight"] = weights.weight()
    for ind_wei in weights.weightStatistics.keys():
        pruned_ev[f"{ind_wei}_weight"] = weights.partial_weight(
            include=[ind_wei]
        )
# Configure histograms- fill the histograms with pruned objects
if not self.noHist:
    output = histo_writter(
        pruned_ev, output, weights, systematics, self.isSyst, self.SF_map
    )
# Output arrays - store the pruned objects in the output arrays
if self.isArray:
    array_writer(self, pruned_ev, events, systematics[0], dataset, isRealData)
  ```

</p>
</details>


### 4. Setup CI pipeline

The actions are checking the changes would break the framework. The actions are collected in `.github/workflow`
You can simply include a workflow by adding the entries with name

```yaml
- name:  semileptonic + c ttbar workflows with correctionlib
      run: |
        string=$(git log -1 --pretty=format:'%s')
        if [[ $string == *"ci:skip array"* ]]; then
        opts=$(echo "$opts" | sed 's/--isArray //g')
        fi
        if [[ $string == *"ci:skip syst"* ]]; then
            opts=$(echo "$opts" | sed 's/--isSyst all//g')
        elif [[ $string == *"ci:JERC_split"* ]]; then
            opts=$(echo "$opts" | sed 's/--isSyst all/--isSyst JERC_split/g')
        elif [[ $string == *"ci:weight_only"* ]]; then
            opts=$(echo "$opts" | sed 's/--isSyst all/--isSyst weight_only/g') 
        fi
        python runner.py --workflow c_ttsemilep_sf --json metadata/test_bta_run3.json --limit 1 --executor iterative --campaign Summer23 --year 2023  $opts
```

Special commit head messages could run different commands in actions (add the flag in front of your commit)
The default configureation is doing 
```python
python runner.py --workflow emctag_ttdilep_sf --json metadata/test_bta_run3.json --limit 1 --executor iterative --campaign Summer23 --isArray --isSyst all
```

- `[skip ci]`: not running ci at all in the commit message
- `ci:skip array` : remove `--isArray` option
- `ci:skip syst` : remove `--isSyst all` option
- `ci:JERC_split` : change systematic option to split JERC uncertainty sources `--isSyst JERC_split`
- `ci:weight_only` : change systematic option to weight only variations `--isSyst weight_only`

<details><summary>Set CI in your github account</summary>
<p>

Since the CI pipelines involve reading files via `xrootd` and access gitlab.cern.ch, you need to save some secrets in your forked directory. 

Yout can find the secret configuration in the direcotry : `Settings>>Secrets>>Actions`, and create the following secrets:

- `GIT_CERN_SSH_PRIVATE`: 
  1. Create a ssh key pair with `ssh-keygen -t rsa -b 4096` (do not overwrite with your local one), add the public key to your CERN gitlab account
  2. Copy the private key to the entry
- `GRID_PASSWORD`: Add your grid password to the entry.
- `GRID_USERCERT` & `GRID_USERKEY`:  Encrypt your grid user certification `base64 -i ~/.globus/userkey.pem | awk NF=NF RS= OFS=` and `base64 -i ~/.globus/usercert.pem | awk NF=NF RS= OFS=` and copy the output to the entry. 

</p>
</details>


### Optional changes
#### Refine used MC as input 
#### Add workflow to `suball.py` 
#### Add new common variables 
#### Add additional `Weight` or `uncertainty` information 
