import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

@st.cache_resource
def get_chain():
    return Chain()

@st.cache_resource
def get_portfolio():
    return Portfolio()

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input(
        "Enter a URL:",
        value="https://career.fpt-software.com/jobs/machine-learning-software-engineer/"
    )
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner("⏳ Generating cold mail... please wait."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No jobs found.")
                for job in jobs:
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language="markdown")

            except Exception as e:
                st.error(f"⚠️ An Error Occurred: {e}")

if __name__ == "__main__":
    chain = get_chain()
    portfolio = get_portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
