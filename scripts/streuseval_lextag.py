import argparse
import ast
import logging
from collections import defaultdict, Counter
from io import StringIO, BytesIO

from streusle.conllulex2json import load_sents, print_sents_json
from streusle.streuseval import to_json, to_tsv, eval_sys
from tqdm import tqdm

from scripts.streusle_set_lextag import SSMapper, swap_lextags

logger = logging.getLogger(__name__)


def main(args):
    ss_mapper = SSMapper(args.depth)

    # Load gold data
    gold_sents = list(tqdm(load_sents(args.goldfile, ss_mapper=ss_mapper),
                           desc="Reading " + args.goldfile.name, unit=" lines"))

    all_sys_scores = {}
    for lextags_file in args.lextags:
        # Load predictions
        with open(lextags_file, encoding="utf-8") as f:
            pred_sents = list(tqdm(swap_lextags(gold_sents, map(ast.literal_eval, f)),
                                   desc="Reading " + lextags_file, unit=" lines"))
        s = StringIO()
        print_sents_json(pred_sents, fh=s)
        s = BytesIO(s.getvalue().encode("utf-8"))
        s.name = "autoid.json"
        scores = eval_sys(s, gold_sents, ss_mapper)
        basename = lextags_file.rsplit('.', 2)[0]
        if basename not in all_sys_scores:
            all_sys_scores[basename] = [defaultdict(lambda: defaultdict(Counter)),
                                        defaultdict(lambda: defaultdict(Counter))]
        if lextags_file.split('.')[-2] == 'goldid':
            all_sys_scores[basename][0] = scores
        else:
            all_sys_scores[basename][1] = scores

    # Print output
    args.output_format(all_sys_scores, depth=args.depth, mode=args.output_mode)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(levelname)s "
                               "- %(name)s - %(message)s",
                        level=logging.INFO)
    argparser = argparse.ArgumentParser(description='Evaluate system output for supersense disambiguation'
                                                    'against a gold standard.')
    argparser.add_argument('goldfile', type=argparse.FileType('r'),
                           help='gold standard .conllulex or .json file')
    argparser.add_argument("lextags", nargs="+", help="jsonlines file: each line is a list of lextags for a sentence"
                                                      "in serialized list notation, e.g., "
                                                      "['B-ADV', 'I~-V-v.communication']")
    argparser.add_argument('--depth', metavar='D', type=int, choices=range(1, 5), default=4,
                           help='depth of hierarchy at which to cluster SNACS supersense labels (default: 4, i.e. no collapsing)')
    # parser.add_argument('--prec-rank', metavar='K', type=int, default=1,
    #                     help='precision@k rank (default: 1)')
    output = argparser.add_mutually_exclusive_group()
    output.add_argument('--json', dest='output_format', action='store_const', const=to_json, default=to_tsv,
                        help='output as JSON (default: output as TSV)')
    output.add_argument('-x', '--extended', dest='output_mode', action='store_const', const='x', default='',
                        help='more detailed TSV output')
    main(argparser.parse_args())
