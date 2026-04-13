import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---------------- UI ----------------
st.set_page_config(page_title="AI Landing Page Personalizer", layout="centered")

st.title("AI Landing Page Personalizer 🚀")
st.markdown("### Free version (no API cost)")

# ---------------- Inputs ----------------
ad_text = st.text_area("Enter Ad Content")
url = st.text_input("Enter Landing Page URL")

# ---------------- Scraping ----------------
def scrape_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No title found"

        headings = []
        for tag in soup.find_all(["h1", "h2", "h3"]):
            text = tag.get_text().strip()
            if text:
                headings.append(text)

        return title, headings

    except:
        return "Error fetching page", []

# ---------------- Simple AI Logic (No API) ----------------
def generate_suggestions(ad_text):
    headline = f"{ad_text} - Limited Time Offer!"
    cta = "Shop Now & Save Big!"

    suggestions = [
        "Match headline with ad message",
        "Add urgency (limited time, discount)",
        "Highlight benefits clearly"
    ]

    return headline, cta, suggestions

# ---------------- Button ----------------
if st.button("Generate"):
    if not ad_text or not url:
        st.warning("Please enter both fields")
    else:
        with st.spinner("Analyzing..."):
            title, headings = scrape_page(url)
            new_headline, new_cta, suggestions = generate_suggestions(ad_text)

        # ---------------- Output ----------------
        st.markdown("## 🎯 AI Suggestions")

        st.markdown(f"🔥 **New Headline:** {new_headline}")
        st.markdown(f"👉 **New CTA:** {new_cta}")

        st.markdown("✨ **Suggestions:**")
        for i, s in enumerate(suggestions, 1):
            st.write(f"{i}. {s}")

        st.markdown("---")

        st.markdown("## 🔄 Before vs After")

        st.markdown(f"**Original Title:** {title}")

        st.markdown("**Headings:**")
        for h in headings:
            if h.strip():
                st.write(f"• {h}")
