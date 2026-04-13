import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os

# API key from Streamlit secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- UI ----------
st.set_page_config(page_title="AI Landing Page Personalizer", layout="centered")

st.markdown("""
<style>
.big-title { font-size: 40px; font-weight: bold; }
.section { margin-top: 30px; }
.card {
    background-color: #1e1e1e;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 AI Landing Page Personalizer</div>', unsafe_allow_html=True)
st.markdown("Improve your landing page using AI + CRO principles")

# ---------- INPUT ----------
ad_text = st.text_area("Enter Ad Content")
url = st.text_input("Enter Landing Page URL")

# ---------- SCRAPER ----------
def scrape_page(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"
        headings = [h.get_text() for h in soup.find_all(["h1", "h2", "h3"])]

        return title, headings[:5]
    except:
        return "Error fetching page", []

# ---------- BUTTON ----------
if st.button("Generate"):

    if not ad_text or not url:
        st.warning("Please enter both fields")
    else:
        title, headings = scrape_page(url)

        prompt = f"""
Ad: {ad_text}
Landing Page Title: {title}
Headings: {headings}

Generate:
1. Better headline
2. CTA
3. Suggestions
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        # ---------- OUTPUT UI ----------
        st.markdown("## 🎯 AI Suggestions")

        st.markdown(f'<div class="card">{output}</div>', unsafe_allow_html=True)

        # ---------- CLEAN HEADINGS ----------
        st.markdown("## 🔄 Before vs After")

        st.write(f"**Original Title:** {title}")

        st.markdown("**Headings:**")
        for h in headings:
            if h.strip():
                st.write(f"• {h}")
