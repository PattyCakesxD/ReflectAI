import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

"""
Retrieves text data specifically from a PDF
"""
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

"""
Retrieves text data from an uploaded file to be used in an LLM
"""
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    st.set_page_config(page_title="ReflectAI", layout="centered")

    st.markdown("""
                # :blue[ResumeAI]

                #### See your resume through a *:rainbow[critical eye]*
                """)

    uploaded_file = st.file_uploader(":green[Upload your resume] :gray[(PDF or TXT)]", type=["pdf", "txt"])

    job = st.text_input("Enter the job you're targetting (optional)")
    analyze = st.button("Analyze Resume")
    
    """ Runs the LLM, assuming a file is actually uploaded. """
    if analyze and uploaded_file:
        try:
            file_content = extract_text_from_file(uploaded_file)

            if not file_content.strip():
                st.error("The file is empty.")
                st.stop()

            prompt = f"""Your task is to help me secure more job interviews by optimizing my resume to highlight relevant skills and experiences. You will perform this task in a series of steps.

                        <step1>Start by compiling all the current information from my resume. Gather details about my education, work experience, skills, certifications, and any relevant projects or volunteer work. Organize this information into categories for easy access and reference. Save this organized information in variable $resume_data.</step1>
                        <step2>Using $resume_data, write a new resume. Begin with a clear header that includes my name, contact information, and professional title or area of expertise. Structure the content into sections: Professional Summary, Skills, Work Experience, Education, and Additional Information. Focus on clarity and relevance to my career goals.</step2>
                        <step3>Modify my resume for each job application. Examine the job description carefully and identify keywords and skills that the employer emphasizes. Adjust my resume to highlight my qualifications that match these requirements. This customization shows employers my candidacy aligns well with the job expectations. Save the tailored resume in $custom_resume.</step3>
                        <step4>Proofread my tailored resume for any errors in spelling, grammar, or formatting. Pay special attention to consistency in style and detail. Consider asking a friend or using professional services to review my resume. This ensures it is polished and professional. Store the final version of my resume in $final_resume.</step4>

                        Resume Content:
                        {file_content}

                        Please provide your analysis in a clear, structured format with specific recommendations."""
            
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
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
                temperature=0.7,
                max_tokens=1000
            )

            st.markdown("### Analysis Results")
            st.markdown(response.choices[0].message.content)
        
        except Exception as e:
            st.error(f"An error occured: {str(e)}")

if __name__ == "__main__":
    main()