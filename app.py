# app.py
from flask import Flask, render_template, request, jsonify
import csv
import pandas as pd
from jobspy import scrape_jobs
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
import io
import markdown
import logging
from dotenv import load_dotenv

load_dotenv

app = Flask(__name__)

# Configure the Google Gemini API client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.route('/scrape_and_analyze', methods=['POST'])
def scrape_and_analyze():
    # Get form data
    logging.debug("scrape_and_analyze route called")
    search_term = request.form.get('search_term')
    location = request.form.get('location')
    results_wanted = int(request.form.get('results_wanted'))
    
    # Handle resume input (text or PDF)
    resume_text = request.form.get('resume')
    resume_file = request.files.get('resume_file')
    
    if resume_file and resume_file.filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_file)
        print("Parsed PDF content:")
        print(resume_text)
        print("End of parsed PDF content")
    elif not resume_text:
        return jsonify({'error': 'Please provide a resume (text or PDF file)'}), 400

    # Scrape jobs
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=24,
        country_indeed='USA',
        linkedin_fetch_description=True
    )

    # Prepare data for the model
    jobs_subset = jobs.head(10)  # Adjust as needed
    data_string = jobs_subset.to_csv(index=False)

    # Create the model with updated configuration
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "max_output_tokens": 5000000,
    }
    
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    # Craft the prompt
    prompt = f"""Here is a list of job postings in CSV format. I need you to look at the data, and choose the jobs that best match my resume, which I will provide to you. You should
    attempt to match the jobs to the resume's experience level and skills as best as possible. You should provide a brief explanation of each job, the location, the salary, and the URL to apply to the job. You should explain why each choice would be a good fit based on the resume that the user provided, comparing their qualifications to the job listing, and give an overview of the job description. Please format your response using Markdown for better readability.
    

    Resume:

    {resume_text}

    Jobs:

    {data_string}
    
    """
    
    print("Prompt: " + prompt)
    

    # Start a chat session and get the response
    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)

    # Convert markdown to HTML
    html_content = markdown.markdown(response.text)

    return jsonify({
        'analysis_markdown': response.text,
        'analysis_html': html_content
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)