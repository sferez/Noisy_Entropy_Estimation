"""
This script calculates the entropy of a given vocabulary.
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import rpy2.robjects as robjects
from collections import Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import gc
import argparse
import os
import pandas as pd

# ----------------------------------------------- CONSTANTS ----------------------------------------------- #

r = robjects.r
r('library(entropy)')
methods = ['ML', 'MM', 'Laplace', 'CS', 'shrink', 'Jeffreys', 'SG', 'minimax']


# ----------------------------------------------- FUNCTIONS ----------------------------------------------- #

def original_entropy(counts, method):
    r_counts = robjects.IntVector(list(counts.values()))
    r.assign('counts', r_counts)
    r.assign('method', method)
    org_entropy = r('entropy(counts, method=method, unit="log2")')[0]
    del r_counts
    gc.collect()
    return org_entropy


def process_file():
    global vocab
    with open(tokens, 'r') as f:
        all_tokens = f.read().splitlines()  # Assuming each line in vocab.txt is a separate token.
    counts = Counter(all_tokens)
    if vocab:
        print(f'Vocab file provided: {vocab}')
        i = 0
        with open(vocab, 'r') as f:
            vocab = set(f.read().splitlines())
            for token in vocab:
                if token not in counts:
                    i += 1
                    counts[token] = 0
        print(f'Vocab size: {len(vocab)}, Number of OOV tokens: {i}')
    return counts, all_tokens


def bootstrap_analysis(all_tokens, method):
    bootstrap_entropies = []
    n_bootstrap_samples = 100  # adjust this to change the number of bootstrap samples
    for _ in range(n_bootstrap_samples):
        bootstrap_tokens = np.random.choice(all_tokens, size=len(all_tokens), replace=True)
        bootstrap_counts = Counter(bootstrap_tokens)
        if vocab:
            for token in vocab:
                if token not in bootstrap_counts:
                    bootstrap_counts[token] = 0
        r_bootstrap_counts = robjects.IntVector(list(bootstrap_counts.values()))
        r.assign('bootstrap_counts', r_bootstrap_counts)
        r.assign('method', method)
        bootstrap_entropy = r('entropy(bootstrap_counts, method=method, unit="log2")')
        bootstrap_entropies.append(bootstrap_entropy[0])

        del bootstrap_tokens, bootstrap_counts, r_bootstrap_counts, bootstrap_entropy
        gc.collect()
    return bootstrap_entropies


def cal_stats(bootstrap_entropies, org_entropy):
    bootstrap_entropies = np.array(bootstrap_entropies)
    mae = np.mean(np.abs(bootstrap_entropies - org_entropy))
    mse = np.mean((bootstrap_entropies - org_entropy) ** 2)
    sd = np.std(bootstrap_entropies)
    ci = np.percentile(bootstrap_entropies, [2.5, 97.5])  # 95% confidence interval
    return mae, mse, sd, ci


def plot_fig(bootstrap_entropies, org_entropy, method, file, ci):
    sns.set_style('whitegrid')
    sns.set_context('paper')
    plt.figure(figsize=(8, 6))
    sns.displot(bootstrap_entropies, bins=20, color='blue', edgecolor='black', linewidth=1.2, kde=True)
    plt.axvline(x=org_entropy, color='red', linestyle='--', linewidth=2, label='Original Entropy')
    plt.axvline(x=ci[0], color='green', linestyle='--', linewidth=2, label='95% CI')
    plt.axvline(x=ci[1], color='green', linestyle='--', linewidth=2)
    plt.xlabel('Entropy', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title(f'Bootstrap Entropy Distribution ({method})', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{file}/{method}.png')


def gen_results(df, file, result_dir, method, org_entropy, mae, mse, sd, ci):
    df = pd.concat([df, pd.DataFrame([[file, method, org_entropy, mae, mse, sd, ci, f'{result_dir}/{method}.png']],
                                     columns=['file', 'method', 'entropy', 'mae', 'mse', 'sd', 'ci', 'img'])])
    return df


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    file = tokens.split('.')[0]
    os.makedirs(f'results/{os.path.basename(tokens)}', exist_ok=True)
    result_dir = f'results/{os.path.basename(tokens)}'
    counts, all_tokens = process_file()
    df = pd.DataFrame(columns=['file', 'method', 'entropy', 'mae', 'mse', 'sd', 'ci', 'img'])
    for method in tqdm(methods):
        print(f'Method: {method}')
        org_entropy = original_entropy(counts, method)
        bootstrap_entropies = bootstrap_analysis(all_tokens, method)
        mae, mse, sd, ci = cal_stats(bootstrap_entropies, org_entropy)
        print(f'{method}: Entropy: {org_entropy:.3f}, MAE: {mae:.3f}, MSE: {mse:.3f}, SD: {sd:.3f}, 95% CI: {ci}')
        plot_fig(bootstrap_entropies, org_entropy, method, result_dir, ci)
        df = gen_results(df, file, result_dir, method, org_entropy, mae, mse, sd, ci)
    df.to_csv(f'{result_dir}/results.csv', index=False)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str, help='Path to vocabulary file', default=None)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab

    main()