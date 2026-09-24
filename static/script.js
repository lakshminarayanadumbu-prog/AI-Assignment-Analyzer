const pdfFile = document.getElementById("pdfFile");
const assignmentText = document.getElementById("assignmentText");

// When PDF is selected
pdfFile.addEventListener("change", function () {

    if (pdfFile.files.length > 0) {
        assignmentText.value = "";
        assignmentText.disabled = true;
    } else {
        assignmentText.disabled = false;
    }

});

// When user starts typing text
assignmentText.addEventListener("input", function () {

    if (assignmentText.value.trim() !== "") {
        pdfFile.value = "";
        pdfFile.disabled = true;
    } else {
        pdfFile.disabled = false;
    }

});
const analyzeButton = document.getElementById("analyzeButton");

analyzeButton.addEventListener("click", async function () {

    const text = document.getElementById("assignmentText").value;
    const pdfFile = document.getElementById("pdfFile").files[0];

    if (text.trim() === "" && !pdfFile) {
        alert("Please enter assignment text or upload a PDF.");
        return;
    }

    try {

        let response;

        // If PDF is selected
        if (pdfFile) {

            const formData = new FormData();
            formData.append("file", pdfFile);

            response = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

        } else {

            // If text is entered
            response = await fetch("/analyze", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            });
        }

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("qualityScore").textContent =
            data.quality_score + "%";

        document.getElementById("qualityProgress").style.width =
            data.quality_score + "%";

        document.getElementById("confidenceScore").textContent =
            data.confidence + "%";

        document.getElementById("confidenceProgress").style.width =
            data.confidence + "%";

        document.getElementById("wordCount").textContent =
            data.word_count;

        document.getElementById("readability").textContent =
            data.readability;

        document.getElementById("grammarErrors").textContent =
            data.grammar_errors;

        document.getElementById("keywords").textContent =
            data.keywords;

        document.getElementById("sections").textContent =
            data.sections;

        document.getElementById("suggestions").textContent =
            data.suggestions;
        
        // Detailed score breakdown

        document.getElementById("grammarScore").textContent =
         data.grammar_score + "/10";

        document.getElementById("grammarProgress").style.width =
          (data.grammar_score * 10) + "%";


        document.getElementById("structureScore").textContent =
          data.structure_score + "/10";

        document.getElementById("structureProgress").style.width =
          (data.structure_score * 10) + "%";


        document.getElementById("keywordScore").textContent =
          data.keyword_score + "/10";

        document.getElementById("keywordProgress").style.width =
          (data.keyword_score * 10) + "%";


        document.getElementById("contentScore").textContent =
           data.content_score + "/10";

        document.getElementById("contentProgress").style.width =
           (data.content_score * 10) + "%";


        document.getElementById("readabilityScore").textContent =
          data.readability_score + "/10";

        document.getElementById("readabilityProgress").style.width =
           (data.readability_score * 10) + "%";

        if (data.grammar_suggestions.length > 0) {

            document.getElementById("grammarSuggestions").textContent =
                data.grammar_suggestions.join(" ");

        } else {

            document.getElementById("grammarSuggestions").textContent =
                "No grammar issues found.";

        }

    } catch (error) {

        console.error(error);

        alert("Something went wrong while analyzing the assignment.");
    }

});
const downloadReportButton =
    document.getElementById("downloadReportButton");

downloadReportButton.addEventListener("click", async function () {

    const response = await fetch("/download-report", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            quality_score:
                document.getElementById("qualityScore").textContent.replace("%", ""),

            confidence:
                document.getElementById("confidenceScore").textContent.replace("%", ""),

            word_count:
                document.getElementById("wordCount").textContent,

            readability:
                document.getElementById("readability").textContent,

            grammar_errors:
                document.getElementById("grammarErrors").textContent,

            grammar_score:
                document.getElementById("grammarScore").textContent.replace("/10", ""),

            structure_score:
                document.getElementById("structureScore").textContent.replace("/10", ""),

            keyword_score:
                document.getElementById("keywordScore").textContent.replace("/10", ""),

            content_score:
                document.getElementById("contentScore").textContent.replace("/10", ""),

            readability_score:
                document.getElementById("readabilityScore").textContent.replace("/10", ""),

            keywords:
                document.getElementById("keywords").textContent,

            sections:
                document.getElementById("sections").textContent,

            suggestions:
                document.getElementById("suggestions").textContent
        })
    });

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "AI_Assignment_Analysis_Report.pdf";

    document.body.appendChild(link);

    link.click();

    link.remove();

    window.URL.revokeObjectURL(url);

});