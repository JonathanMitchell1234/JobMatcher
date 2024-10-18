# NexOp AI

NexOp AI is a web application that helps users find job postings that best match their resume. The application scrapes job listings from various job sites and uses a generative AI model to analyze and match the jobs to the user's resume. This project is currently under early active development but is fully functional.

Job Scraping is enabled by [Bunsly/JobSpy](https://github.com/Bunsly/JobSpy/tree/main). Shoutout to their work on creating/maintaining the JobSpy package.

<img width="1429" alt="Screenshot 2024-10-17 at 7 50 27 PM" src="https://github.com/user-attachments/assets/a2ec5ae3-9af6-4c79-b502-b1ac3ba85546">


## Features

- Scrape job listings from multiple job sites including Indeed, LinkedIn, ZipRecruiter, and Glassdoor.
- Upload resume as text or PDF.
- Analyze job listings and match them to the user's resume.
- Display analysis results in a user-friendly format.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/nexop-ai.git
    cd jobmatcher
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory.
    - Add your Google API key:
        ```
        GOOGLE_API_KEY=your_google_api_key
        ```

## Usage

1. Start the Flask application:
    ```sh
    python3 app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5001`.

3. Fill out the form with the search term, location, number of results, and your resume (either as text or PDF).

4. Click "Analyze Jobs" to see the analysis results.

## Project Structure

- `app.py`: Main application file containing the Flask routes and logic for scraping and analyzing jobs.
- `static/`: Directory containing static files such as JavaScript.
    - `script.js`: JavaScript file for handling form submission and displaying results.
- `templates/`: Directory containing HTML templates.
    - `index.html`: Main HTML template for the application.
- `requirements.txt`: List of Python dependencies.
- `.env`: Environment variables file (not included in the repository).
- `scraped_job_ids.json`: Sample JSON file containing scraped job IDs.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
