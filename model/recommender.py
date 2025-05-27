# model/recommender.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load job dataset
def load_jobs(file_path="model/job_data.csv"):
    """
    Loads job data CSV into a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"job_data.csv not found at {file_path}")
    
    df = pd.read_csv(file_path)
    df["requiredSkills"] = df["requiredSkills"].apply(lambda x: " ".join(eval(x)))
    return df


def recommend_jobs(user_skills, top_n=5):
    """
    Recommends jobs based on similarity between user skills and job requirements.

    Args:
        user_skills (List[str]): Skills parsed from resume.
        top_n (int): Number of top jobs to recommend.

    Returns:
        List[Dict]: List of recommended jobs with jobID, title, and score.
    """
    job_df = load_jobs()

    # Combine job skills with user input to build corpus
    job_texts = job_df["requiredSkills"].tolist()
    user_text = " ".join(user_skills)
    corpus = job_texts + [user_text]

    # Vectorize text using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Compute cosine similarity
    user_vector = tfidf_matrix[-1]
    job_vectors = tfidf_matrix[:-1]
    similarities = cosine_similarity(user_vector, job_vectors).flatten()

    # Append similarity scores to the DataFrame
    job_df["score"] = similarities

    # Return top N recommended jobs
    top_matches = job_df.sort_values(by="score", ascending=False).head(top_n)
    return top_matches[["jobID", "title", "score"]].to_dict(orient="records")
