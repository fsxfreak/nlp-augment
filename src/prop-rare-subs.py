'''
prop-rare-subs.py
Proposes sentences with a rare word augmented for later scoring by forwards
and backwards language models.

Unsuitable for practical use. Combinatorial explosion on the order of L * K * N,
where L is the average length of a sentence, K is the number of rare words, and
N is the number of sentences in the original parallel corpus.
'''

import argparse, sys, os, time, string
import logging as log

import argparse
import numpy as np

import reader
from data import read_sentence_data, read_word_data

log.basicConfig(stream=sys.stderr, level=log.INFO,
    format='%(asctime)s [%(levelname)s]:%(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S')                        

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--rare_src', default='../data/rare.txt', 
      type=str,
      help='List of source words deemed as rare in the parallel training data.')
  parser.add_argument('--train_src', default='../data/train.src', 
      type=str,
      help='Original training data source.')
  parser.add_argument('--out_fwd', default='../data/train.src.fwd.rare-aug', 
      type=str,
      help='Outputs index of original sentence <tab> proposed augmentation.')
  parser.add_argument('--out_rev', default='../data/train.src.rev.rare-aug', 
      type=str,
      help='Outputs index of original sentence <tab> reversed augmentation.')
  args = parser.parse_args()

  lines = read_sentence_data(args.train_src)
  rares = read_word_data(args.rare_src)

  out_fwds = open(args.out_fwd, 'w')
  out_revs = open(args.out_rev, 'w')
  log.info('Writing to %s and %s.' % (args.out_fwd, args.out_rev))

  for i, line in enumerate(lines):
    for rare in rares:
      for index in range(len(line) - 1): # don't substitute the end punctuation
        output_raw = line[:]
        output_raw[index] = rare
        out_fwd = ' '.join(output_raw).strip()
        output_raw.reverse()
        out_rev = ' '.join(output_raw).strip()

        out_fwds.write('%d\t%s\n' % (i, out_fwd))
        out_revs.write('%d\t%s\n' % (i, out_rev))
    if i % 10000 == 0:
      log.info('Processed line %d.' % i)

if __name__ == '__main__':
  time1 = time.time()
  main()
  time2 = time.time()

  duration = (time2-time1)/float(60)
  log.info("Execution took %d minutes." % duration)
