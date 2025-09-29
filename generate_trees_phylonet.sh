set -x

# PHYLONET_PATH=~/Documents/Studie/PhD/Software/PhyloNet/PhyloNet_3.7.3.jar
PHYLONET_PATH=~/PhyloNet/PhyloNet_3.8.2.jar

# NEXUS_FILE="./mcmc_gene_trees.nex"
# NEXUS_FILE="./mcmc_gene_trees_large_sample.nex"
# NEXUS_FILE="./mcmc_gene_trees_large_sample_pseudo.nex"
NEXUS_FILE="mcmc_sequence.nex"

PHYLONET_RESULTS_PATH="./phylonet"

OUTPUT_FILENAME="phylonet_generated_networks.out"
ERROR_FILENAME="phylonet_generated_networks.err"
TABLE_OUT_FILENAME="table_gene_trees2.csv"

OUTPUT=${PHYLONET_RESULTS_PATH}/${NEXUS_FILE}.output/$OUTPUT_FILENAME
ERROR=${PHYLONET_RESULTS_PATH}/${NEXUS_FILE}.output/$ERROR_FILENAME
TABLE_OUT=${PHYLONET_RESULTS_PATH}/${NEXUS_FILE}.output/$TABLE_OUT_FILENAME

mkdir ${PHYLONET_RESULTS_PATH}/${NEXUS_FILE}.output

cp ${PHYLONET_RESULTS_PATH}/${NEXUS_FILE} ${PHYLONET_RESULTS_PATH}/${NEXUS_FILE}.output/input.nex

java -jar $PHYLONET_PATH ${PHYLONET_RESULTS_PATH}/${NEXUS_FILE} > $OUTPUT 2> $ERROR

# Clip the phylonet output to the output table:
# remove the first lines with info and everything after the summary line
SUMMARY_LINE=$(grep -nF "Summarization" $OUTPUT | cut --delimiter=":" --fields=1)
head -n $(( SUMMARY_LINE -1 )) $OUTPUT > $OUTPUT.clipped
tail -n +3 $OUTPUT.clipped > $OUTPUT.clipped_buff
mv $OUTPUT.clipped_buff $OUTPUT.clipped

# Remove every other enter, to get Newick on same line as
cat $OUTPUT.clipped | awk 'ORS=NR%2?RS:FS' > $OUTPUT.clipped_buff
mv $OUTPUT.clipped_buff $OUTPUT.clipped

#add newick header to table
sed ' 1 s/.*/&;   Newick/' $OUTPUT.clipped > $OUTPUT.clipped_buff
mv $OUTPUT.clipped_buff $OUTPUT.clipped

# remove all spaces
cat $OUTPUT.clipped | tr -d " "  > $OUTPUT.clipped_buff
mv $OUTPUT.clipped_buff $OUTPUT.clipped

# Analyse all networks
python ./network_properties/phylonet_properties.py -f $OUTPUT.clipped -o $TABLE_OUT
