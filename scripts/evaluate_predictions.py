"""Report overall and per-class accuracy from a prediction file written by the notebook.

Each line of the file is `<class>/<filename> <desired> <predicted>`.

Usage:
    python scripts/evaluate_predictions.py outputs/gender_prediction.txt
    python scripts/evaluate_predictions.py outputs/age_prediction.txt
"""

import sys
from collections import Counter


def main(path):
	total = Counter()
	correct = Counter()

	with open(path) as file:
		for line in file:
			filename, desired, predicted = line.split()
			label = filename.split('/')[0]
			total[label] += 1
			correct[label] += desired == predicted

	for label in sorted(total):
		print('%-10s %5d / %5d  %6.2f %%' % (label, correct[label], total[label], 100 * correct[label] / total[label]))
	print('%-10s %5d / %5d  %6.2f %%' % ('overall', sum(correct.values()), sum(total.values()),
	                                      100 * sum(correct.values()) / sum(total.values())))


if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit(__doc__)
	main(sys.argv[1])
