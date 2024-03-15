# NLP Lyrics Classifier

**Classifying song lyrics using Natural Language Processing (NLP)**

In this project, we build a text classification model on song lyrics. The task is to predict the artist from a piece of text. To train such a model, we first need to collect a lyrics dataset. We will

- Download a HTML page from lyrics.com with links to songs using the `requests` library
- Extract hyperlinks of song pages using the `BeautifulSoup` library
- Download and extract the song lyrics and save them to a temporary CSV file using the `requests` and `pandas` libraries
- Clean and preprocess the lyrics using `TreebankWordTokenizer` and `WordNetLemmatizer` from the `nltk` library
- Vectorize the text using `TfidfVectorizer` from the `sklearn` library
- Build a classification model using Naive Bayes classifier for multinomial models (`MultinomialNB`) and tune its hyperparameters using `GridSearchCV`
- Predict the artist from a piece of text based on the trained model

## Script

All these steps are implemented in the files contained in `includes`. To **run the project**, create a Python environment (Python 3.11), install dependencies from `requirements.txt`, define configuration in `settings.py`, and run `main.py` in the root directory. To **predict the artist** from a piece of text, run `predict.py` in the root directory.

Running `main.py` with all options set tu `True` will create the following files in the `data` and `models` directories:

- **`data/songs_clean.csv`** will contain the lyrics of ~600 songs from 3 artists (Adele, Eels, Rage Against The Machine)
- **`data/songs_by_line.csv`** will contain the same lyrics split by line (~15.000 rows)
- **`models/trained_model.pkl`** will contain the trained model

The trained model is included in the project. To just try out the prediction, you can run `predict.py` without running `main.py` first.

## Notebook

The Jupyter Notebook included in the proyect uses the the functions defined in the files in `include` to walk through the steps of the script.

## Word Clouds

The script includes the possibility to create word clouds from the corpus. See the function `plot_wordcloud()` in `includes/misc.py` or the example the Jupyter Notebook. To create the `text` option, download the [Boldova font](https://www.cufonfonts.com/font/boldova) first and place the ttf in `data/Boldova.ttf`.

Here are some examples (Left to right: Adele, Eels, Rage Against The Machine):

### Rectangle

<p float="left">
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Adele-rect.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Adele-rect.png?raw=true" width="250" />
  </a>
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Eels-rect.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Eels-rect.png?raw=true" width="250" />
  </a>
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-ratm-rect.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-ratm-rect.png?raw=true" width="250" />
  </a>
</p>

### Circle

<p float="left">
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Adele-circle.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Adele-circle.png?raw=true" width="250" />
  </a>
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Eels-circle.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Eels-circle.png?raw=true" width="250" />
  </a>
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-ratm-circle.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-ratm-circle.png?raw=true" width="250" />
  </a>
</p>

### Text

<p float="left">
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Adele-text.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Adele-text.png?raw=true" width="250" />
  </a>
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Eels-text.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-Eels-text.png?raw=true" width="250" />
  </a>
  <a href="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-ratm-text.png">
    <img src="https://github.com/yotkadata/lyrics-classifier-nlp/blob/main/wordclouds/wordcloud-ratm-text.png?raw=true" width="250" />
  </a>
</p>

## Other

This project was a weekly project in the Data Science Bootcamp at Spiced Academy, April 2023.
