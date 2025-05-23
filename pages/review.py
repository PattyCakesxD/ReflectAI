import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

# Retrieves text data specifically from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Retrieves text data from an uploaded file to be used in an LLM
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

# LLM
def analyze_resume(uploaded_file, job, job_desc, additional_details):
    file_content = extract_text_from_file(uploaded_file)

    if not file_content.strip():
        st.error("The file is empty.")
        st.stop()

    job_desc_prompt = f"""The applicant has included a description of the job listing:
                            {job_desc}"""
    
    additional_details_prompt = f"""The applicant also has some additional details that needs consideration:
                {additional_details}"""
    
    prompt = f"""Act as a senior hiring manager with over 20 years of experience in the ${job if job else 'general work' } industry. You have firsthand expertise in the ${job} industry and a deep understanding of what it takes to succeed in this position. Your task is to identify the ideal candidate based solely on their resume, ensuring they meet and exceed expectations for ${job} job applications".
                Break down the key qualifications, technical and soft skills, relevant experience, and project work that would make a candidate stand out. Highlight essential industry certifications, domain expertise, and the impact of past roles in shaping their suitability.
                Additionally, evaluate leadership qualities, problem-solving abilities, and adaptability to evolving industry trends. If applicable, consider cultural fit, teamwork, and communication skills required for success in the organization.
                Finally, provide a structured assessment framework what an exceptional resume should look like, red flags to avoid, and how to differentiate between a good candidate and a perfect hire. Ensure your response is comprehensive, strategic, and aligned with real-world hiring best practices.

                {job_desc_prompt if job_desc else ""}
                
                {additional_details_prompt if additional_details else ""}
                
                Resume Content:
                {file_content}

                Keep the assessment concise and straight to the point.
                There is no need for recaps if there is no constructive criticism or assertment to go along with them.
                Though, if you deem it necessary, do include examples to drive a point.
                This includes change recommendations, such as changing a certain phrasing to another phrasing.
                
                If possible, colorize important messages. For example, red for critiques and green for positive reinforcement.
                The colors you may use are: green, orange, red. Which colors you use is up to your discretion, but it should relate to severity (e.g., the good, bad, and ugly)
                This program uses streamlit to show the output text. As such, when you colorcode, use the format ':color[text]' (ignore the single quotes), where color can be green or red, and text is the intended text for output.
                For example, the line ':green[Hello world!]' (ignore the single quotes) will write the string 'Hello world!' in green.
                If you do 'Hello :red[world!] Example' instead, you will get a white 'Hello', a red 'world!', and a white 'Example'.
                To clarify, the following syntax is invalid: ':orange: text'. It must be in the form ':color[text]'.

                Consider using bold text too, as if you were highlighting phrases.
                A table to explain things may also make things easier to interpret.
                
                At the end, include a table that summarizes the assessment in 3 columns: Areas, Rating, and Comments. A "Summarized Assessment".
                Areas refers to the major sections or areas of expertise you've identified or have covered implicitly.
                For the ratings, format it explicitly out of 10, e.g. '7/10'. Color-code as relevant.
                Do not sugar coat anything. Feel free to speak as critically as you feel.

                Do not ask follow up questions.
                """
    
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {  
                "role": "system",
                "content": "You are an expert resume reviewer with years of experience in HR and recruitment."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=2000
    )
    
    return response

def main():
    # Page setup
    st.image("assets/banner_big.png")
    st.markdown("""
                #### See your resume through a *:rainbow[critical eye]*
                """)

    # Initialize states
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'analysis_response' not in st.session_state:
        st.session_state.analysis_response = None
    
    # Inputs
    uploaded_file       = st.file_uploader(":green[Upload your resume] :gray[(PDF or TXT)]", type=["pdf", "txt"], disabled=st.session_state.processing)
    job                 = st.text_input(":material/business_center: **Career/Job Title**", max_chars=100, disabled=st.session_state.processing)
    job_desc            = st.text_area(":material/assignment_ind: **Job Description** :gray[(optional)]", disabled=st.session_state.processing)
    additional_details  = st.text_area(":material/edit: Any additional details? :gray[(optional)]", disabled=st.session_state.processing)
    
    # Layout
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        analyze_button = st.button("Analyze Resume", icon=":material/troubleshoot:", disabled=st.session_state.processing)

    with c2:
        status_placeholder = st.empty()

    # Validate inputs
    if analyze_button:
        if not uploaded_file or not job:
            st.toast(":orange[Missing file or job title.] Please try again!", icon=":material/error:")
        else:
            st.session_state.processing = True
            st.rerun()

    # Analysis
    if st.session_state.processing:   
        with status_placeholder:
            with st.spinner(":blue[In analysis...]"):
                try:
                    response = analyze_resume(uploaded_file, job, job_desc, additional_details)
                    st.session_state.analysis_response = response
                except Exception as e:
                    st.error(f"Something went wrong: ${str(e)}")
                    st.session_state.analysis_response = None
                    st.stop()
                finally:
                    st.session_state.processing = False
                    st.rerun()
    
    # Output LLM response
    res = st.session_state.analysis_response
    if res:
        st.markdown("### Analysis Results")
        st.divider()
        st.markdown(res.choices[0].message.content)

if __name__ == "__main__":
    main()