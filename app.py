import sys
import os

# app.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_skills
from recommender import recommend_jobs

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (e.g., from frontend)

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Career Recommender API is running 🚀"}), 200

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        resume_text = data.get("resumeText", "")

        if not resume_text.strip():
            return jsonify({"error": "Empty resumeText provided"}), 400

        # Extract skills from the resume text
        parsed_skills = extract_skills(resume_text)

        if not parsed_skills:
            return jsonify({
                "parsedSkills": [],
                "recommendations": [],
                "message": "No meaningful skills extracted from resume."
            }), 200

        # Get job recommendations
        recommendations = recommend_jobs(parsed_skills)

        return jsonify({
            "parsedSkills": parsed_skills,
            "recommendations": recommendations
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
