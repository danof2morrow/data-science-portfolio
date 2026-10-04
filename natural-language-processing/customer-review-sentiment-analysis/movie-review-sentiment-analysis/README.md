# Movie Review Sentiment Analysis and Text Preprocessing

## Overview

This project applies natural language processing techniques to 25,000 labeled movie reviews to classify sentiment and prepare unstructured text for future machine learning models.

The first part of the analysis compares two prebuilt sentiment analyzers, TextBlob and VADER. The second part focuses on transforming raw review text into numerical features that could be used to train a custom text classification model.

## Sentiment Analysis

The dataset contains:

- 25,000 movie reviews
- 12,500 positive reviews
- 12,500 negative reviews

Two sentiment analysis tools are evaluated:

- TextBlob achieved approximately 68.5% accuracy
- VADER achieved approximately 69.4% accuracy

Both performed better than the 50% accuracy expected from random guessing on the balanced dataset, with VADER performing slightly better.

## Text Preprocessing

The project also prepares the review text for future machine learning by:

- Converting text to lowercase
- Removing punctuation and special characters
- Removing English stopwords
- Applying NLTK's PorterStemmer
- Creating a bag-of-words representation
- Creating a TF-IDF representation

Both the bag-of-words and TF-IDF matrices contain 25,000 rows and 49,642 text features.

## Tools

- Python
- Pandas
- TextBlob
- NLTK
- VADER
- Scikit-learn
- Jupyter Notebook

## Project Files

- Jupyter notebook — sentiment analysis, text preprocessing, bag-of-words, and TF-IDF feature creation

## Limitations

TextBlob and VADER are prebuilt sentiment analyzers rather than models trained specifically on this movie review dataset.

The preprocessing portion prepares the text for a custom machine learning model, but this notebook does not train that custom classifier.
