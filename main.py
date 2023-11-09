"""
A Python Script to predict the artist of a song line
"""

import os
import sys

import pandas as pd
from includes import misc, modelling, parse, scrape
from settings import conf


def main():
    """
    Main function
    """
    if conf["scrape_song_list"]:
        print("Scraping HTML files containing URLs to song lyrics")
        scrape.scrape_artist_song_list(conf["artist_urls"])
    else:
        print("Skip scraping HTML files containing URLs to song lyrics")

    if conf["scrape_songs"]:
        print("Scraping lyric files from URLs")
        scrape.scrape_songs_to_files(conf["artist_urls"])
    else:
        print("Skip scraping lyric files from URLs")

    if conf["parse_html"]:
        print("Parsing lyrics from file and save them in a CSV file")
        songs = parse.parse_lyrics_from_files(conf["artist_urls"])

        if isinstance(songs, pd.DataFrame):
            print("Converting lyrics to lines")
            misc.convert_lyrics_to_lines(songs)
        else:
            print("Error: Parsing result has no data.")
            sys.exit(1)
    else:
        print("Skip parsing lyrics from file and save them in a CSV file")

    file_songs_by_line = conf["base_path"] + "data/" + "songs_by_line.csv"
    if os.path.isfile(file_songs_by_line):
        print("Importing CSV file with lyrics")
        df_corpus = pd.read_csv(file_songs_by_line, index_col=0)
    else:
        print(f"Error: File not found. ({file_songs_by_line})")
        sys.exit(1)

    if conf["create_wordclouds"]:
        print("Creating wordclouds")
        corpus = " ".join(df_corpus[df_corpus["artist"] == "Eels"]["lyrics"])
        misc.plot_wordcloud(corpus, name="Eels", shape="circle")

        corpus = " ".join(
            df_corpus[df_corpus["artist"] == "Rage Against the Machine"]["lyrics"]
        )
        misc.plot_wordcloud(corpus, name="ratm", shape="text")

        corpus = " ".join(df_corpus[df_corpus["artist"] == "Adele"]["lyrics"])
        misc.plot_wordcloud(corpus, name="Adele", shape="circle")
    else:
        print("Skip creating wordclouds")

    if conf["train_model"]:
        print("Train model")
        print("Prepare corpus and labels")
        corpus, labels = modelling.prepare_corpus(df_corpus)

        print("Preprocess data")
        corpus_clean = modelling.preprocess_corpus(corpus)
        assert len(corpus_clean) == len(corpus_clean)

        # Tune hyperparameters and save fitted model to file
        modelling.tune_hyperparameters(corpus_clean, labels)
    else:
        print("Skip training model")

    print("Done. Run predict.py to predict the artist of a song line.")


if __name__ == "__main__":
    main()
