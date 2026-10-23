"""Build the train/val/test folders the notebook reads from data/unsegregated/.

By default the split follows data/splits/<task>.csv, which reproduces the exact split used
in the report. Pass --random to draw a fresh stratified 80/10/10 split instead.

Usage:
    python scripts/prepare_splits.py --task age
    python scripts/prepare_splits.py --task gender
    python scripts/prepare_splits.py --task age --random --seed 0
"""

import argparse
import csv
import os
import random
import shutil
import sys


def manifest_rows(path):
	with open(path, newline='') as file:
		return [(row['filename'], row['label'], row['split']) for row in csv.DictReader(file)]


def random_rows(source, seed):
	rng = random.Random(seed)
	rows = []
	for label in sorted(os.listdir(source)):
		if label.startswith('.'):
			continue
		files = sorted(f for f in os.listdir(os.path.join(source, label)) if not f.startswith('.'))
		rng.shuffle(files)
		n_val = n_test = round(0.1 * len(files))
		for i, filename in enumerate(files):
			split = 'val' if i < n_val else 'test' if i < n_val + n_test else 'train'
			rows.append((filename, label, split))
	return rows


def main():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('--task', choices=['age', 'gender'], required=True)
	parser.add_argument('--data', default='data', help='data root containing unsegregated/ and splits/')
	parser.add_argument('--random', action='store_true', help='ignore the manifest and draw a new 80/10/10 split')
	parser.add_argument('--seed', type=int, default=0, help='random seed used with --random')
	args = parser.parse_args()

	source = os.path.join(args.data, 'unsegregated', args.task)
	if args.random:
		rows = random_rows(source, args.seed)
	else:
		rows = manifest_rows(os.path.join(args.data, 'splits', args.task + '.csv'))

	missing = 0
	for filename, label, split in rows:
		img = os.path.join(source, label, filename)
		if not os.path.exists(img):
			missing += 1
			continue
		dest = os.path.join(args.data, split + '_' + args.task, label)
		os.makedirs(dest, exist_ok=True)
		shutil.copy(img, dest)

	for split in ('train', 'val', 'test'):
		print(split, sum(1 for row in rows if row[2] == split))
	if missing:
		sys.exit('%d images listed in the split were not found under %s' % (missing, source))


if __name__ == '__main__':
	main()
