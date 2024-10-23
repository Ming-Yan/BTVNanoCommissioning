## Installation


> [!Caution]
> suggested to install under `bash` environment

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

Alternatively, if you are using lxplus, you can simply do

```
micromamba activate /eos/user/m/milee/miniforge3/envs/btv_coffea
```

Once the environment is set up, compile the python package(also do that if new modules are developed):
```
git clone  git@github.com:cms-btv-pog/BTVNanoCommissioning.git 
pip install -e .
pip install -e .[dev] # for developer
```

# activate enviroment once you have coffea framework (Do it everytime) 
```
conda activate btv_coffea
```

### Other installation options for coffea
See [https://coffeateam.github.io/coffea/installation.html](https://coffeateam.github.io/coffea/installation.html)
