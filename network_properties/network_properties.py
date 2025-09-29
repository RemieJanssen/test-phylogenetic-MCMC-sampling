from phylox.constants import LABEL_ATTR
from phylox.networkproperties.properties import b2_balance, blob_properties, count_reducible_pairs


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
