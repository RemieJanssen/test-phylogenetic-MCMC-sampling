set -x

# Generate networks
python ./phylox_networks/generate_networks.py -o ./phylox_networks/

# Analyse all networks
python ./network_properties/phylox_properties.py -f ./phylox_networks/networks_corrected.csv -o ./phylox_networks/networks_corrected_counts.csv
python ./network_properties/phylox_properties.py -f ./phylox_networks/networks_not_corrected.csv -o ./phylox_networks/networks_not_corrected_counts.csv
