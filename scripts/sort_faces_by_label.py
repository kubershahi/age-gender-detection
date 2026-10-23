"""Sort Adience aligned face crops into one folder per label.

Reads the Adience fold metadata (data/folds/fold_frontal_*_data.txt) and copies each
face from the raw Adience `faces/` directory into data/unsegregated/<task>/<label>/.

Usage:
    python scripts/sort_faces_by_label.py --faces /path/to/adience/faces --task gender
    python scripts/sort_faces_by_label.py --faces /path/to/adience/faces --task age
"""

import argparse
import glob
import os
import shutil
from collections import Counter

AGE_GROUPS = {'(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)'}
GENDERS = {'f', 'm'}


def label_for(row, task):
	if task == 'gender':
		return row['gender'] if row['gender'] in GENDERS else None
	return row['age'] if row['age'] in AGE_GROUPS else None


def main():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('--faces', required=True, help='Adience faces/ directory (one subfolder per user_id)')
	parser.add_argument('--task', choices=['age', 'gender'], required=True)
	parser.add_argument('--folds', default='data/folds', help='directory containing fold_frontal_*_data.txt')
	parser.add_argument('--out', default='data/unsegregated', help='output root; images go to <out>/<task>/<label>/')
	args = parser.parse_args()

	counts = Counter()
	for fold in sorted(glob.glob(os.path.join(args.folds, 'fold_frontal_*_data.txt'))):
		with open(fold) as file:
			header = file.readline().rstrip('\n').split('\t')
			for line in file:
				row = dict(zip(header, line.rstrip('\n').split('\t')))
				label = label_for(row, args.task)
				if label is None:
					continue

				img = os.path.join(args.faces, row['user_id'],
				                   'coarse_tilt_aligned_face.' + row['face_id'] + '.' + row['original_image'])
				if not os.path.exists(img):
					continue

				dest = os.path.join(args.out, args.task, label)
				os.makedirs(dest, exist_ok=True)
				shutil.copy(img, dest)
				counts[label] += 1

	for label, n in sorted(counts.items()):
		print(label, n)


if __name__ == '__main__':
	main()
