import sys
import os
"""
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from resume_parser import extract_skills

sample = "
Experienced Python Developer with knowledge in data science, machine learning,
Flask APIs, and database systems like MongoDB and SQL.
"

print("Extracted Skills:", extract_skills(sample))
"""
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from model.recommender import recommend_jobs

skills = ['Python', 'Flask', 'APIs', 'MongoDB']
results = recommend_jobs(skills)
for job in results:
    print(job)

