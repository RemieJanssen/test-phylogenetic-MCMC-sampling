from phylox import DiNetwork
from phylox.networkproperties.properties import b2_balance, blob_properties
from phylox.constants import LABEL_ATTR
import pandas as pd
import argparse


def is_bottom_of_triangle(network, node):
    parents = list(network.predecessors(node))
    return parents[0] in network.predecessors(parents[1]) or parents[1] in network.predecessors(parents[0])

def leaf_under_reticulation(network):
    """
    Finds the leaf that is under a reticulation, if there is any.
    If both are under a reticulation, then it finds the leaf that is on the side of a triangle.

    Note: For a network with 2 leaves and 2 reticulations, there must be such a
    leaf if both leaves are under a reticulation.
    """
    parent_retic_leaf = None
    leaves = network.leaves
    for leaf in leaves:
        leaf_parent = network.parent(leaf)
        if not network.is_reticulation(leaf_parent):
            continue
        if parent_retic_leaf is None or is_bottom_of_triangle(network, leaf_parent):
            parent_retic_leaf = leaf
    return parent_retic_leaf

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
    }

    for index, row in phylonet_output.iterrows():
        print(index)
        newick = row["Newick"]
        print(newick)
        network = DiNetwork.from_newick(newick)

        data["index"] += [index]
        data["retics"] += [network.reticulation_number]
        data["balance"] += [b2_balance(network)]
        data["blob_sizes"] += [sorted([blob[0] for blob in blob_properties(network)])]
        if (leaf := leaf_under_reticulation(network)) is not None:
            data["leaf_under_reticulation_list"] += [network.nodes[leaf].get(LABEL_ATTR, "noLabel")]
        else:
            data["leaf_under_reticulation_list"] += ["None"]

        if (leaf := leaf_with_sibling_retic(network)) is not None:
            data["leaf_with_sibling_retic_list"] += [network.nodes[leaf].get(LABEL_ATTR, "noLabel")]
        else:
            data["leaf_with_sibling_retic_list"] += ["None"]

        data["leaf_on_side_of_triangle_list"] += [leaf_on_side_of_triangle(network)]

    network_properties = pd.DataFrame(data)
    print(network_properties)
    network_properties.to_csv(args.output)

if __name__ == "__main__":
    main()