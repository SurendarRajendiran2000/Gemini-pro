import os
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
from env import *
import pandas as pd
import docx
import fitz
import time

if __name__ == '__main__':
    def to_markdown(text):
        text = text.replace('.', '*')
        return Markdown(textwrap.indent(text, '>', predicate=lambda _: True))

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    def extract_resume_details(description):
        prompt = (
            "Please extract the following details from the job description and return the output only in JSON format with labels:\n\n"
            "1. Job Title\n"
            "2. Worktype\n"
            "3. Technical Skills\n"
            "4. Non-Technical Skills\n"
            "5. Certification\n"
            "6. Qualifications\n"
            "7. Experience\n\n"
            "Resume:\n" + description
        )

        response = model.generate_content(prompt)
        return response.text

    def process_job_descriptions(directory_path, excel_output_path):
        start_time = time.time()  # Record the start time

        # Check if the directory exists
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        # Create an empty list to store results
        results_list = []

        # List all files in the directory
        files = [file for file in os.listdir(directory_path) if file.endswith((".txt", ".pdf", ".docx"))]

        # Process each file
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)

            # Read the content based on the file type
            if file_name.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    job_description = file.read()
            elif file_name.endswith(".pdf"):
                job_description = extract_text_from_pdf(file_path)
            elif file_name.endswith(".docx"):
                job_description = extract_text_from_docx(file_path)
            else:
                print(f"Unsupported file format: {file_name}")
                continue

            # Extract details from job description
            extracted_details = extract_resume_details(job_description)

            # Append the results to the list
            results_list.append({"File Name": file_name, "Gemini Pro Output": extracted_details})


        # Create a DataFrame from the list of results
        results_df = pd.DataFrame(results_list)
        # Save the results to Excel
        results_df.to_excel(excel_output_path, index=False)

        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time} seconds")

    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text += page.get_text()
        return text

    def extract_text_from_docx(docx_path):
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    # Specify the directory containing job descriptions
    job_description_directory = r"C:\Users\surendar.rajendiran\Desktop\Job_Description"

    # Specify the Excel output path
    excel_output_path = r"C:\Users\surendar.rajendiran\Desktop\Output.xlsx"

    process_job_descriptions(job_description_directory, excel_output_path)
