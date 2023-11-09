"""
Python script to predict the artist of a song based on its lyrics.
"""

import joblib
from includes import modelling
from settings import conf


def main():
    """
    Main function
    """

    keep_asking = True

    # Load model
    file_name = "trained_model.pkl"
    model = joblib.load(conf["base_path"] + file_name)

    while keep_asking:
        print(
            "Enter a line from a song by the Eels, Adele, or Rage Against the Machine"
        )
        print("Write 'exit' to quit.\n")

        # Get user input
        user_input = input()

        if user_input in ["quit", "q", "exit"]:
            keep_asking = False
            continue

        lyrics = [user_input]

        # Preprocess
        lyrics_clean = modelling.preprocess_corpus(lyrics)

        # Get results
        predictions = model.predict(lyrics_clean)
        probabilities = [p.max() for p in model.predict_proba(lyrics_clean)]

        # Print results
        modelling.print_results(lyrics, predictions, probabilities)
        print("\n")


if __name__ == "__main__":
    main()
