## Installation


>  [!Caution]
>suggested to install under `bash` environment

```
# only first time, including submodules
git clone --recursive git@github.com:cms-btv-pog/BTVNanoCommissioning.git 

# activate enviroment once you have coffea framework 
conda activate btv_coffea
```
### Coffea installation with Micromamba
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
pip install -e .[dev] # for developer
```

### Other installation options for coffea
See [https://coffeateam.github.io/coffea/installation.html](https://coffeateam.github.io/coffea/installation.html)
