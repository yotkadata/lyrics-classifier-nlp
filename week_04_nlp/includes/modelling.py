"""
Helper functions for modelling.
"""

import time

import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as PipelineIMB
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from settings import conf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB


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

    # initial time
    t_initial = time.time()

    # grid-search cross-validation
    gscv.fit(corpus_, labels_)

    # final time
    t_final = time.time()

    # time taken
    print(f"time taken: {round(t_final-t_initial,2)} sec")

    print(f"Best parameters: {gscv.best_params_}")
    print(f"Best score: {round(gscv.best_score_,6)}")

    return gscv.best_estimator_


def fit_model(model_, corpus_, labels_):
    """
    Function to fit the model and save it.
    """
    # Fit the model with the vectorized data
    print("Fit model")
    trained_model = model_.fit(corpus_, labels_)

    # Check score
    print(f"Score: {model_.score(corpus_, labels_)}")

    # Save trained model
    file_name = "trained_model.pkl"
    joblib.dump(trained_model, conf["base_path"] + file_name)
    print(f"Model saved as {file_name}.")
