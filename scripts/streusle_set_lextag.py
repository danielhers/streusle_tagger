import argparse
import json
import logging

from streusle.conllulex2json import load_sents, print_sents_json

logger = logging.getLogger(__name__)


def swap_lextags(sents, lextags_lines):
    for sent, lextags_line in zip(sents, lextags_lines):
        lextags = json.loads(lextags_line)
        for tok, lextag in zip(sent["toks"], lextags):
            tok["lextag"] = lextag


def main(args):
    with open(args.fname, encoding="utf-8") as f, open(args.lextags, encoding="utf-8") as lextags_lines:
        print_sents_json(swap_lextags(load_sents(f), lextags_lines))


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(levelname)s "
                        "- %(name)s - %(message)s",
                        level=logging.INFO)
    argparser = argparse.ArgumentParser(description="Swap lextags into a STREUSLE file")
    argparser.add_argument("fname", help="conllulex or json file with full STREUSLE annotation")
    argparser.add_argument("lextags", help="jsonlines file: each line is a list of lextags for a sentence")
    main(argparser.parse_args())
