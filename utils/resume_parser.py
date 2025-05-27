# utils/resume_parser.py

import spacy
from typing import List
from skills_list import COMMON_SKILLS

nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str) -> List[str]:
    """
    Extract actual known skills from resume using a skills dictionary match.
    """
    doc = nlp(text.lower())
    found_skills = set()

    for token in doc:
        if token.text in COMMON_SKILLS:
            found_skills.add(token.text)

    # Also try 2-word phrases (e.g., "machine learning")
    phrases = [chunk.text for chunk in doc.noun_chunks if chunk.text in COMMON_SKILLS]
    found_skills.update(phrases)

    return sorted(found_skills)
