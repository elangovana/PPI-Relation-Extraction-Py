import argparse
import json
import logging
import os
import sys

from Train import run

"""
This is the sagemaker entry point
"""




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description='PPI interaction: Text Classification')

    parser.add_argument('entry', required=True,
                        help='The dataset file with respect to the train directory', choices={"train"})

    parser.add_argument('--traindata', required=True,
                        help='The dataset file with respect to the train directory')

    parser.add_argument('--traindata-dir',
                        help='The directory containing training artifacts such as training data',
                        default=os.environ.get('SM_CHANNEL_TRAIN', "."))

    parser.add_argument('--out', '-o', default=os.environ.get('SM_OUTPUT_DATA_DIR', "result_data"),
                        help='Directory to output the result')
    args = parser.parse_args()

    logger.info("Invoking training with arguments \n ..{}".format(json.dumps(args.__dict__, indent=2)))

    # args parse

    training_set = os.path.join(args.traindata_dir, args.traindata)
    out = args.out


    # Based on the op
    if args.entry == "train":
        run(training_set, out)
