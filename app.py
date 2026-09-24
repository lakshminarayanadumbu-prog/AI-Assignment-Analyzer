from flask import Flask, render_template, request, jsonify,send_file
from nlp.analyzer import analyze_text
from pypdf import PdfReader

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check if PDF was uploaded
    if "file" in request.files:

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "Please select a PDF file."
            }), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({
                "error": "Only PDF files are allowed."
            }), 400

        try:
            reader = PdfReader(file)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        except Exception as e:
            return jsonify({
                "error": "Could not read the PDF file."
            }), 400

    else:

        data = request.get_json()

        text = data.get("text", "")

    if not text.strip():
        return jsonify({
            "error": "No text found in the assignment."
        }), 400

    result = analyze_text(text)

    return jsonify(result)

@app.route("/download-report", methods=["POST"])
def download_report():

    data = request.get_json()

    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    report_path = "assignment_analysis_report.pdf"

    doc = SimpleDocTemplate(
        report_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("AI Assignment Analysis Report", styles["Title"])
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Quality Score: {data.get('quality_score', 0)}%",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Confidence: {data.get('confidence', 0)}%",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Word Count: {data.get('word_count', 0)}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Readability: {data.get('readability', '')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Grammar Issues: {data.get('grammar_errors', 0)}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph("Detailed Score Breakdown", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Grammar: {data.get('grammar_score', 0)}/10",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Structure: {data.get('structure_score', 0)}/10",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Keywords: {data.get('keyword_score', 0)}/10",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Content: {data.get('content_score', 0)}/10",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Readability: {data.get('readability_score', 0)}/10",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Keywords: {data.get('keywords', '')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Detected Sections: {data.get('sections', '')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Suggestions: {data.get('suggestions', '')}",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return send_file(
        report_path,
        as_attachment=True,
        download_name="AI_Assignment_Analysis_Report.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)