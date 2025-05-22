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

# Run navigation
pg.run()