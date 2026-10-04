# Movie Review Sentiment Analysis and Text Preprocessing

## Overview

This project applies natural language processing techniques to 25,000 labeled movie reviews to evaluate sentiment and prepare unstructured text for future machine learning models.

The analysis has two parts. First, it compares TextBlob and VADER as prebuilt sentiment analyzers. Second, it transforms the raw review text into numerical features using common text preprocessing techniques.

## Dataset

The dataset contains:

- 25,000 movie reviews
- 12,500 positive reviews
- 12,500 negative reviews

Because the dataset is evenly balanced, random guessing would be expected to achieve approximately 50% accuracy.

## Sentiment Analysis

Two prebuilt sentiment analyzers are evaluated:

- TextBlob achieved approximately 68.5% accuracy
- VADER achieved approximately 69.4% accuracy

Both performed better than random guessing, with VADER producing slightly higher accuracy on this dataset.

## Text Preprocessing

The second part of the project prepares the movie review text for use in a custom machine learning model.

The preprocessing process includes:

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

- Jupyter notebook — sentiment classification, text preprocessing, bag-of-words, and TF-IDF feature creation

## Limitations

TextBlob and VADER are prebuilt sentiment analyzers rather than models trained specifically on this movie review dataset.

The preprocessing portion prepares the text for a custom machine learning model, but this project does not train that custom classifier.
