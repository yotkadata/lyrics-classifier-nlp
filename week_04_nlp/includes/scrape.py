"""
Helper functions for scraping.
"""
import os
import time

import requests
from includes import misc, parse
from settings import conf


def scrape_artist_song_list(artist_urls: dict[str, str]) -> None:
    """
    Function to scrape song list from a website and save them as files.
    """

    for artist, url in artist_urls.items():
        # Create directory for scraped files if it doesn't exist
        if not os.path.exists(conf["base_path"] + conf["scrape_path"]):
            os.makedirs(conf["base_path"] + conf["scrape_path"])

        file_name = f"{misc.shorten_artist(artist)}_full_song_list.html"

        # Do nothing if file exists already
        if os.path.isfile(
            os.path.join(conf["base_path"], conf["scrape_path"], file_name)
        ):
            print(f"Skipped existing file {file_name}.")
            continue

        # If file does not exist, fetch it
        response = requests.get(url, conf["header"], allow_redirects=False, timeout=30)

        if response.status_code == 200:
            with open(
                conf["base_path"] + conf["scrape_path"] + file_name,
                "w",
                encoding="utf-8",
            ) as file:
                file.write(response.text)

            print(
                f"Song list for {artist} written to file {conf['scrape_path']}{file_name}"
            )

        else:
            print(f"Error: Response code {response.status_code} for URL {url}.")

        time.sleep(conf["sleep_sec"])


def scrape_songs_to_files(artist_urls: dict[str, str]) -> None:
    """
    Function to scrape songs and save them locally.
    """

    # Get song URLs
    song_urls = parse.get_song_urls(artist_urls)

    for artist, urls in song_urls.items():
        path = (
            conf["base_path"] + conf["scrape_path"] + misc.shorten_artist(artist) + "/"
        )
        count_skipped = 0

        # Create directory for scraped files if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)

        for url in urls:
            file_name = f"{misc.shorten_artist(artist)}-{url.split('/')[-1]}.html"

            # Do nothing if file exists already
            if os.path.isfile(os.path.join(path, file_name)):
                count_skipped += 1
                continue

            # GET file
            response = requests.get(
                url, conf["header"], allow_redirects=False, timeout=30
            )

            if response.status_code == 200:
                with open(path + file_name, "w", encoding="utf-8") as file:
                    file.write(response.text)

                print(f"File {path + file_name} for {artist} written to file.")

            else:
                print(f"Error: Response code {response.status_code} for URL {url}.")

            time.sleep(conf["sleep_sec"])

        print(f"Skipped {count_skipped} existing files for artist {artist}.")
