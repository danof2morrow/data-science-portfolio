# Fine-Tuning DistilBERT for Movie Review Sentiment

## Business Question

Can a small fine-tuning run classify unfamiliar movie reviews well, and what does the overall score miss when the wording is sarcastic, mixed, or neutral?

## Approach

This project fine-tunes all 66,955,010 parameters of pretrained DistilBERT for binary sentiment classification. It uses 2,000 training reviews, 400 validation reviews, and 500 held-out test reviews sampled from IMDb. Exact duplicate text is removed and split overlap is checked. The best checkpoint is selected by validation macro F1, with test reviews reserved for the final evaluation.

Training uses two epochs, batches of eight, and a 256-token limit. A training-majority baseline provides a simple reference. Error analysis examines high-scoring wrong predictions and six original examples, including sarcasm and text without a clear binary label.

## Saved Results

- Test accuracy: **88.4%**, or 442 of 500 reviews.
- Test macro F1: **0.8840**.
- Training-majority baseline accuracy: **50.2%**.
- The model misclassified the sarcastic example as positive. It also assigned binary labels to mixed and neutral examples because the task offers no neutral category.
- **44.4%** of training reviews exceeded the 256-token limit and were truncated.

These are retained results from the notebook's October 17, 2026 Tesla T4 run, not a newly repeated training run. Training loss decreased while validation loss increased in the second epoch, despite a small validation F1 improvement. The result does not establish that longer training would help.

## How This Differs from the Prebuilt Sentiment Project

The [TextBlob/VADER project](../movie-review-sentiment-analysis/README.md) evaluates existing sentiment tools and creates text features. This project trains a transformer classifier and examines checkpoint selection, generalization, truncation, and confident mistakes. The datasets and evaluation samples differ, so the reported scores are not a controlled head-to-head comparison.

## Artifact

[Open the complete notebook](fine_tuned_movie_review_sentiment.ipynb) for code, retained charts and predictions, interpretation, and references. The notebook is preserved byte for byte from the final source file; only its filename changed.

## Reproduce

Open the notebook in Google Colab, choose a GPU runtime, and run the cells in order. The notebook installs its specified Hugging Face packages, downloads IMDb and DistilBERT, and saves training results under `/content/dsc670_week6`. Internet access and a compatible PyTorch/CUDA environment are required. Keep the original internal paths because the source code has not been altered.

The model weights and generated CSVs are saved separately during a run; they are not embedded in or distributed with this repository. Download them before a temporary Colab session ends if you want to reuse them.

## Limitations

The training and evaluation samples are small, inputs are truncated, and results concern English movie reviews. Prediction scores are not calibrated probabilities of correctness. Six original examples are diagnostic probes, not another reliable accuracy estimate. This session reviewed saved outputs and notebook structure; it did not repeat GPU training.

[Portfolio](../../index.html) · [Validation record](../../docs/validation.md)
