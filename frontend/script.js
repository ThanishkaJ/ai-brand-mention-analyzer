
const API_BASE_URL = "/api";

// DOM elements
const analysisForm = document.getElementById("analysisForm");
const companyInput = document.getElementById("companyInput");
const answerInput = document.getElementById("answerInput");
const analyzeButton = document.getElementById("analyzeButton");

const analysisSection = document.getElementById("analysisSection");
const historySection = document.getElementById("historySection");

const resultsSection = document.getElementById("resultsSection");
const historyList = document.getElementById("historyList");

const newAnalysisNav = document.getElementById("newAnalysisNav");
const historyNav = document.getElementById("historyNav");

const characterCount = document.getElementById("characterCount");
const toast = document.getElementById("toast");


// Utility: Display notifications
function showToast(message) {
    toast.textContent = message;
    toast.classList.remove("hidden");

    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}


// Utility: Create an HTML element safely
function createElement(tag, className, text = "") {
    const element = document.createElement(tag);

    if (className) {
        element.className = className;
    }

    element.textContent = text;

    return element;
}


// Navigation
function showAnalysisPage() {
    analysisSection.classList.remove("hidden");
    historySection.classList.add("hidden");

    newAnalysisNav.classList.add("active");
    historyNav.classList.remove("active");

    document.getElementById("pageTitle").textContent = "Brand Analysis";
    document.getElementById("currentPage").textContent = "New Analysis";
}


async function showHistoryPage() {
    analysisSection.classList.add("hidden");
    historySection.classList.remove("hidden");

    newAnalysisNav.classList.remove("active");
    historyNav.classList.add("active");

    document.getElementById("pageTitle").textContent = "Analysis History";
    document.getElementById("currentPage").textContent = "Analysis History";

    await loadHistory();
}


newAnalysisNav.addEventListener("click", showAnalysisPage);
historyNav.addEventListener("click", showHistoryPage);


// Character counter
answerInput.addEventListener("input", () => {
    characterCount.textContent =
        `${answerInput.value.length} / 20000 characters`;
});


// Clear form
analysisForm.addEventListener("reset", () => {
    resultsSection.classList.add("hidden");
    characterCount.textContent = "0 / 20000 characters";
});


// Analyze brand
analysisForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const company = companyInput.value.trim();
    const answer = answerInput.value.trim();

    if (!company || !answer) {
        showToast("Please enter both the brand and AI-generated response.");
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                company: company,
                answer: answer
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Unable to analyze the brand."
            );
        }

        displayAnalysis(result);

        showToast("Brand analysis completed successfully!");

    } catch (error) {
        console.error("Analysis error:", error);

        showToast(error.message || "Unable to connect to the backend.");

    } finally {
        analyzeButton.disabled = false;
        analyzeButton.innerHTML = "<span>✦</span> Analyze Brand";
    }
});


// Display analysis results
function displayAnalysis(result) {
    resultsSection.classList.remove("hidden");

    document.getElementById("resultCompany").textContent =
        result.company;

    const sentimentValue = document.getElementById("sentimentValue");

    sentimentValue.textContent =
        result.sentiment.replace("_", " ");

    const sentimentCard = document.getElementById("sentimentCard");

    sentimentCard.className = "sentiment-card";
    sentimentCard.classList.add(result.sentiment);

    const sentimentDescriptions = {
        positive: "The brand received positive evaluations.",
        negative: "The brand received negative evaluations.",
        neutral: "The brand was mentioned without clear positive or negative opinions.",
        neutral_mixed: "The brand received both positive and negative evaluations.",
        not_applicable: "The brand was not mentioned in the response."
    };

    document.getElementById("sentimentDescription").textContent =
        sentimentDescriptions[result.sentiment] || "";

    document.getElementById("scoreValue").textContent =
        result.sentiment_score === null
            ? "—"
            : Number(result.sentiment_score).toFixed(4);

    document.getElementById("mentionValue").textContent =
        result.mentioned ? "Brand mentioned" : "Brand not mentioned";

    document.getElementById("explanationValue").textContent =
        result.explanation;

    // Relevant context
    const contextList = document.getElementById("contextList");
    contextList.replaceChildren();

    if (result.relevant_context.length === 0) {
        contextList.appendChild(
            createElement("p", "empty-message", "No relevant context found.")
        );
    } else {
        result.relevant_context.forEach((context) => {
            contextList.appendChild(
                createElement("div", "context-item", context)
            );
        });
    }

    // Extracted opinions
    const opinionsList = document.getElementById("opinionsList");
    opinionsList.replaceChildren();

    if (result.opinions.length === 0) {
        opinionsList.appendChild(
            createElement("p", "empty-message", "No evaluative opinions found.")
        );
    } else {
        result.opinions.forEach((opinion) => {
            const item = createElement("div", "opinion-item");

            const opinionText = createElement(
                "div",
                "opinion-text",
                opinion.opinion
            );

            const metadata = createElement("div", "opinion-meta");

            metadata.appendChild(
                createElement(
                    "span",
                    `polarity-tag ${opinion.polarity}`,
                    opinion.polarity
                )
            );

            metadata.appendChild(
                createElement(
                    "span",
                    "intensity-tag",
                    `Intensity ${opinion.intensity}`
                )
            );

            item.append(opinionText, metadata);
            opinionsList.appendChild(item);
        });
    }

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// Load analysis history
async function loadHistory() {
    historyList.replaceChildren();

    historyList.appendChild(
        createElement("p", "empty-message", "Loading history...")
    );

    try {
        const response = await fetch(`${API_BASE_URL}/history`);

        const records = await response.json();

        if (!response.ok) {
            throw new Error(records.detail || "Unable to load history.");
        }

        historyList.replaceChildren();

        if (records.length === 0) {
            historyList.appendChild(
                createElement("p", "empty-message", "No previous analyses found.")
            );
            return;
        }

        records.forEach((record) => {
            const item = createElement("div", "history-item");

            const details = createElement("div", "history-details");

            details.appendChild(
                createElement("h4", "", record.company)
            );

            details.appendChild(
                createElement("p", "", `Analysis ID: ${record.id}`)
            );

            details.appendChild(
                createElement(
                    "p",
                    "",
                    new Date(record.created_at).toLocaleString()
                )
            );

            details.appendChild(
                createElement(
                    "span",
                    "history-sentiment",
                    record.sentiment.replace("_", " ")
                )
            );

            const actions = createElement("div", "history-actions");

            const viewButton = createElement("button", "", "View");
            viewButton.type = "button";
            viewButton.addEventListener("click", () => {
                viewAnalysis(record.id);
            });

            const deleteButton = createElement(
                "button",
                "delete-button",
                "Delete"
            );

            deleteButton.type = "button";
            deleteButton.addEventListener("click", () => {
                deleteAnalysis(record.id);
            });

            actions.append(viewButton, deleteButton);
            item.append(details, actions);

            historyList.appendChild(item);
        });

    } catch (error) {
        console.error("History error:", error);

        historyList.replaceChildren();

        historyList.appendChild(
            createElement("p", "empty-message", error.message)
        );
    }
}


// Retrieve one analysis by ID
async function viewAnalysis(analysisId) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/history/${analysisId}`
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Analysis not found.");
        }

        showAnalysisPage();
        displayAnalysis(result);

    } catch (error) {
        console.error("Retrieval error:", error);
        showToast(error.message);
    }
}


// Delete analysis
async function deleteAnalysis(analysisId) {
    const confirmed = confirm(
        `Are you sure you want to delete analysis #${analysisId}?`
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/history/${analysisId}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to delete analysis.");
        }

        showToast("Analysis deleted successfully!");

        await loadHistory();

    } catch (error) {
        console.error("Deletion error:", error);
        showToast(error.message);
    }
}


// Refresh history
document.getElementById("refreshHistory").addEventListener(
    "click",
    loadHistory
);


// Check backend health
async function checkBackend() {
    const statusText = document.querySelector(".sidebar-info small");
    const statusDot = document.querySelector(".status-dot");

    try {
        const response = await fetch("/health");

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        statusText.textContent = "Backend connected";
        statusDot.style.background = "#36d6a0";

    } catch (error) {
        statusText.textContent = "Backend disconnected";
        statusDot.style.background = "#e05266";
    }
}


// Initial application setup
document.addEventListener("DOMContentLoaded", () => {
    showAnalysisPage();
    checkBackend();
});
