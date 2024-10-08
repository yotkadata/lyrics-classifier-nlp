"""
Helper functions for modelling.
"""

import time
from pathlib import Path

import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as PipelineIMB
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB

from includes.misc import download_nltk_data
from settings import conf


def prepare_corpus(df_c: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Function to prepare the corpus from a dataframe.
    """

    corpus = []
    labels = []

    # Create list of song lines and labels
    for artist in df_c["artist"].unique():
        song_lines = df_c[df_c["artist"] == artist]["lyrics"]

        for line in song_lines:
            corpus.append(line)

        for _ in range(len(song_lines)):
            labels.append(artist)

    return corpus, labels


def preprocess_corpus(corpus_: list[str]) -> list[str]:
    """
    Function to preprocess the data for the model.
    """

    # Convert to lowercase
    corpus_ = [s.lower().strip() for s in corpus_]

    # Tokenize and lemmatize
    corpus_clean = []

    tokenizer = TreebankWordTokenizer()
    lemmatizer = WordNetLemmatizer()

    for doc in corpus_:
        tokens = tokenizer.tokenize(text=doc)
        clean_doc = " ".join(lemmatizer.lemmatize(token) for token in tokens)
        corpus_clean.append(clean_doc)

    return corpus_clean


def print_results(
    lyrics: list[str], predictions: list[str], probabilities: list[float]
) -> None:
    """
    Function to print the results of a prediction.
    """
    prob_phrases = []
    for prob in probabilities:
        if prob < 0.6:
            prob_phrases.append("I guess")
        elif prob < 0.75:
            prob_phrases.append("I believe")
        elif prob < 0.9:
            prob_phrases.append("I am pretty sure")
        else:
            prob_phrases.append("I am positive")

    for lyric, pred, prob, phrase in zip(
        lyrics, predictions, probabilities, prob_phrases
    ):
        print(
            f"Line: {lyric}\n{phrase} that line is from a {pred} song ({prob:.0%} sure)\n"
        )


def tune_hyperparameters(corpus_: list[str], labels_: list[str]):
    """
    Function to tune the model's hyperparameters.
    """

    # Make sure necessary NLTK files have been downloaded
    download_nltk_data("wordnet")
    download_nltk_data("stopwords")

    model = PipelineIMB(
        steps=[
            ("tdidf", TfidfVectorizer(stop_words=list(stopwords.words("english")))),
            ("smote", SMOTE()),
            ("nb", MultinomialNB()),
        ]
    )

    param_grid = {
        "nb__alpha": [0.1, 0.5, 1, 2, 3],
        "nb__fit_prior": [True, False],
        "tdidf__ngram_range": [(1, 1), (1, 2), (1, 3)],
    }

    gscv = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring="accuracy",
        cv=5,
        n_jobs=-1,
        verbose=1,
    )

    time_initial = time.time()

    # Grid Search cross-validation
    gscv.fit(corpus_, labels_)

    time_final = time.time()

    print(f"time taken: {round(time_final-time_initial, 2)} sec")

    print(f"Best parameters: {gscv.best_params_}")
    print(
        f"Best cross-validation score during Grid Search: {round(gscv.best_score_, 6)}"
    )

    # Score on the entire dataset using the best estimator
    best_estimator = gscv.best_estimator_
    score_on_entire_dataset = best_estimator.score(corpus_, labels_)
    print(f"Score on the entire dataset: {round(score_on_entire_dataset, 6)}")

    # Save model
    dir_path = conf["base_path"] + "models/"
    file_name = "trained_model.pkl"
    save_model(best_estimator, dir_path, file_name)

    return best_estimator


def save_model(trained_model, dir_path: str, file_name: str) -> None:
    """
    Function to save a model to a file.
    """
    # Use Path to create directories if they don't exist
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    joblib.dump(trained_model, dir_path + file_name)
    print(f"Model saved as {dir_path + file_name}.")


def load_model(dir_path: str, file_name: str):
    """
    Function to load a model from a file.
    """
    return joblib.load(dir_path + file_name)
