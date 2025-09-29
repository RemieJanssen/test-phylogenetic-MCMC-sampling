# test-phylogenetic-MCMC-sampling
Test MCMC sampling of phylogenetic networks under an uninformative prior.
The repo contains the configuration for such an experiment using PhyloNet, and using the MCMC sampler of PhyloX.

## PhyloNet
The main script is `generate_networks_phylonet.sh`, which first generates the networks using a nexus file.
Afterwards, it parses the PhyloNet output, and computes some properties of the networks which are sufficient to distinguish between all networks with two leaves and at most two reticulations.
All results are combined in one table and saved to a csv file.

### Code execution
First create a conda environment with the remaining dependencies:
```
  mamba env update -f ./envs/phylonet.yaml
  conda activate phylonet
```

Then make sure PhyloNet is installed, and set the path of the PhyloNet jar executable in `generate_networks_phylonet.sh`.
Run the script directly with `./generate_networks_phylonet.sh`, or run it on an LSF cluster: `bsub -o hpc.out -e hpc.err ./generate_networks_phylonet.sh`

## PhyloX
The main script is `./phylox_networks/generate_networks.py`. This script uses the MCMC method from phylox to generate networks.

### Code execution
First make sure the conda environment is activated:
```
  mamba env update -f ./envs/phylonet.yaml
  conda activate phylonet
```

Run the script directly with `./generate_networks_phylox.sh`,
or run it on an LSF cluster: `bsub -o hpc.out -e hpc.err ./generate_networks_phylox.sh`

