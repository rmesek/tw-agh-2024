import argparse
from pathlib import Path

from file_handler import read_file, write_file
from solver import gaussian_elimination


def valid_in_file(filename):
    path = Path(filename)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File {filename} does not exist")
    return path


def valid_out_file(filename):
    path = Path(filename)
    if not path.parent.exists() and not path.parent.is_dir():
        raise argparse.ArgumentTypeError(f"Directory {path.parent} does not exist")
    return path


parser = argparse.ArgumentParser(
    description="Concurrent Gauss Elimination for NxN matrix"
)

parser.add_argument(
    "-i",
    "--input",
    type=valid_in_file,
    required=True,
    help="Input text file containing NxN matrix to analyze (required)",
)

parser.add_argument(
    "-o",
    "--output",
    type=valid_out_file,
    required=True,
    help="Output text file to save the result (required)",
)


def main():
    args = parser.parse_args()
    A, b = read_file(args.input)
    D, x = gaussian_elimination(A, b)
    write_file(args.output, D, x)


if __name__ == "__main__":
    main()
