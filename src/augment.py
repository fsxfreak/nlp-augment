'''
augment.py
Reads parallel data, and attempts to substitute words for similar rare words,
using word2vec similarity.

Warning, will read all files into memory. Best suited for low-data scenarios.
'''
import argparse, sys, os, time, string
import logging as log

from data import read_sentence_data, read_word_data, write_parallel_data

log.basicConfig(stream=sys.stderr, level=log.DEBUG)

def find_substitutable(lines, sims):
  '''
  find_substitutable
  Find sentences which contain a word in the similarity list to a rare word.

  lines:  list of token lists 
  sims:   list of token lists

  return: substitutions
            a list of tuple of (corr_index, line, [(rare_index, word)])
  '''
  substitutions = [] 
  for x, line in enumerate(lines):
    sim_indices = []
    for i, sim in enumerate(sims):
      # iterate through all sim lists looking for matches
      intersects = set(line).intersection(sim)
      for intersect in intersects:
        if '.' in intersect:
          log.debug('sim: %d, %s' % (i, sim))
          log.debug('\tline: %s' % line)
          log.debug('\tintersects: %s' % intersects)
          log.debug('\tline num: %d' % (x + 1))
        sim_indices.append((i, intersect))
    if len(sim_indices) > 0:
      substitutions.append((x, line, sim_indices))
      if len(substitutions) % 5000 == 0:
        log.debug('Found %d potential substitutions.' % len(substitutions))

  log.debug(substitutions[:5])
  log.info('Finished finding sentences for potential substitutions.')
  return substitutions

def build_augments(subs, rares, corresponding_lines, src=True):
  '''
  build_augments: takes a list of lines and the words to be substituted in them,
                  and substitutes in the corresponding rare word

  subs:           a list of tuple (corr_index, line, replaces), where line is 
                  the original, corr_index its parallel correspondence, and 
                  replaces a list of (rare_index, words) that should be
                  replaced in that line with the rare_index'd word
  '''
  augments = []
  for corr_index, line, replaces in subs:
    for rare_index, replace in replaces:
      line_index = line.index(replace)
      line_copy = list(line)

      line_copy[line_index] = rares[rare_index]
      if src:
        augments.append((line_copy, corresponding_lines[corr_index]))
      else:
        augments.append((corresponding_lines[corr_index], line_copy))
  log.debug("Sample old line: %s\t, new line:%s" % (line, line_copy))
  return augments

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_src', type=str, default='train.src',
      help='Newline delimited sentence file for source language.')
  parser.add_argument('--data_trg', type=str, default='train.trg',
      help='Newline delimited sentence file for target language.')
  parser.add_argument('--rare_src', type=str, default='train.src.rare',
      help='Newline delimited word file of rare words in source lang.')
  parser.add_argument('--rare_trg', type=str, default='train.trg.rare',
      help='Newline delimited word file of rare words in target lang.')
  parser.add_argument('--sim_src', type=str, default='train.src.rare.sim',
      help='Newline delimited words file of similar to rare in source lang.')
  parser.add_argument('--sim_trg', type=str, default='train.trg.rare.sim',
      help='Newline delimited words file of similar to rare in target lang.')
  parser.add_argument('--out_src', type=str, default='train.src.aug',
      help='Output file for the new sentences on the source side.')
  parser.add_argument('--out_trg', type=str, default='train.trg.aug',
      help='Output file for the new sentences on the target side.')

  args = parser.parse_args()

  lines_src = read_sentence_data(args.data_src)
  sims_src = read_sentence_data(args.sim_src, '\t')
  log.debug('Sims data; %s' % sims_src[:2])

  subs_src = find_substitutable(lines_src, sims_src)
  rares_src = read_word_data(args.rare_src)

  lines_trg = read_sentence_data(args.data_trg)
  sims_trg = read_sentence_data(args.sim_trg, '\t')
  log.debug('Sims data; %s' % sims_trg[:2])

  subs_trg = find_substitutable(lines_trg, sims_trg)
  rares_trg = read_word_data(args.rare_trg)

  augments = []
  augments_src = build_augments(subs_src, rares_src, lines_trg)
  log.debug('New augment data; %s' % augments_src[:3])
  augments.extend(augments_src)

  # uncomment to build augmentations including the target side
  #augments_trg = build_augments(subs_trg, rares_trg, lines_src, src=False)
  #log.debug('New augment data; %s' % augments_trg[:3])
  #augments.extend(augments_trg)

  write_parallel_data(args.out_src, args.out_trg, augments)

  # TODO make sure the src and target make sense translated together?
  # additional processing

if __name__ == '__main__':
  time1 = time.time()
  main()
  time2 = time.time()

  duration = (time2-time1)/float(60)
  log.info("Execution took %d minutes." % duration)
