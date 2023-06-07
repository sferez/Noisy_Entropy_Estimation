"""
Sentiment NLP detection
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from tqdm import tqdm
import tweetnlp


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def detect_sentiment(text):
    topic = model.predict(text)

    if topic['label'] == 'positive':
        return 1
    elif topic['label'] == 'negative':
        return -1
    else:
        return 0


def process_file(fp):
    df = pd.read_csv(fp)

    if 'sentiment' in df.columns and not force:
        if df['sentiment'].isnull().sum() == 0:
            print('Already detected')
            return

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    tqdm.pandas()
    df['sentiment'] = df['text'].progress_apply(detect_sentiment)

    df.to_csv(fp, index=False)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    print(f'Sentiment detection on {input_}...')

    if os.path.isfile(input_):  # Single file
        fp = input_
        process_file(fp)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply NLP Sentiment detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()
    input_ = args.input
    force = args.force

    model = tweetnlp.Sentiment(multilingual=True)

    main()
