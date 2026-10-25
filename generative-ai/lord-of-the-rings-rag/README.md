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

This project uses one changing web article, character-based chunking, and a 512-token model input limit. Relevant context can be missed or truncated. It does not provide a formal accuracy benchmark or guarantee source-grounded answers. The saved run is retained, but a fresh connected model run has not been confirmed in this session.

[Portfolio](../../index.html) · [Validation record](../../docs/validation.md)
