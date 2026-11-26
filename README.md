# BrandScope – AI Brand Mention & Sentiment Analyzer

BrandScope is an AI-powered application that analyzes AI-generated text to identify brand mentions, extract brand-specific opinions, and determine the overall sentiment expressed toward a target brand.

It uses Google's Gemini API for contextual brand detection and opinion extraction, while a Python-based sentiment engine calculates the final sentiment using an intensity-weighted scoring approach.

## Features

- **Brand Mention Detection:** Identifies whether a specified brand appears in AI-generated text.
- **Context Extraction:** Extracts the original sentences relevant to the target brand.
- **Opinion Extraction:** Identifies individual positive and negative opinions about the brand.
- **Intensity-Based Sentiment Analysis:** Assigns intensity values to extracted opinions and calculates an overall sentiment.
- **Five Sentiment Categories:** Positive, negative, neutral, neutral mixed, and not applicable.
- **Analysis History:** Stores previous analyses in an SQLite database.
- **Interactive Web Interface:** Provides a frontend for submitting text, viewing results, and managing analysis history.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| LLM | Google Gemini API |
| AI Integration | Google Gen AI SDK |
| Data Validation | Pydantic |
| Database | SQLite |
| ORM | SQLAlchemy |
| Testing | pytest |

## System Architecture

```text
              User
               |
               v
       Frontend (HTML/CSS/JS)
               |
               v
         FastAPI Backend
               |
               v
       Analysis Service
               |
               v
         Gemini API
               |
               v
    Structured Opinion Extraction
               |
               v
      Python Sentiment Engine
               |
               v
       Final Analysis Result
               |
          +----+----+
          |         |
          v         v
       SQLite    Frontend
       Database   Results
```

## Sentiment Analysis Methodology

BrandScope uses a hybrid LLM and rule-based approach.

### 1. Brand Detection

Gemini identifies whether the specified brand is mentioned in the supplied text. It also identifies relevant contextual sentences without paraphrasing the original content.

### 2. Opinion Extraction

If the brand is mentioned, Gemini extracts individual evaluative opinions directed toward that brand.

Each opinion contains:

- Opinion text
- Polarity: positive or negative
- Intensity: 1 or 2

Intensity levels:

| Intensity | Meaning |
|---|---|
| 1 | Moderate evaluation |
| 2 | Strong evaluation |

### 3. Sentiment Calculation

The backend calculates the total positive and negative opinion intensities.

Let:

- P = Sum of positive opinion intensities
- N = Sum of negative opinion intensities

For cases containing both positive and negative opinions, the normalized positive sentiment score is:

\[
S = \frac{P}{P+N}
\]

The final sentiment is determined using the following thresholds:

| Score | Sentiment |
|---|---|
| S < 0.4 | Negative |
| 0.4 ≤ S ≤ 0.6 | Neutral Mixed |
| S > 0.6 | Positive |

### 4. Special Cases

| Condition | Final Sentiment |
|---|---|
| Brand is not mentioned | Not Applicable |
| Brand is mentioned without evaluative opinions | Neutral |
| Only positive opinions exist | Positive |
| Only negative opinions exist | Negative |
| Both positive and negative opinions exist | Calculated using the normalized score |

**Important design decision:** Gemini is responsible for contextual understanding and structured opinion extraction. The final numerical sentiment score and sentiment classification are calculated by the Python backend. This separates language understanding from deterministic scoring logic.

## Project Structure

```text
brand_context_analyzer/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── analysis.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── llm/
│   │   ├── gemini_client.py
│   │   └── prompt.py
│   │
│   ├── schemas/
│   │   └── analysis.py
│   │
│   ├── services/
│   │   ├── analysis_service.py
│   │   └── database_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   └── evaluation_cases.json
│
├── .env.example
├── .gitignore
├── requirements.txt
├── init_db.py
└── test_database.py
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Google Gemini API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ThanishkaJ/ai-brand-mention-analyzer.git
cd ai-brand-mention-analyzer
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your actual Gemini API key.

**Security:** Never commit your `.env` file or expose your API key publicly.

### 5. Initialize the Database

```bash
python init_db.py
```

This creates the SQLite database and the required analysis table.

### 6. Start the Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### 7. Start the Frontend

Open another terminal from the project root:

```bash
python -m http.server 5500 --directory frontend
```

Open the application:

`http://127.0.0.1:5500`

Keep both servers running while using the application.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API is running |
| GET | `/health` | Backend health check |
| POST | `/api/analyze` | Analyzes brand mentions and sentiment |
| GET | `/api/history` | Retrieves previous analyses |
| GET | `/api/history/{analysis_id}` | Retrieves a specific analysis |
| DELETE | `/api/history/{analysis_id}` | Deletes an analysis |

### Example Analysis Request

```json
{
  "company": "Apple",
  "answer": "Apple produces excellent smartphones with impressive performance. However, its products are expensive compared to competitors."
}
```

## Evaluation

The project includes a manually annotated evaluation dataset containing 60 test cases across six categories:

- Direct positive mentions
- Direct negative mentions
- Competitor comparisons
- Mixed sentiment
- Neutral factual mentions
- Brand not mentioned

The dataset is used to evaluate brand mention detection, opinion extraction, and sentiment classification.

A separate model smoke test can be used to check the live Gemini integration.

## Limitations

- Sentiment quality depends on the accuracy of LLM-based opinion extraction.
- Opinion intensity is based on predefined annotation guidelines and may involve subjective judgments.
- The current implementation focuses on English-language text.
- The system analyzes the supplied text and does not independently verify the factual accuracy of AI-generated claims.
- Sentiment classification is based on extracted brand-specific opinions rather than general positive or negative wording.

## Future Improvements

- Expand evaluation with larger and more diverse datasets.
- Improve consistency in opinion intensity annotation.
- Add support for multiple languages.
- Introduce more detailed evaluation metrics.
- Deploy the application for public access.

## Author

**Thanishka**

B.Tech – Artificial Intelligence and Data Science

GitHub: https://github.com/ThanishkaJ

---

*BrandScope – Understanding how brands are represented in AI-generated responses.*