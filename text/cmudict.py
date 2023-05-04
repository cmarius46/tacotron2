""" from https://github.com/keithito/tacotron """

import re


# valid_symbols = [
#   'AA', 'AA0', 'AA1', 'AA2', 'AE', 'AE0', 'AE1', 'AE2', 'AH', 'AH0', 'AH1', 'AH2',
#   'AO', 'AO0', 'AO1', 'AO2', 'AW', 'AW0', 'AW1', 'AW2', 'AY', 'AY0', 'AY1', 'AY2',
#   'B', 'CH', 'D', 'DH', 'EH', 'EH0', 'EH1', 'EH2', 'ER', 'ER0', 'ER1', 'ER2', 'EY',
#   'EY0', 'EY1', 'EY2', 'F', 'G', 'HH', 'IH', 'IH0', 'IH1', 'IH2', 'IY', 'IY0', 'IY1',
#   'IY2', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OW0', 'OW1', 'OW2', 'OY', 'OY0',
#   'OY1', 'OY2', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UH0', 'UH1', 'UH2', 'UW',
#   'UW0', 'UW1', 'UW2', 'V', 'W', 'Y', 'Z', 'ZH'
# ]

valid_symbols_RO = [
  'sh', 'ij', 'k', '@', 'zh', 'a', 'n', 'd', 'r', 'm', 'u', 'l', 'i', 't', 'a@', 'e', 'j', 
  'h', 'o', 'dz', 'p', 'ch', 'g', 'v', 's', 'z', 'g.z', 'ts', '-', 'f', 'e@', 'k.s', 'w', 'b', 
  'o@', 'j.e'
]

# apparently it has to be the same length as the english one

valid_symbols = [
    'sh', 'ij', 'k', '@', 'zh', 'a', 'n', 'd', 'r', 'm', 'u', 'l', 'i', 't', 'a@', 'e', 'j',
    'h', 'o', 'dz', 'p',   'ch', 'g', 'v', 's', 'z', 'g.z', 'ts', '-', 'f', 'e@', 'k.s', 'w', 
    'b', 'o@', 'j.e', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', 
    '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',   '60', '61', '62', '63', 
    '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78',   
    '79', '80', '81', '82', '83', '84']
# ! make sure it's the same length as the english one = 84


_valid_symbol_set = set(valid_symbols)


class CMUDict:
  '''Thin wrapper around CMUDict data. http://www.speech.cs.cmu.edu/cgi-bin/cmudict'''
  def __init__(self, file_or_path, keep_ambiguous=True):
    if isinstance(file_or_path, str):
      with open(file_or_path, encoding='latin-1') as f:
        entries = _parse_cmudict(f)
    else:
      entries = _parse_cmudict(file_or_path)
    if not keep_ambiguous:
      entries = {word: pron for word, pron in entries.items() if len(pron) == 1}
    self._entries = entries


  def __len__(self):
    return len(self._entries)


  def lookup(self, word):
    '''Returns list of ARPAbet pronunciations of the given word.'''
    return self._entries.get(word.upper())



_alt_re = re.compile(r'\([0-9]+\)')


def _parse_cmudict(file):
  cmudict = {}
  for line in file:
    if len(line) and (line[0] >= 'A' and line[0] <= 'Z' or line[0] == "'"):
      parts = line.split('  ')
      word = re.sub(_alt_re, '', parts[0])
      pronunciation = _get_pronunciation(parts[1])
      if pronunciation:
        if word in cmudict:
          cmudict[word].append(pronunciation)
        else:
          cmudict[word] = [pronunciation]
  return cmudict


def _get_pronunciation(s):
  # verifies that s is comprised of sounds that are in _valid_symbol_set

  parts = s.strip().split(' ')
  for part in parts:
    if part not in _valid_symbol_set:
      return None
  return ' '.join(parts)
