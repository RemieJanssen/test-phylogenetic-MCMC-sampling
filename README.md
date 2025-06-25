# test-phylonet-sampling
Test phylonet sampling under uninformative information

Main script is `generate_trees_phylonet.sh`
First activate the conda environment.
```
  mamba env update -f ./phylonet.conda-env.yaml
  conda activate phylonet
```

Then set the location of the PhyloNet jar file in the script, and go!

To run on an LSF cluster: `bsub -o hpc.out -e hpc.err ./generate_trees_phylonet.sh`