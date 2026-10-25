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

## Open the Artifacts

- [movie_review_sentiment_analysis.ipynb](movie_review_sentiment_analysis.ipynb)

## Reproduce the Analysis

Use Python 3.11 or newer. From this project folder:

```bash
python -m pip install -r requirements.txt
python setup_data.py
python -m jupyterlab
```

Open `movie_review_sentiment_analysis.ipynb`, restart the kernel, and run all cells in order. No API key is required. The setup helper downloads and verifies `labeledTrainData.tsv` beside the notebook and the NLTK stopwords and VADER lexicon ZIP resources under `~/nltk_data`, a default NLTK search location. These ZIPs can be read directly by NLTK.

If you prefer a custom resource directory, use `python setup_data.py --nltk-data /your/resource/path`, then set `NLTK_DATA` to that directory before starting Jupyter. Existing files with different hashes are not overwritten. A changed upstream download is rejected rather than silently changing the experiment inputs.

## Dataset Provenance

The original local TSV was unavailable. The test uses a [public dataset mirror](https://github.com/datarobot-community/movie-rating-app/blob/d0c255ace2fc9e44aa7b026711ac02b042c52e56/resources/labeledTrainData.tsv) pinned to a specific commit. It contains the Kaggle labeled IMDb training data, with 25,000 reviews and 12,500 labels in each class. Its first five review IDs and both classifier scores match the retained notebook outputs. This comparison supports using this copy for reproduction; it is not a byte-level comparison with the unavailable original local file.

NLTK resources come from the [official NLTK data repository](https://github.com/nltk/nltk_data). The setup helper fixes SHA-256 digests for all three downloads. The large TSV and downloaded resources are not bundled with this repository. If automatic downloading is unavailable, obtain the same TSV and NLTK resources manually, place them at the documented locations, and rerun setup to check their hashes.

## Execution Check

On October 25, 2026, all **12 nonempty code cells** completed sequentially in a fresh IPython process across **25,000 reviews**. The notebook code, markdown, saved outputs, and file bytes are unchanged.

| Output | Fresh result | Match to saved notebook |
|---|---:|---|
| TextBlob accuracy | 68.524% | Exact |
| VADER accuracy | 69.356% | Exact |
| Bag-of-words matrix | 25,000 rows x 49,642 features | Exact |
| TF-IDF matrix | 25,000 rows x 49,642 features | Exact |

The first five review IDs and the 12,500/12,500 class counts also match the saved outputs. The [execution record](execution_summary.json) includes input hashes, package versions, and results. This was a fresh IPython execution; a connected Jupyter kernel was not tested because its transport is restricted in this environment.

The reported accuracy evaluates prebuilt tools on labeled reviews; this notebook does not train a custom sentiment classifier. The separate [DistilBERT fine-tuning project](../fine-tuned-movie-review-sentiment/README.md) covers model training on different samples, so its scores are not a controlled head-to-head comparison.


[Portfolio](../../index.html) · [Repository guide](../../README.md)
