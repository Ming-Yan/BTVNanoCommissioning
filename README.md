
# BTVNanoCommissioning
[![Linting](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/python_linting.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/python_linting.yml)
[![btag ttbar](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ttbar_workflow.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ttbar_workflow.yml)
[![ctag ttbar](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ctag_ttbar_workflow.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ctag_ttbar_workflow.yml)
[![ctag DY+jets Workflow](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ctag_DY_workflow.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ctag_DY_workflow.yml)
[![ctag W+c Workflow](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ctag_Wc_workflow.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/ctag_Wc_workflow.yml)
[![BTA Workflow](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/BTA_workflow.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/BTA_workflow.yml)
[![QCD Workflow](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/QCD_workflow.yml/badge.svg)](https://github.com/cms-btv-pog/BTVNanoCommissioning/actions/workflows/QCD_workflow.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repository for Commissioning studies in the BTV POG based on (custom) nanoAOD samples
Detailed documentation in [btv-wiki](https://btv-wiki.docs.cern.ch/SoftwareAlgorithms/BTVNanoCommissioning/)

## Requirements
### Setup 

> [!Caution]
> suggested to install under `bash` environment

```
# only first time, including submodules
git clone --recursive git@github.com:cms-btv-pog/BTVNanoCommissioning.git 

# activate enviroment once you have coffea framework 
conda activate btv_coffea
```
#### Coffea installation with Micromamba
For installing Micromamba, see [[here](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)]
```
wget -L micro.mamba.pm/install.sh
# Run and follow instructions on screen
bash install.sh
```
NOTE: always make sure that conda, python, and pip point to local micromamba installation (`which conda` etc.).

You can simply create the environment through the existing `test_env.yml` under your micromamba environment using micromamba, and activate it
```
micromamba env create -f test_env.yml 
micromamba activate btv_coffea
```

Once the environment is set up, compile the python package:
```
pip install -e .
pip install -e .[dev, doc] # for developer
```



## Structure
 
Each workflow can be a separate "processor" file, creating the mapping from NanoAOD to
the histograms we need. Workflow processors can be passed to the `runner.py` script 
along with the fileset these should run over. Multiple executors can be chosen 
(for now iterative - one by one, uproot/futures - multiprocessing and dask-slurm). 

To test a small set of files to see whether the workflows run smoothly, run:
```
python runner.py --workflow ttsemilep_sf --json metadata/test_bta_run3.json --campaign Summer23 --year 2023
```

>[!TIP]
> Documentation can be found [here](https://btvnanocommissioning.readthedocs.io/en/latest/)

