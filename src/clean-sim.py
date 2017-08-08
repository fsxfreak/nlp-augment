'''
clean-sim.py
Removes punctuation and very common words from .sim file.
'''
import argparse, time, sys
import logging as log

from unicodedata import category
from collections import Counter
from data import read_sentence_data

log.basicConfig(stream=sys.stderr, level=log.DEBUG)

def clean(s, common):
  s = s.strip().decode('utf-8')
  s = ''.join(ch for ch in s if category(ch)[0] != 'P')
  if s in common:
    s = ''

  return s

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--sim_in', type=str, default='train.src.rare.sim')
  parser.add_argument('--sim_out', type=str, default='train.src.rare.clean.sim')
  parser.add_argument('--mono', type=str, default='ug.mono')
  parser.add_argument('--num_common', type=int, default=1000)
  args = parser.parse_args()

  lines = read_sentence_data(args.mono)
  flat_lines = [ e for toks in lines for e in toks ]
  count = Counter(flat_lines)
  log.info('Finished building word count.')

  common = count.most_common()[:args.num_common]
  common = [ e[0] for e in common ]
  log.debug('Most common words:\n%s' % common)

  sims = read_sentence_data(args.sim_in, '\t')
  clean_common = lambda s : clean(s, common)
  with open(args.sim_out, 'w') as f:
    for sim in sims:
      clean_sim = [ clean_common(tok).strip().encode('utf-8')
                    for tok in sim ]
      f.write('%s\n' % '\t'.join(clean_sim))


if __name__ == "__main__":
  time1 = time.time()
  main()
  time2 = time.time()

  duration = (time2-time1)/float(60)
  log.info("Execution took %d minutes." % duration)
