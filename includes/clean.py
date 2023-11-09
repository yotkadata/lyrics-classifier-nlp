"""
Helper functions for data cleaning.
"""

import pandas as pd
from settings import conf


def remove_duplicate_urls(song_urls: dict[str, list]) -> dict[str, list]:
    """
    Function to remove duplicate URLs.
    """
    song_urls_clean = {}

    for artist, urls in song_urls.items():
        urls_clean = []
        count_append = 0
        count_remove = 0

        for url in urls:
            end_of_url = "/".join(url.rsplit("/", 2)[1:3])

            # Check if string already exists in list
            if not any(end_of_url in c for c in urls_clean):
                urls_clean.append(url)
                count_append += 1
            else:
                count_remove += 1

        print(
            f"{count_remove} duplicates removed, leaving {count_append} URLs for {artist}."
        )

        song_urls_clean[artist] = urls_clean

    return song_urls_clean


def clean_data(df_: pd.DataFrame) -> pd.DataFrame:
    """
    Function to clean the data.
    """
    # Remove all rows where lyrics cell is empty
    df_ = df_[df_["lyrics"].notna()]
    df_ = df_[df_["lyrics"] != ""]

    # Remove all songs that are not exactly by artists specified
    filters = []
    for artist in conf["artist_urls"]:
        filters.append(df_["artist"].str.lower() == artist.lower())
    filt = [any(sublist) for sublist in zip(*filters)]
    df_ = df_[filt]

    # Remove all rows where title ends with ]
    df_ = df_[df_["title"].str[-1] != "]"]

    return df_
