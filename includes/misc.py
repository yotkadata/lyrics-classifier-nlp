"""
Other helper functions for the project.
"""

import os
import re

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from wordcloud import STOPWORDS, WordCloud

from settings import conf


def shorten_artist(artist: str) -> str:
    """
    Function to shorten the artist name.
    """
    return (
        "".join(re.findall(r"\b\w", artist)).lower()
        if len(artist.split(" ")) > 1
        else artist.lower()
    )


def convert_lyrics_to_lines(df_: pd.DataFrame) -> pd.DataFrame:
    """
    Function to split the lyrics by line.
    """
    df_ = (
        # Set columns not to be touched as index
        df_.set_index(["title", "artist"])
        # Split and explode the lyrics by newline
        .apply(lambda x: x.str.split("\n").explode())
        # Reset index
        .reset_index()
    )

    # Remove rows without lyrics in them
    df_ = df_[df_["lyrics"].notna()]
    df_ = df_[df_["lyrics"] != ""]

    dir_name = conf["base_path"] + "data/"
    file_name = "songs_by_line.csv"
    df_.to_csv(dir_name + file_name)
    print(f"Saved lyrics by line to {dir_name + file_name}")

    return df_


def wordcloud_create_img(text: str, width: int = 2000, height: int = 1500):
    """
    Function to create an image containing the artist name.
    """
    # Define font to be used (downloaded from https://www.cufonfonts.com/font/boldova)
    font_file = "data/Boldova.ttf"

    if not os.path.isfile(font_file):
        print("Error: Font file not found.")
        return None

    font = ImageFont.truetype(font_file, size=600)

    # Create image
    img = Image.new("RGB", (width, height), color="white")
    img_draw = ImageDraw.Draw(img)

    # Calculate coordinates to center the text
    text_width, text_height = img_draw.textsize(text, font=font)
    x_text = int((width - text_width) / 2)
    y_text = int((height - text_height) / 2)

    # Add text
    img_draw.text((x_text, y_text), text, font=font, fill=(0, 0, 0))

    return img


def plot_wordcloud(corpus: str, name: str, shape: str = "rect") -> None:
    """
    Function to plot the wordcloud.
    """
    # Some settings
    width = 2000
    height = 1000

    # Create shapes
    if shape == "circle":
        # From https://www.python-lernen.de/wordcloud-erstellen-python.htm
        x_val, y_val = np.ogrid[:1000, :1000]
        mask = (x_val - 500) ** 2 + (y_val - 500) ** 2 > 400**2
        mask = 255 * mask.astype(int)

        # Change width to get a square
        width = height
    elif shape == "text":
        # Change width to get a wide rectangle
        height = int(width / 2)

        # Create image with text
        wordcloud_img = wordcloud_create_img(name, width=width, height=height)
        if wordcloud_img is None:
            return None
        mask = np.array(wordcloud_img)
    else:
        mask = None

    # Generate word cloud
    wordcloud = WordCloud(
        width=width,
        height=height,
        random_state=1,
        background_color="white",
        # colormap="Pastel1",
        collocations=False,
        stopwords=STOPWORDS,
        mask=mask,
        contour_color="#ccc",
        contour_width=2,
    ).generate(corpus)

    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off")
    # Save as file
    plt.savefig(f"wordclouds/wordcloud-{name}-{shape}.png", dpi=72, bbox_inches="tight")

    return None


def download_nltk_data(data_type: str) -> None:
    """
    Function to download the NLTK data.
    """

    if data_type not in ["wordnet", "stopwords"]:
        print("Error: Invalid data type.")
        return None

    data_directory = conf["base_path"] + "data/nltk/"

    # Check if zip is already in the data directory
    if not os.path.isfile(data_directory + "corpora/" + data_type + ".zip"):
        print("Downloading NLTK data")
        nltk.download(data_type, download_dir=data_directory)

    return None
