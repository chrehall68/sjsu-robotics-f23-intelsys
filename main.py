from gui import GUI
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--width", type=int, required=False, default=10)
parser.add_argument("--height", type=int, required=False, default=10)

if __name__ == "__main__":
    args = parser.parse_args()
    g = GUI([args.width, args.height])
    g.run()
