"""
Other helper functions for the project.
"""

import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from settings import conf
from wordcloud import STOPWORDS, WordCloud


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

    file_name = "songs_by_line.csv"
    df_.to_csv(conf["base_path"] + file_name)
    print(f"Saved lyrics by line to {file_name}")

    return df_


def wordcloud_create_img(text: str, width: int = 2000, height: int = 1500):
    """
    Function to create an image containing the artist name.
    """
    # Define font to be used
    font = ImageFont.truetype("Boldova.ttf", size=600)

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
        mask = np.array(wordcloud_create_img(name, width=width, height=height))
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
