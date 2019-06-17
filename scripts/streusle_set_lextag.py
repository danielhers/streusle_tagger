import argparse


def main(args):
    pass


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Swap lextags into a STREUSLE file")
    argparser.add_argument("fname", help="conllulex or json file with full STREUSLE annotation")
    argparser.add_argument("lextags", help="jsonlines file: each line is a list of lextags for a sentence")
    argparser.add_argument("-o", "--out", help="output filename, default being derived from fname + lextags arguments")
    main(argparser.parse_args())
