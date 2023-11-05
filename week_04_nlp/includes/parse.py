"""
Helper functions for parsing.
"""
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from includes import clean, misc
from settings import conf


def get_song_urls(artist_urls: dict[str, str]) -> dict[str, list]:
    """
    Function to get song URLs from HTML files.
    """

    song_urls = {}

    for artist in artist_urls:
        file_name = f"{misc.shorten_artist(artist)}_full_song_list.html"
        count = 0

        with open(
            conf["base_path"] + conf["scrape_path"] + file_name, "r", encoding="utf-8"
        ) as file:
            html = file.read()

            soup = BeautifulSoup(html, "html.parser")

            parsed_urls = []

            for row in soup.find("table", class_="tdata").find_all("tr"):  # type: ignore
                try:
                    # Get URL from href
                    url = row.find("td").find("a", href=True)["href"]
                except Exception:
                    continue

                # Append to list
                parsed_urls.append("https://www.lyrics.com" + url)
                count += 1

        song_urls[artist] = parsed_urls
        print(f"Added {count} URLs for artist {artist}.")

    # Remove duplicate URLS
    song_urls_clean = clean.remove_duplicate_urls(song_urls)

    return song_urls_clean


def parse_html(html: str, source: str = "") -> tuple[str, str, str]:
    """
    Function to parse HTML and extract title, artist and lyrics
    """

    title, artist, lyrics = "", "", ""

    soup = BeautifulSoup(html, "html.parser")

    # Extract title, artits, and lyrics
    try:
        title = soup.h1.text.strip()  # type: ignore
    except Exception:
        print(f"Unable to parse title at {source}.")

    try:
        artist = soup.find("h3", class_="lyric-artist").text.strip()  # type: ignore
    except Exception:
        print(f"Unable to parse artist at {source}.")

    try:
        lyrics = soup.find(id="lyric-body-text").text.strip()  # type: ignore
    except Exception:
        print(f"Unable to parse lyrics at {source}.")

    return title, artist, lyrics


def get_lyrics_from_file(path_html: str) -> tuple[str, str, str]:
    """
    Function to scrape one single song lyric from html file
    """

    with open(path_html, "r", encoding="utf-8") as file:
        html = file.read()

    title, artist, lyrics = parse_html(html, path_html)

    return title, artist, lyrics


def get_lyrics_from_url(url: str) -> tuple[str, str, str]:
    """
    Function to scrape one single song lyric from URL
    """

    title, artist, lyrics = "", "", ""

    response = requests.get(url, conf["header"], allow_redirects=False, timeout=30)

    if response.status_code == 200:
        title, artist, lyrics = parse_html(response.text, url)
    else:
        print(f"Error: Response code {response.status_code} for URL {url}.")

    return title, artist, lyrics


def get_files_to_parse(artists: list[str]) -> dict:
    """
    Function to get file names in the scrape directory.
    """

    all_files = {}

    for artist in artists:
        # Directory holding HTML files
        path_html_files = (
            conf["base_path"] + conf["scrape_path"] + "/" + misc.shorten_artist(artist)
        )

        all_files[artist] = [
            f
            for f in os.listdir(path_html_files)
            if os.path.isfile(os.path.join(path_html_files, f)) and f.endswith(".html")
        ]

    return all_files


def parse_lyrics_from_files(artist_urls: dict[str, str]) -> pd.DataFrame:
    """
    Function to parse lyrics from existing files.
    """

    # Create empty DataFrame
    songs = pd.DataFrame(columns=["title", "artist", "lyrics"])

    # Get file names
    files_to_parse = get_files_to_parse(list(artist_urls.keys()))

    # Loop through file names and parse HTML
    for artist, files in files_to_parse.items():
        for file in files:
            path_html_file = (
                conf["base_path"]
                + conf["scrape_path"]
                + misc.shorten_artist(artist)
                + "/"
                + file
            )
            title_, artist_, lyrics_ = get_lyrics_from_file(path_html_file)
            songs.loc[len(songs)] = [title_, artist_, lyrics_]  # type: ignore

    # Clean data
    songs_clean = clean.clean_data(songs)

    # Save DataFrame to CSV
    file_name_csv_clean = "songs_clean.csv"
    songs_clean.to_csv(conf["base_path"] + "data/" + file_name_csv_clean)

    print(f"Saved {len(songs_clean)} songs to {file_name_csv_clean}")

    return songs_clean
