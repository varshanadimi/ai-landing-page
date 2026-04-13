import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Landing Page Personalizer", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: white;
}
.stTextInput, .stTextArea {
    background-color: #262730 !important;
    border-radius: 10px;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}
.highlight {
    color: #00ffcc;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align: center;'>🚀 AI Landing Page Personalizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Optimize your landing page using AI + CRO principles</p>", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown("### 📝 Input Details")

ad_text = st.text_area("Ad Content", placeholder="Enter your ad copy here...")
url = st.text_input("Landing Page URL", placeholder="https://example.com")

# ---------------- SCRAPER ----------------
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

# ---------------- LOGIC ----------------
def generate_suggestions(ad_text):
    headline = f"{ad_text} - Limited Time Offer!"
    cta = "🚀 Shop Now & Save Big!"

    suggestions = [
        "Match headline with ad message",
        "Add urgency (limited time, discount)",
        "Highlight benefits clearly"
    ]

    return headline, cta, suggestions

# ---------------- BUTTON ----------------
if st.button("✨ Generate AI Suggestions"):
    if not ad_text or not url:
        st.warning("⚠️ Please fill both fields")
    else:
        with st.spinner("Analyzing your landing page..."):
            title, headings = scrape_page(url)
            new_headline, new_cta, suggestions = generate_suggestions(ad_text)

        # ---------------- OUTPUT ----------------
        st.markdown("## 🎯 AI Suggestions")

        st.markdown(f"""
        <div class="card">
            🔥 <span class="highlight">New Headline:</span><br>{new_headline}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            👉 <span class="highlight">New CTA:</span><br>{new_cta}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ✨ Improvement Suggestions")
        for i, s in enumerate(suggestions, 1):
            st.markdown(f"- {i}. {s}")

        st.markdown("---")

        # ---------------- BEFORE AFTER ----------------
        st.markdown("## 🔄 Before vs After")

        st.markdown(f"""
        <div class="card">
            📌 <span class="highlight">Original Title:</span><br>{title}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📄 Page Headings")
        for h in headings[:5]:  # limit to 5 for clean UI
            st.markdown(f"• {h}")
