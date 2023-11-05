"""
A Python Script to predict the artist of a song line
"""

import pandas as pd
from includes import misc, modelling, parse, scrape
from settings import conf


def main():
    """
    Main function
    """
    if conf["scrape_song_list"]:
        # Scrape HTML files containing URLs to song lyrics
        scrape.scrape_artist_song_list(conf["artist_urls"])

    if conf["scrape_songs"]:
        # Scrape lyric files from URLs
        scrape.scrape_songs_to_files(conf["artist_urls"])

    if conf["parse_html"]:
        # Parse lyrics from file and save them in a CSV file
        songs = parse.parse_lyrics_from_files(conf["artist_urls"])

        # Convert lyrics to lines
        misc.convert_lyrics_to_lines(songs)

    # Import CSV file with lyrics
    df_corpus = pd.read_csv(
        conf["base_path"] + "data/" + "songs_by_line.csv", index_col=0
    )

    # Create wordclouds
    if conf["create_wordclouds"]:
        corpus = " ".join(df_corpus[df_corpus["artist"] == "Eels"]["lyrics"])
        misc.plot_wordcloud(corpus, name="Eels", shape="circle")

        corpus = " ".join(
            df_corpus[df_corpus["artist"] == "Rage Against the Machine"]["lyrics"]
        )
        misc.plot_wordcloud(corpus, name="ratm", shape="text")

        corpus = " ".join(df_corpus[df_corpus["artist"] == "Adele"]["lyrics"])
        misc.plot_wordcloud(corpus, name="Adele", shape="circle")

    if conf["train_model"]:
        # Prepare corpus and labels
        corpus, labels = modelling.prepare_corpus(df_corpus)

        # Preprocess data
        corpus_clean = modelling.preprocess_corpus(corpus)
        assert len(corpus_clean) == len(corpus_clean)

        model = modelling.tune_hyperparameters(corpus_clean, labels)

        # Fit the model with the vectorized data
        modelling.fit_model(model, corpus_clean, labels)


if __name__ == "__main__":
    main()
