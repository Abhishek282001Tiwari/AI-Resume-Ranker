print("app.py is running...")
from flask import Flask, request, render_template
from ranker import get_resume_score
import os
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        resume = request.files["resume"]
        job = request.files.get("job")

        resume_path = os.path.join(UPLOAD_FOLDER, secure_filename(resume.filename))
        resume.save(resume_path)

        job_text = request.form.get("job_text")
        if job and job.filename:
            job_path = os.path.join(UPLOAD_FOLDER, secure_filename(job.filename))
            job.save(job_path)
            if not job_text:
                job_text = extract_text_from_pdf(job_path)

        resume_text = extract_text_from_pdf(resume_path)

        result = get_resume_score(resume_text, job_text)
    print("Rendering index.html")
    return render_template("index.html", result=result)

if __name__ == "__main__":
    print("Flask app is starting...")
    print("Running app on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)