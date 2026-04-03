# AI Website Analysis & Outreach Generator

## Overview

This project is an AI-powered pipeline that analyzes business websites and generates structured insights along with personalized outreach messages.

It combines web scraping, semantic search (embeddings), and LLM-based reasoning to produce grounded, context-aware outputs.

---

## Problem

Large Language Models often produce generic or inaccurate outputs when given raw or unstructured web data.

This project addresses that by:

* Extracting clean, structured website content
* Ranking relevant information using embeddings
* Supplying only high-signal context to the LLM

---

## Solution Architecture

The system consists of four main stages:

### 1. Web Scraping & Crawling

* Built using Playwright + BeautifulSoup
* BFS crawling (up to top ~25 pages per site)
* URL scoring based on relevance keywords:

  * "about", "contact", "services", etc.
* Partial filtering using robots.txt rules
* Extracted elements:

  * `h1`, `h2`, `h3`, `p`, `li`
* Content grouped by DOM structure (`section`, `article`, `div`)

---

### 2. Content Processing

* Clean text extraction using `get_text(strip=True)`
* Logical chunking to preserve semantic grouping
* Each chunk represents a coherent piece of content

---

### 3. Semantic Ranking (Embeddings)

* Model: SentenceTransformers
* Keyword embeddings created for target signals
* All content chunks embedded and compared via similarity
* Top-ranked chunks selected (~5000 characters total)

This ensures only the most relevant information is passed to the LLM.

---

### 4. LLM Analysis & Generation

* Model: GPT-4o-mini
* Structured prompt design to enforce:

  * grounded outputs
  * minimal hallucination
  * JSON format responses

### Output includes:

* Business analysis
* Identified friction points
* Personalized outreach message

---

## Example Output

```json
{
  "business_analysis": {
    "what_they_do": "...",
    "who_they_serve": "...",
    "concrete_offerings": ["..."],
    "proof_points": ["..."]
  }},
  "friction_points": [
    {{
      "observation": "...",
      "why_it_matters": "...",
      "anchor": "..."
    }}
  ],
  "outreach_message": "..."
}
```

---

## Key Learnings

* Passing raw HTML significantly reduces LLM output quality
* Embedding-based filtering improves relevance and accuracy
* Structured prompts reduce hallucinations
* Data selection is more important than model size

---

## Limitations

* robots.txt filtering is partial
* Some irrelevant sections (e.g., legal pages) may still be included
* Outreach messages can still sound generic without further refinement

---

## Future Improvements

* Better classification of content (e.g., legal vs marketing)
* Improved personalization in outreach generation
* More robust robots.txt compliance
* Lead generation and automation layer

---

## Tech Stack

* Python
* Playwright
* BeautifulSoup
* SentenceTransformers
* OpenAI API (GPT-4o-mini)

---

## How to Run

Add your OpenAI API key on the .env file and save it.

***Then:***

```bash
pip install -r requirements.txt
python src/main.py
```

---

## Author

Konstantinos Leivaditis

