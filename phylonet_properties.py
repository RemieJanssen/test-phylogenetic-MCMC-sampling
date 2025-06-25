from phylox import DiNetwork
from phylox.networkproperties.properties import b2_balance, blob_properties, count_reducible_pairs
from phylox.constants import LABEL_ATTR
import pandas as pd
import argparse


def is_bottom_of_triangle(network, node):
    parents = list(network.predecessors(node))
    return parents[0] in network.predecessors(parents[1]) or parents[1] in network.predecessors(parents[0])

def leaves_under_reticulation(network):
    """
    Finds the list leaves that are under a reticulation, ordered alphabetically.
    """
    leaves = network.leaves
    reticulation_leaves = [network.nodes[l].get(LABEL_ATTR, "noLabel") for l in leaves if network.is_reticulation(network.parent(l))]
    return sorted(reticulation_leaves)

def leaf_with_sibling_retic(network):
    """
    Returns the leaf with a sibling reticulation
    if there is such a leaf, otherwise returns None.
    """
    leaves = network.leaves
    for leaf in leaves:
        leaf_parent = network.parent(leaf)
        if network.is_reticulation(leaf_parent):
            continue
        sibling = network.child(leaf_parent, exclude=[leaf])
        if network.is_reticulation(sibling):
            return leaf
    return None

def has_leaf_on_bottom_of_triangle(network):
    leaves = network.leaves
    for leaf in leaves:
        leaf_parent = network.parent(leaf)
        if not network.is_reticulation(leaf_parent):
            continue
        parents = list(network.predecessors(leaf_parent))
        if parents[0] in network.predecessors(parents[1]) or parents[1] in network.predecessors(parents[0]):
            return network.nodes[leaf].get(LABEL_ATTR, "noLabel")
    return "None"

def leaf_on_side_of_triangle(network):
    """
    Returns True iff there is a leaf hanging off of the side
    of a triangle.
    """
    leaf = leaf_with_sibling_retic(network)
    if leaf is None:
        return False
    leaf_parent = network.parent(leaf)
    sibling = network.child(leaf_parent, exclude=[leaf])
    leaf_grandparent = network.parent(leaf_parent)
    sibling_parent = network.parent(sibling, exclude=[leaf_parent])
    return leaf_grandparent == sibling_parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Takes clipped PhyloNet output (until the ---summarization--- part), and calculates
        properties of the networks in this output.
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-f",
        "--filepath",
        type=str,
        required=True,
        help="Input filepath",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output filepath",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    input_path = args.filepath

    phylonet_output = pd.read_csv(input_path, sep=";", header='infer', index_col=False)

    print(phylonet_output)

    data = {
        "index": [],
        "retics": [],
        "balance": [],
        "blob_sizes": [],
        "leaf_under_reticulation_list": [],
        "leaf_with_sibling_retic_list": [],
        "leaf_on_side_of_triangle_list": [],
        "has_leaf_on_bottom_of_triangle": [],
        "reticulated_cherries": [],
    }

    for index, row in phylonet_output.iterrows():
        print(index)
        newick = row["Newick"]
        network = DiNetwork.from_newick(newick)

        data["index"] += [index]
        data["retics"] += [network.reticulation_number]
        data["balance"] += [b2_balance(network)]
        data["blob_sizes"] += [str(sorted([blob[0] for blob in blob_properties(network)]))]
        data["leaf_under_reticulation_list"] += [str(leaves_under_reticulation(network))]
        data["has_leaf_on_bottom_of_triangle"] += [has_leaf_on_bottom_of_triangle(network)]
        if (leaf := leaf_with_sibling_retic(network)) is not None:
            data["leaf_with_sibling_retic_list"] += [network.nodes[leaf].get(LABEL_ATTR, "noLabel")]
        else:
            data["leaf_with_sibling_retic_list"] += ["None"]

        data["leaf_on_side_of_triangle_list"] += [leaf_on_side_of_triangle(network)]
        data["reticulated_cherries"] += [count_reducible_pairs(network)["reticulate_cherries"]]

    network_properties = pd.DataFrame(data)
    network_properties = network_properties.join(phylonet_output)
    network_properties["posterior_probability"] = network_properties["Posterior"].apply(lambda x: 10**x)
    print(network_properties)
    network_properties.to_csv(args.output)

    groupy_columns = ["retics","balance","blob_sizes","leaf_under_reticulation_list","leaf_with_sibling_retic_list","leaf_on_side_of_triangle_list","reticulated_cherries", "has_leaf_on_bottom_of_triangle"]
    counts = network_properties.groupby(groupy_columns,as_index=False)\
        .agg(count=("index", "size"), median_posterior_probability=('posterior_probability', 'median'), mean_posterior_probability=('posterior_probability', 'mean'))\
        .reset_index()
    print(counts)

    counts.to_csv(f"{args.output}.counts")

if __name__ == "__main__":
    main()