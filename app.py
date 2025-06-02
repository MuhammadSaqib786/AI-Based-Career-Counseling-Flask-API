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
        print("[DEBUG] Incoming request JSON:", data)

        resume_text = data.get("resumeText", "")
        print("[DEBUG] Resume text received:", resume_text[:200])  # Show a snippet

        if not resume_text.strip():
            print("[ERROR] Empty resumeText provided.")
            return jsonify({"error": "Empty resumeText provided"}), 400

        # Extract skills from resume
        parsed_skills = extract_skills(resume_text)
        print("[DEBUG] Extracted skills:", parsed_skills)

        if not parsed_skills:
            print("[WARNING] No meaningful skills extracted.")
            return jsonify({
                "parsedSkills": [],
                "recommendations": [],
                "message": "No meaningful skills extracted from resume."
            }), 200

        # Get job recommendations
        recommendations = recommend_jobs(parsed_skills)
        print("[DEBUG] Job recommendations:", recommendations)

        return jsonify({
            "parsedSkills": parsed_skills,
            "recommendations": recommendations
        }), 200

    except Exception as e:
        print("[ERROR] Exception in /recommend:", str(e))
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
