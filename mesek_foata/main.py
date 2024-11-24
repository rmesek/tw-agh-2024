import argparse
from pathlib import Path

from foata_analyzer import FoataAnalyzer


def valid_file(filename):
    path = Path(filename)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File {filename} does not exist")
    return path


parser = argparse.ArgumentParser(
    description="Analyze Foata Normal Form from input text file"
)
parser.add_argument(
    "-i",
    "--input",
    type=valid_file,
    required=True,
    help="Input text file containing words to analyze (required)",
)
parser.add_argument(
    "-d",
    "--dependency",
    action="store_true",
    help="Calculate dependency relation D",
)
parser.add_argument(
    "-n",
    "--independence",
    action="store_true",
    help="Calculate independence relation I",
)
parser.add_argument(
    "-f",
    "--fnf",
    action="store_true",
    help="Calculate Foata Normal Form FNF([w]) for trace [w]",
)
parser.add_argument(
    "-g",
    "--graph",
    action="store_true",
    help="Calculate minimal dependency graph for word w in DOT format",
)
parser.add_argument(
    "-p",
    "--plot-graph",
    action="store_true",
    help="Draw minimal dependency graph for word w (requires `matplotlib` and `networkx`)",
)


def main():
    args = parser.parse_args()
    if not any(
        [args.dependency, args.independence, args.fnf, args.graph, args.plot_graph]
    ):
        parser.error("At least one analysis option must be selected")

    if args.plot_graph:
        try:
            import matplotlib.pyplot  # noqa
            import networkx  # noqa
        except ImportError:
            parser.error("--plot-graph requires `matplotlib` and `networkx`")
        analyzer = FoataAnalyzer(args.input, nxgraph=True)
    else:
        analyzer = FoataAnalyzer(args.input)

    if args.dependency:
        print(f"D = {analyzer.dependency_relation}")

    if args.independence:
        print(f"I = {analyzer.independence_relation}")

    if args.fnf:
        print(f"FNF([w]) = {analyzer.foata_normal_form}")

    if args.graph:
        print(analyzer.dependency_graph)

    if args.plot_graph:
        analyzer.plot_dependency_graph()


if __name__ == "__main__":
    main()
