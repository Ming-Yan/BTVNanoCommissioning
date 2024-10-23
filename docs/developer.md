## Instructions for developers


The BTV tutorial for coffea part is under [`notebooks`](https://github.com/cms-btv-pog/BTVNanoCommissioning/tree/master/notebooks) and the template to construct new workflow is [`src/BTVNanoCommissioning/workflows/example.py`](https://github.com/cms-btv-pog/BTVNanoCommissioning/blob/master/src/BTVNanoCommissioning/workflows/example.py)

The BTV tutorial for coffea part is `notebooks/BTV_commissiong_tutorial-coffea.ipynb` and the template to construct new workflow is `src/BTVNanoCommissioning/workflows/example.py`.
The roadmap to construct new workflows are dicussed [here](#construct-new-workflows) and a detailed information how to change the modules are described [here](#submodules-within-the-framework). The information to make CI works in forked repository can be found [here](#setup-ci-pipeline-for-fork-branch)

### Construct new workflow

Use the `example.py` as template to develope new workflow.

0. Add new workflow info to `__init__.py` in `workflows` directory.
<details><summary>example variable</summary>
<p>
  
  ```python
 from BTVNanoCommissioning.workflows.new_workflow import (
    NanoProcessor as new_WORKFLOWProcessor
)
workflows["name_workflow"] = new_WORKFLOWProcessor
  ```

</p>
</details>

1. Add histogram collections to [`utils/histogrammer.py`](#utilshistogrammerpy).
2. Implemented selections on events, create `boolean` arrays along event axis. Also check whether some common selctions already in [`utils/selection.py`](#utilsselectionpy)
3. Pruned the object with the event selections ex. `events[event_selection].Electron`
4. Add the `Weight` or `uncertainty` information on selected objects/events.
5. Fill the histograms with the selected events. The input fill to histogram should be always be flat(`np.arrays`). If weight uncertainties are considered, the weights would modified with `weights.weight(modifier=syst)`. Notice for the training input variables, BTV related corrections are excluded. The histograms are accumulated and saved into `.coffea` files
6. Store the selected information into `root` file. Keep event structure, pruned exist objects and add user defined objects into output arrays. Information and example include in `example.py`
### Setup CI pipeline for fork branch
Since the CI pipelines involve reading files via `xrootd` and access gitlab.cern.ch, you need to save some secrets in your forked directory. 

Yout can find the secret configuration in the direcotry : `Settings>>Secrets>>Actions`, and create the following secrets:

- `GIT_CERN_SSH_PRIVATE`: 
  1. Create a ssh key pair with `ssh-keygen -t rsa -b 4096` (do not overwrite with your local one), add the public key to your CERN gitlab account
  2. Copy the private key to the entry
- `GRID_PASSWORD`: Add your grid password to the entry.
- `GRID_USERCERT` & `GRID_USERKEY`:  Encrypt your grid user certification `base64 -i ~/.globus/userkey.pem | awk NF=NF RS= OFS=` and `base64 -i ~/.globus/usercert.pem | awk NF=NF RS= OFS=` and copy the output to the entry. 

Special commit head messages could run different commands in actions (add the flag in front of your commit)
The default configureation is doing 
```
python runner.py --workflow emctag_ttdilep_sf --json metadata/test_bta_run3.json --limit 1 --executor iterative --campaign Summer23 --isArray --isSyst all
```

- `[skip ci]`: not running ci at all in the commit message
- `ci:skip array` : remove `--isArray` option
- `ci:skip syst` : remove `--isSyst all` option
- `ci:JERC_split` : change systematic option to split JERC uncertainty sources `--isSyst JERC_split`
- `ci:weight_only` : change systematic option to weight only variations `--isSyst weight_only`
 
### Running jupyter remotely
1. On your local machine, edit `.ssh/config`:
```
Host lxplus*
  HostName lxplus7.cern.ch
  User <your-user-name>
  ForwardX11 yes
  ForwardAgent yes
  ForwardX11Trusted yes
Host *_f
  LocalForward localhost:8800 localhost:8800
  ExitOnForwardFailure yes
```
2. Connect to remote with `ssh lxplus_f`
3. Start a jupyter notebook:
```
jupyter notebook --ip=127.0.0.1 --port 8800 --no-browser
```
4. URL for notebook will be printed, copy and open in local browser