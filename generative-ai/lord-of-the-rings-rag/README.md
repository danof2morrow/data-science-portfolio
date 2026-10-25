# Lord of the Rings Question-Answering with RAG

## Question

How can a language model answer questions using retrieved article text, and where can the retrieval and generation process still fail?

## Approach

The application retrieves a Wikipedia article about the Lord of the Rings film trilogy with requests and BeautifulSoup. It splits the text into overlapping 500-character chunks with 100-character overlap, creates normalized embeddings using `sentence-transformers/all-MiniLM-L6-v2`, and indexes them with FAISS inner-product search. The top three retrieved chunks become context for `google/flan-t5-large`, followed by an interactive question-answer loop.

## Saved Results and Lessons

The saved run contains 100 indexed chunks and answers examples such as the director question with Peter Jackson and the composer question with Howard Shore. It also retains failed retrievals, unavailable-answer responses, and an incorrect principal-photography answer of `2001`.

Changing a question's wording changes which chunks are retrieved. Similarity scores do not establish that a chunk contains the answer, and an instruction to use only context does not guarantee factual grounding. This makes the notebook useful as an examination of RAG failure modes as well as a working application example.

## Artifact

[Open the complete notebook](lord_of_the_rings_rag.ipynb). The source, markdown, and saved outputs are unchanged. The original Colab badge inside the notebook references its former root filename; open the current notebook directly in Colab instead.

## Reproduce

Use a compatible Jupyter or Google Colab environment with internet access. Run the installation cell, then the remaining cells in order. The notebook downloads the Wikipedia article, the embedding model, and FLAN-T5 Large. A GPU is recommended for generation; the code falls back to CPU when CUDA is unavailable. The final cell prompts interactively; enter `exit` to stop.

## Limitations

This project uses one changing web article, character-based chunking, and a 512-token model input limit. Relevant context can be missed or truncated. It does not provide a formal accuracy benchmark or guarantee source-grounded answers. The saved run is retained, and a fresh connected CPU run has now completed; see the execution record below.

[Portfolio](../../index.html) · [Validation record](../../docs/validation.md)

## Verified Run and Quick Start

From this project folder:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

[Open the current notebook in Colab](https://colab.research.google.com/github/danof2morrow/data-science-portfolio/blob/main/generative-ai/lord-of-the-rings-rag/lord_of_the_rings_rag.ipynb) or open it locally, then run cells in order. Internet access is required for Wikipedia and model downloads. No API key is needed for the public models. A GPU can speed up generation, but the original code also runs on CPU.

The October 25, 2026 fresh IPython run passed all **12 runtime code cells** on CPU. The installation command was completed separately using the same package list, with tokenizer and proxy dependencies supplied by the requirements file. The test fetched the article, created **100 chunks**, produced **100 x 384 embeddings**, indexed **100 vectors**, ran the existing example questions, and exercised the original interactive loop with a question and `exit`.

See [execution_summary.json](execution_summary.json) for exact package versions and source hash. The notebook, including its saved examples and failure cases, remains unchanged. A completed execution does not establish that every generated answer is factually correct. Live article contents, model downloads, and compatible package versions can affect later results.
