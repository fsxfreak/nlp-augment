import logging as log

'''
data.py
Utilities for reading from corpuses or word files.
'''
def read_sentence_data(filename, token_delim=' '):
  '''
  read_data:  reads data from a line-delimited sentence file.

  filename:   path to file
  return:     list of lists, each list in the list being a list of
              tokens for a sentence.
  '''

  lines = []
  with open(filename, 'r') as f:
    for line in f:
      line = line.strip()
      toks = line.split(token_delim)

      # remove all none-like tokens
      toks = list(filter(None, toks))

      lines.append(toks)

  log.debug('Finished reading %s.' % filename)
  return lines

def read_word_data(filename):
  '''
  read_word_data:  reads data from a line-delimited word file.

  filename:   path to file
  return:     list of strings
  '''

  lines = []
  with open(filename, 'r') as f:
    for line in f:
      line = line.strip()
      lines.append(line)

  log.debug('Finished reading %s.' % filename)
  return lines

def write_sentence_data(filename, lines):
  '''
  write_sentence_data:  writes data, each item newline delimited

  filename: path to file
  lines:    list of list of tokens

  return:   True on success
  '''
  with open(filename, 'w') as f:
    for line in lines:
      s = ' '.join(line).strip()
      f.write('%s\n' % s)

  log.debug('Finished writing to %s.' % filename)
  return True

def write_parallel_data(file_src, file_trg, lines_src_trg):
  '''
  write_parallel_data:  writes paired data to newline delimited file

  file_src:             path to output src file
  file_trg:             path to output trg file
  lines_src_trg:        list of tuple of (tok list, tok list)

  return:               True on success
  '''

  with open(file_src, 'w') as f_src:
    with open(file_trg, 'w') as f_trg:
      for src, trg in lines_src_trg:
        s_src = ' '.join(src).strip()
        s_trg = ' '.join(trg).strip()

        f_src.write('%s\n' % s_src)
        f_trg.write('%s\n' % s_trg)

  log.debug('Finished writing to %s and %s.' % (file_src, file_trg))
  return True

