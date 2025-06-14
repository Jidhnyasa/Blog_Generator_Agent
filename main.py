import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import numpy as np
import streamlit as st


llm=ChatGroq(model="qwen-qwq-32b", temperature=0.5)

def get_transcript(video_url: str)-> str:
    """
    Given a full Youtube Video ID or URl, fetch and concatenate the transcript text

    """
     
    if "youtube.com" in video_url or "youtube.be" in video_url:
        import re
        match=re.search(r"(?:v=|\.be/)([A-Za-z0-9_-]{11})", video_url)
        video_id = match.group(1) if match else video_url
    else:
        video_url = video_id

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    return " ".join(seg['text'] for seg in transcript)

title_generator = PromptTemplate(
    input_variables=['transcript'],
    template=(
        "You are a blog title generator. Create 2 SEO-optimized, click worthy titles for the blog titles" \
        "based on the following YouTube transcript:\n\n{transcript}\n\nTitles:"
    )
)

title_chain = LLMChain(llm=llm, prompt=title_generator)

def generate_titles(transcript: str) -> list[str]:
    raw = title_chain.run(transcript=transcript)
    return [t.strip() for t in raw.split("\n") if t.strip()]


content_prompt = PromptTemplate(
    input_variables=["title", "transcript"],
    template=(
        "You are an expert blog writer. Given the title and the transcript, "
        "write a detailed 800–1000 word blog post with introduction, body, and conclusion. "
        "Use insights from the transcript.\n\n"
        "Title: {title}\n\nTranscript:\n{transcript}\n\nBlog Post:"
    )
)
content_chain = LLMChain(llm=llm, prompt=content_prompt)

def generate_content(title: str, transcript: str) -> str:
    return content_chain.run(title=title, transcript=transcript)


def agentic_blog_generator(video_url: str, pick: int = 0) -> dict:
    """
    Full pipeline: ingest → title list → choose → blog.
    Returns dict with: titles, selected_title, blog_post.
    """
    ts = get_transcript(video_url)
    titles = generate_titles(ts)
    if not titles:
        raise ValueError("No titles generated.")
    idx = max(0, min(pick, len(titles)-1))
    sel = titles[idx]
    blog = generate_content(sel, ts)
    return {"titles": titles, "selected_title": sel, "blog_post": blog}


st.title("Agentic AI Blog Generator")
st.write("Enter a YouTube URL or ID, then generate SEO-optimized titles & a full blog post.")

video_input = st.text_input("YouTube URL or ID")
pick = st.number_input("Pick title # (0-based)", min_value=0, step=1, value=0)

if st.button("Generate Blog"):
    with st.spinner("Running pipeline…"):
        try:
            result = agentic_blog_generator(video_input, pick)
            st.write(result["selected_title"])
            
            st.write(result["blog_post"])
        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    
    st.title("END")
    