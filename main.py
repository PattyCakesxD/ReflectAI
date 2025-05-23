import streamlit as st

# Pages
resume_review_page = st.Page(
    page="pages/review.py",
    title="Resume Review",
    icon=":material/troubleshoot:",
    default=True
)

cover_letter_page = st.Page(
    page="pages/cover.py",
    title="Cover Letter Generator",
    icon=":material/stylus_note:",
)


# Navigation
pg = st.navigation(
    {
        "Tools": [resume_review_page, cover_letter_page],
    }
)

# Shared on all pages
st.logo("assets/logo.png", size="large")

st.set_page_config(page_title="ReflectAI", layout="centered")
st.sidebar.markdown(":gray[:material/bolt: Built in 2025 :material/bolt:]")

# Run navigation
pg.run()
