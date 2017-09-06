'''
gen-vec-subs.py
Reads parallel data, and attempts to substitute similar sentences, using
cosine similarity of rnn language model output vectors.
'''
import argparse, sys, os, time, string
import logging as log

from scipy import spatial
# cosine similarity 1 - spatial.distance.cosine(.,.)

from data import read_sentence_data, read_word_data, write_parallel_data

log.basicConfig(stream=sys.stderr, level=log.DEBUG)

def find_substitutable(lines, sims):
  # TODO

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
      help='Newline delimited sentence file.')
  parser.add_argument('--data_trg', type=str, default='train.trg',
      help='Newline delimited sentence file.')
  parser.add_argument('--data_trg_vecs', type=str, default='train.trg.vec',
      help='Newline delimited sentence file.')
  parser.add_argument('--candidate_vecs', type=str, default='en.mono.vec',
      help='Newline delimited sentence file.')
  parser.add_argument('--out_src', type=str, default='train.src.out',
      help='Output file for the new source side candidate sentences.')
  parser.add_argument('--out_trg', type=str, default='train.trg.out',
      help='Output file for the new target side candidate sentences.')

  args = parser.parse_args()

  lines_src = read_sentence_data(args.data_src)
  # TODO read train.trg.vec and en.mono.vec, for each of the train.trg.vec
  # find the closest K vectors from en.mono.vec, and note the index of the
  # corresponding sentence.
  # then output the original source and the "close" sentence as new parallel
  # data

if __name__ == '__main__':
  time1 = time.time()
  main()
  time2 = time.time()

  duration = (time2-time1)/float(60)
  log.info("Execution took %d minutes." % duration)
