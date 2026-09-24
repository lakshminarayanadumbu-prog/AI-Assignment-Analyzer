import language_tool_python

def check_grammar(text):

    tool = language_tool_python.LanguageToolPublicAPI("en-US")

    matches = tool.check(text)

    grammar_errors = len(matches)

    suggestions = []

    for match in matches[:5]:
        suggestions.append(match.message)

    tool.close()

    return grammar_errors, suggestions

from .preprocessing import clean_text, get_words
from sklearn.feature_extraction.text import TfidfVectorizer


def detect_sections(text):

    text_lower = text.lower()

    section_names = {
        "Introduction": ["introduction", "background"],
        "Methodology": ["methodology", "method", "approach"],
        "Results": ["results", "findings"],
        "Discussion": ["discussion"],
        "Conclusion": ["conclusion", "summary"],
        "References": ["references", "bibliography"]
    }

    detected = []

    for section, keywords in section_names.items():

        for keyword in keywords:

            if keyword in text_lower:
                detected.append(section)
                break

    if not detected:
        detected.append("No sections detected")

    return detected


def analyze_text(text):

    # Clean the text
    cleaned_text = clean_text(text)

    # Get words
    words = get_words(text)

    # Word count
    word_count = len(words)

    # -----------------------------
    # TF-IDF Keyword Extraction
    # -----------------------------

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5
    )

    tfidf_matrix = vectorizer.fit_transform([cleaned_text])

    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(zip(feature_names, scores))

    keyword_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    keywords = [
        word for word, score in keyword_scores
    ]

    # -----------------------------
    # Section Detection
    # -----------------------------

    sections = detect_sections(text)
    # -----------------------------
    # Confidence Score
    # -----------------------------

    confidence = 70

    if len(sections) > 0 and sections[0] != "No sections detected":
        confidence += 10

    if len(keywords) >= 3:
        confidence += 10

    if word_count >= 50:
        confidence += 5

    # -----------------------------
    # Grammar Checking
    # -----------------------------

    grammar_errors, grammar_suggestions = check_grammar(text)

    if grammar_errors == 0:
        confidence += 5

    if confidence > 100:
        confidence = 100

    # -----------------------------
    # Readability
    # -----------------------------

    if word_count < 50:
        readability = "Easy"
    elif word_count < 150:
        readability = "Good"
    else:
        readability = "Advanced"

    # -----------------------------
    # Quality Score
    # -----------------------------

    quality_score = 50

    # Word count
    if word_count >= 50:
     quality_score += 10

    if word_count >= 100:
     quality_score += 10

    # Keywords
     if len(keywords) >= 3:
      quality_score += 10

    # Assignment sections
     if len(sections) >= 3:
      quality_score += 10

    # Grammar
    if grammar_errors == 0:
     quality_score += 10
    elif grammar_errors <= 3:
     quality_score += 5

    # Maximum score
    if quality_score > 100:
     quality_score = 100

    # -----------------------------
    # Suggestions
    # -----------------------------

    suggestions = []

    if word_count < 50:
        suggestions.append(
        "Add more content to your assignment."
    )

    if "Introduction" not in sections:
     suggestions.append(
        "Add an Introduction section."
    )

    if "Conclusion" not in sections:
     suggestions.append(
        "Add a Conclusion section."
    )

    if "Methodology" not in sections:
     suggestions.append(
        "Consider adding a Methodology section."
    )

    if grammar_errors > 3:
     suggestions.append(
        "Review the grammar and spelling errors."
    )

    if len(keywords) < 3:
     suggestions.append(
        "Include more important technical keywords."
    )

    if len(suggestions) == 0:
     suggestions.append(
        "Good structure. Consider adding more examples and details."
    )
    # -----------------------------
    # Return Results
    # -----------------------------
    
        # Detailed score breakdown

    grammar_score = 10
    if grammar_errors > 0:
        grammar_score = max(0, 10 - grammar_errors)

    structure_score = min(len(sections) * 2, 10)

    keyword_score = min(len(keywords) * 2, 10)

    content_score = 5

    if word_count >= 100:
        content_score = 8

    if word_count >= 250:
        content_score = 10

    readability_score = 10

    if readability == "Easy":
        readability_score = 8
    elif readability == "Good":
        readability_score = 9

    return {
        "quality_score": quality_score,
        "confidence": confidence,
        "word_count": word_count,
        "readability": readability,
        "grammar_errors": grammar_errors,
        "grammar_score": grammar_score,
        "structure_score": structure_score,
        "keyword_score": keyword_score,
        "content_score": content_score,
        "readability_score": readability_score,
        "keywords": ", ".join(keywords),
        "sections": ", ".join(sections),
        "suggestions": " ".join(suggestions),
        "grammar_suggestions": grammar_suggestions
    }
    