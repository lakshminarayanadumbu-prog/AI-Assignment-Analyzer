const analyzeButton = document.getElementById("analyzeButton");

analyzeButton.addEventListener("click", async function () {

    const text = document.getElementById("assignmentText").value;

    if (text.trim() === "") {
        alert("Please enter your assignment text.");
        return;
    }

    try {

        const response = await fetch("/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

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