'''
build-rare.py
Reads data, and outputs a list of rare words from the data.
Leon Cheung, lcheung@isi.edu
'''
import argparse, sys, os, time
import logging as log
from collections import Counter

from data import read_sentence_data

log.basicConfig(stream=sys.stderr, level=log.DEBUG)

def least_common(counter):
  return counter.most_common()[::-1]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_in', type=str, default='train.src',
      help='Newline delimited sentence file.')
  parser.add_argument('--rare_out', type=str, default='train.src.rare',
      help='File where the least common words from data_in will be stored.')
  parser.add_argument('--rare_num', type=int, default=2000,
      help='Number of rarest words to take.')
  parser.add_argument('--min_count', type=int, default=5,
      help='Ignore words with count less than this number.')

  args = parser.parse_args()

  lines = read_sentence_data(args.data_in)
  flat_lines = [ e for toks in lines for e in toks ]
  count = Counter(flat_lines)
  log.info('Finished building word count.')
 
  least_count = least_common(count)
  log.debug(least_count[:10])
  log.debug(least_count[-10:])

  with open(args.rare_out, 'w') as f:
    i = 0
    for word, count in least_count:
      if i >= args.rare_num:
        break
      if count > args.min_count:
        f.write('%s\n' % word.strip().lower())
        i += 1

  log.info('Finished outputting rare words to file.')

if __name__ == "__main__":
  time1 = time.time()
  main()
  time2 = time.time()

  duration = (time2-time1)/float(60)
  log.info("Execution took %d minutes." % duration)
