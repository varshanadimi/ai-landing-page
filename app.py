import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("AI Landing Page Personalizer 🚀")
st.markdown("### Free version (no API cost)")

ad_text = st.text_area("Enter Ad Content")
url = st.text_input("Enter Landing Page URL")

def scrape_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else ""
        headings = [h.get_text() for h in soup.find_all(["h1", "h2"])][:3]

        return title, headings
    except:
        return "", []

def generate_fake_ai(ad, title, headings):
    return f"""
🔥 New Headline:
{ad} - Limited Time Offer!

👉 New CTA:
Shop Now & Save Big!

✨ Suggestions:
1. Match headline with ad message
2. Add urgency (limited time, discount)
3. Highlight benefits clearly
"""

if st.button("Generate"):
    if ad_text and url:
        with st.spinner("🔍 Analyzing..."):
            title, headings = scrape_page(url)
            output = generate_fake_ai(ad_text, title, headings)

        st.markdown("## 🎯 AI Suggestions")
        st.write(output)

        st.markdown("## 🔄 Before vs After")
        st.write(f"Original Title: {title}")
        st.write(f"Headings: {headings}")

    else:
        st.warning("Enter both fields")

st.markdown("---")
st.markdown("Built with ❤️ (Free Demo Version)")
