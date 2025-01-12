"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Tokenize a Twitter CSV file.

CLI Arguments:
    - --input, --i: Directory or CSV File
    - --ngrams, --n: Generate n-grams (default: 1)
    - --chars, --c: Use characters instead of words (default: False)

Examples:
    >>> python tokenize_tweets.py --input data
    >>> python tokenize_tweets.py --input data --ngrams 2
    >>> python tokenize_tweets.py --input data --ngrams 2 --chars
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import argparse
import os
from nltk.tokenize import TweetTokenizer
import pandas as pd
from tqdm import tqdm
from itertools import chain
from nltk.util import ngrams
import subprocess
import csv

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

CHUNKSIZE = 100000


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def generate_ngrams(tokens, n):
    """
    Generate n-grams from a list of tokens.

    :param tokens: list of tokens
    :type tokens: list
    :param n: n-gram
    :type n: int
    :return: list of n-grams
    :rtype: list

    >>> generate_ngrams(['I', 'am', 'so', 'happy'], 2)
    >>> ['I am', 'am so', 'so happy']
    """
    n_grams = ngrams(tokens, n)
    return [" ".join(gram) for gram in n_grams]


def process_file(fp):
    """
    Process a Twitter CSV file.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    print(f'Tokenizing {fp}...')
    df = pd.read_csv(fp)
    df = df.dropna(subset=['text'])
    df['text'] = df['text'].astype(str)
    tqdm.pandas()
    if not chars:
        df['tokens'] = df['text'].progress_apply(lambda x: tweet_tokenizer.tokenize(x))
    else:
        df['tokens'] = df['text'].progress_apply(lambda x: list(x))
    if ngrams_ > 1:
        df['tokens'] = df['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
    all_tokens = list(chain.from_iterable(df['tokens']))
    csv_writer = csv.writer(
        open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}_ppm.txt'), 'w'))
    for tokens in df["tokens"]:
        csv_writer.writerow(tokens)
    with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for tokens in all_tokens:
            f.write(f'{tokens}\n')
    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for token in set(all_tokens):
            f.write(f'{token}\n')
        f.close()

    print(f'Tokenized {fp}.'
          f'\n\tVocab: {fp.replace(".csv", f"_vocab_{ngrams_}-gram.txt")}'
          f'\n\tTokens: {fp.replace(".csv", f"_tokens_{ngrams_}-gram.txt")}')


def process_file_chunk(fp, num_lines):
    """
    Process a Twitter CSV file by chunks.

    :param fp: file path
    :type fp: str
    :param num_lines: number of lines
    :type num_lines: int
    :return: None
    :rtype: None

    >>> process_file_chunk('data.csv', 100_000)
    """
    vocab = set()
    print('Processing in chunks...')
    csv_writer = csv.writer(
        open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}_ppm.txt'), 'w'))
    for i, df in tqdm(enumerate(pd.read_csv(fp, chunksize=CHUNKSIZE)), total=num_lines // CHUNKSIZE + 1):
        df = df.dropna(subset=['text'])
        df_ = df.copy()
        df_['text'] = df_['text'].astype(str)
        if not chars:
            df_['tokens'] = df_['text'].apply(lambda x: tweet_tokenizer.tokenize(x))
        else:
            df_['tokens'] = df_['text'].apply(lambda x: list(x))
        if ngrams_ > 1:
            df_['tokens'] = df_['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
        all_tokens = list(chain.from_iterable(df_['tokens']))

        mode = 'a' if i != 0 else 'w'

        for tokens in df_["tokens"]:
            csv_writer.writerow(tokens)

        with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}.txt'), mode) as f:
            for token in all_tokens:
                f.write(f'{token}\n')

        vocab.update(all_tokens)

    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for token in vocab:
            f.write(f'{token}\n')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function of the tokenize_tweets.py script.

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Tokenizing data with {ngrams_}-grams tokens...')

    if os.path.isfile(input_):
        num_lines = int(subprocess.check_output(f"wc -l {input_}", shell=True).split()[0]) - 1
        if num_lines > CHUNKSIZE:
            process_file_chunk(input_, num_lines)
        else:
            process_file(input_)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    fp = os.path.join(root, file)
                    num_lines = int(subprocess.check_output(f"wc -l {fp}", shell=True).split()[0]) - 1
                    if num_lines > CHUNKSIZE:
                        process_file_chunk(fp, num_lines)
                    else:
                        process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of the tokenize_tweets.py script.
    
    Args:
        --input, --i: Directory or CSV File
        --ngrams, --n: Generate n-grams (default: 1)
        --chars, --c: Use characters instead of words (default: False)
        
    Examples:
        >>> python tokenize_tweets.py --input data
        >>> python tokenize_tweets.py --input data --ngrams 2
        >>> python tokenize_tweets.py --input data --ngrams 2 --chars
    """
    parser = argparse.ArgumentParser(description='Perform tokenization on the raw linguistic data.')
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV file', required=True)
    parser.add_argument('--ngrams', '--n', type=int, help='Generate n-grams', default=1)
    parser.add_argument('--chars', '--c', action=argparse.BooleanOptionalAction, help='Use characters instead of words',
                        default=False)

    args = parser.parse_args()

    input_ = args.input
    ngrams_ = args.ngrams
    chars = args.chars

    tweet_tokenizer = TweetTokenizer()

    main()
