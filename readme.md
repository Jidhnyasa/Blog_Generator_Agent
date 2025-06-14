# Agentic AI Blog Generator

An end-to-end **Agentic AI** pipeline that ingests a YouTube transcript, auto-generates SEO-optimized blog titles, and drafts a full blog post—exposed via a Streamlit web UI.

---

## Features

- **Transcript Ingestion**  
  Fetches and concatenates YouTube video captions via the YouTube Transcript API.

- **Title Generation**  
  Uses an OpenAI model (e.g. GPT-4o) with LangChain to propose 3 SEO-optimized, click-worthy blog titles.

- **Content Generation**  
  Leverages the selected title + transcript to produce an 800–1,000 word blog post (introduction, body, conclusion).

- **Agentic Flow**  
  Orchestrated via a single “agentic” function that runs transcript → titles → selection → blog in sequence.

- **Streamlit Frontend**  
  Simple web app for entering any YouTube URL/ID, choosing a title index, and viewing the generated blog.

---


