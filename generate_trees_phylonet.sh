set -x

# PHYLONET_PATH=~/Documents/Studie/PhD/Software/PhyloNet/PhyloNet_3.7.3.jar
PHYLONET_PATH=~/PhyloNet/PhyloNet_3.8.2.jar
OUTPUT="phylonet_generated_networks.out"
ERROR="phylonet_generated_networks.out"


NEXUS_FILE="./mcmc_gene_trees.nex"
TABLE_OUT="table_gene_trees.csv"

# NEXUS_FILE="./mcmc_sequence.nex"
# TABLE_OUT="table_sequence.csv"


java -jar $PHYLONET_PATH $NEXUS_FILE > $OUTPUT >> $ERROR

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
python phylonet_properties.py -f $OUTPUT.clipped -o $TABLE_OUT
