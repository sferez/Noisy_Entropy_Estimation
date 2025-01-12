"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Tokenize a Programming Language CSV file.

CLI Arguments:
    - --input, --i: CSV file or directory
    - --char, --c: Character-level tokenization (default: False)
    - --ngrams, --n: Generate n-grams (default: 1)

Examples:
    >>> python tokenize_code.py --input data.csv
    >>> python tokenize_code.py --input data.csv --char
    >>> python tokenize_code.py --input data.csv --ngrams 3
    >>> python tokenize_code.py --input data.csv --char --ngrams 3
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
from ast import literal_eval
from itertools import chain
import pandas as pd
from tqdm import tqdm
import argparse
import os
import subprocess
from nltk.util import ngrams
import csv

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

CHUNKSIZE = 100000
vocab = set()


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def generate_ngrams(tokens, n):
    """
    Generate n-grams from a list of tokens.

    :param tokens: list of tokens
    :type tokens: list
    :param n: n-gram size
    :type n: int
    :return: list of n-grams
    :rtype: list

    >>> generate_ngrams(['def', 'main', '(', ')', ':', 'return', '0'], 3)
    >>> ['def main (', 'main ( )', '( ) :', ') : return', ': return 0']
    """
    n_grams = ngrams(tokens, n)
    return [" ".join(gram) for gram in n_grams]


def process_file(fp):
    """
    Process a CSV file and generate tokens and vocab files.

    :param fp: CSV file
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    print('Processing...')
    df = pd.read_csv(fp)
    df['tokens'] = df['tokens'].apply(lambda x: literal_eval(x))
    if ngrams_ > 1:
        df['tokens'] = df['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
    tokens = list(chain.from_iterable(df['tokens']))

    csv_writer = csv.writer(
        open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}_ppm.txt'), 'w'))
    if not char:
        for t in df["tokens"]:
            csv_writer.writerow(t)
    else:
        for t in df["tokens"]:
            csv_writer.writerow(''.join(t))
    with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}.txt'), 'w') as f:
        if not char:
            for token in tokens:
                f.write(f'{token}\n')
        else:
            for c in ''.join(tokens):
                f.write(f'{c}\n')
    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if char else ""}.txt'), 'w') as f:
        if not char:
            for token in set(tokens):
                f.write(f'{token}\n')
        else:
            for c in set(''.join(tokens)):
                f.write(f'{c}\n')


def process_file_chunk(fp, num_lines):
    """
    Process a CSV file by chunks and generate tokens and vocab files.

    :param fp: CSV file
    :type fp: str
    :param num_lines: number of lines
    :type num_lines: int
    :return: None
    :rtype: None

    >>> process_file_chunk('data.csv', 100_000)
    """
    print('Processing in chunks...')
    csv_writer = csv.writer(
        open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}_ppm.txt'), 'w'))
    for i, df in tqdm(enumerate(pd.read_csv(fp, chunksize=CHUNKSIZE)),
                      total=num_lines // CHUNKSIZE + 1):
        df['tokens'] = df['tokens'].apply(lambda x: literal_eval(x))
        if ngrams_ > 1:
            df['tokens'] = df['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
        tokens = list(chain.from_iterable(df['tokens']))

        mode = 'a' if i != 0 else 'w'

        if not char:
            for t in df["tokens"]:
                csv_writer.writerow(t)
        else:
            for t in df["tokens"]:
                csv_writer.writerow(''.join(t))
        with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}.txt'), mode) as f:
            if not char:
                for token in tokens:
                    f.write(f'{token}\n')
            else:
                for c in ''.join(tokens):
                    f.write(f'{c}\n')

        vocab.update(tokens)

    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if char else ""}.txt'), 'w') as f:
        for token in vocab:
            f.write(f'{token}\n')


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    """
    Main function of the tokenize_code.py script.

    :return: None
    :rtype: None

    >>> main()
    """
    if os.path.isfile(input_):  # Single file
        num_lines = int(subprocess.check_output(f"wc -l {input_}", shell=True).split()[0]) - 1
        if num_lines > CHUNKSIZE:
            process_file_chunk(input_, num_lines)
        else:
            process_file(input_)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    num_lines = int(subprocess.check_output(f"wc -l {input_}", shell=True).split()[0]) - 1
                    if num_lines > CHUNKSIZE:
                        process_file_chunk(input_, num_lines)
                    else:
                        process_file(input_)


if __name__ == '__main__':
    """
    Command Line Interface of the tokenize_code.py script.
    
    Args:
        --input, --i: CSV file or directory
        --char, --c: Character-level tokenization (default: False)
        --ngrams, --n: Generate n-grams (default: 1)
        
    Examples:
        >>> python tokenize_code.py --input data.csv
        >>> python tokenize_code.py --input data.csv --char
        >>> python tokenize_code.py --input data.csv --ngrams 3
        >>> python tokenize_code.py --input data.csv --char --ngrams 3
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--char', '--c', action=argparse.BooleanOptionalAction, help='Character-level tokenization',
                        default=False)
    parser.add_argument('--ngrams', '--n', type=int, help='Generate n-grams', default=1)

    args = parser.parse_args()
    input_ = args.input
    char = args.char
    ngrams_ = args.ngrams

    main()
