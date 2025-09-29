import argparse
import os

from phylox import DiNetwork
from phylox.rearrangement.movetype import MoveType
from phylox.generators.mcmc import sample_mcmc_networks

STARTING_NETWORK = DiNetwork(
    edges=((0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (4, 6)),
    labels=((5, "A"), (6, "B")),
)
# MOVE_TYPE_PROBABILITIES = {
#     MoveType.TAIL: 0.5,
#     MoveType.HEAD: 0.2,
#     MoveType.VPLU: 0.15,
#     MoveType.VMIN: 0.15,
# }
MOVE_TYPE_PROBABILITIES = {
    MoveType.TAIL: 0.8,
    MoveType.HEAD: 0.2,
}
SAMPLES = 10000
SAMPLE_FREQUENCY = 100


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Generates networks with phylox MCMC generator and saves them to file.
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output path",
    )
    return parser.parse_args()


def generate_networks(output_file, correct_for_symmetries):
    with open(output_file, "w+") as f:
        f.write("Iteration;Newick\n")
    for i, network in enumerate(
        sample_mcmc_networks(
            STARTING_NETWORK,
            MOVE_TYPE_PROBABILITIES,
            correct_symmetries=correct_for_symmetries,
            # restriction_map=lambda n: n.reticulation_number <=2,
            burn_in=SAMPLE_FREQUENCY,
            number_of_samples=SAMPLES,
            add_root_if_necessary=True,
            seed=1,
        )
    ):
        with open(output_file, "a") as f:
            f.write(f"{i};{network.newick()}\n")


def main():
    args = parse_args()
    generate_networks(os.path.join(args.output, "networks_corrected.csv"), True)
    generate_networks(os.path.join(args.output, "networks_not_corrected.csv"), False)


if __name__ == "__main__":
    main()
