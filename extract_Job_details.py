import json
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
import os

if __name__ == '__main__':
    def to_markdown(text):
        text = text.replace('.', '*')
        return Markdown(textwrap.indent(text, '>', predicate=lambda _: True))

    GOOGLE_API_KEY = "AIzaSyDqMRnAMNrc8N_B2QHIxpSzFcHSM-SnCCE"

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro-vision')

    def get_text_from_document(document_path):
      try:
          with open(document_path, "r", encoding="utf-16-le") as f:
              text = f.read()
              return text
      except UnicodeError:
          try:
              with open(document_path, "r", encoding="utf-16-be") as f:
                  text = f.read()
                  return text
          except UnicodeError:
              # Handle both encoding attempts failing
              raise Exception("Unable to determine file encoding")


    def extract_job_details(text):
        # Extract document text and call the model with the desired prompt
        document_text = get_text_from_document(text)  # Replace this with your function to extract text from a document
        response = model.generate_content(text=document_text, prompt="Extract the skills, job title, worktype, experience, qualifications, and certifications in JSON format")


        # Process the response to extract data into a dictionary
        extracted_data = {}
        for entity in response.entities:
            if entity.label == "JobTitle":
                extracted_data["job_title"] = entity.text
            elif entity.label == "Skills":
                extracted_data["skills"] = [skill.text for skill in entity.subentities]
            elif entity.label == "WorkExperience":
                extracted_data["experience"] = [exp.text for exp in entity.subentities]
            elif entity.label == "EmploymentType":
                extracted_data["worktype"] = entity.text
            elif entity.label == "Qualification":
                extracted_data["qualifications"] = [qual.text for qual in entity.subentities]
            elif entity.label == "Certification":
                extracted_data["certifications"] = [cert.text for cert in entity.subentities]

        return extracted_data

    # Example usage with a document path
    document_path = "./Description/.Net Developer.txt"
    extracted_data = extract_job_details(document_path)

    # Print extracted data as JSON
    print(json.dumps(extracted_data, indent=4))

    # Optionally, format and display the data in Markdown
    display(to_markdown(f"Job Title: {extracted_data['job_title']}"))
    display(to_markdown(f"Skills: {', '.join(extracted_data['skills'])}"))
    display(to_markdown(f"Experience: {', '.join(extracted_data['experience'])}"))
    display(to_markdown(f"Work Type: {extracted_data['worktype']}"))
    display(to_markdown(f"Qualifications: {', '.join(extracted_data['qualifications'])}"))
    display(to_markdown(f"Certifications: {', '.join(extracted_data['certifications'])}"))
