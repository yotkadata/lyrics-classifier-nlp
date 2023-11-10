import os

#
# Define some variables for the script
#


conf = {
    "scrape_path": "scrape/",
    "scrape_song_list": False,
    "scrape_songs": False,
    "parse_html": False,
    "create_wordclouds": False,
    "train_model": True,
    "sleep_sec": 10,
    "header": {
        "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
    },
    "artist_urls": {
        "Eels": "https://www.lyrics.com/artist.php?name=Eels&aid=182509&o=1",
        "Rage Against the Machine": "https://www.lyrics.com/artist.php?name=Rage-Against-the-Machine&aid=23206&o=1",
        "Adele": "https://www.lyrics.com/artist.php?name=Adele&aid=861756&o=1",
    },
    "base_path": os.path.dirname(os.path.abspath(__file__)) + "/",
}
