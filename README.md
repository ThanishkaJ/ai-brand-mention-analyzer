# AirMeet – AI-Powered Brand Mention & Sentiment Analyzer

AirMeet is an AI-powered brand mention analysis platform that helps users understand how brands are represented in textual content. It uses Google's Gemini API to identify brand mentions, determine relevance, analyze sentiment, and extract contextual opinions.

The application provides an interactive interface for analyzing brand mentions and maintaining a history of previously performed analyses.

**Live Application:** https://ai-brand-mention-analyzer.onrender.com

**GitHub Repository:** https://github.com/ThanishkaJ/ai-brand-mention-analyzer

---

## 1. Problem Statement

Brands are frequently discussed across digital platforms, articles, reviews, and other forms of textual content. However, identifying whether a particular brand is mentioned, understanding the context of the mention, and determining the associated sentiment can be challenging when performed manually.

AirMeet addresses this problem through an AI-powered analysis system that processes textual content and extracts meaningful brand-related insights.

## 2. Key Features

- **AI-Powered Brand Analysis:** Uses Google's Gemini API to analyze textual content.
- **Brand Mention Detection:** Identifies whether the requested brand appears in the provided text.
- **Relevance Detection:** Determines whether the content is actually relevant to the requested brand.
- **Sentiment Analysis:** Identifies the sentiment associated with a relevant brand mention.
- **Sentiment Scoring:** Stores sentiment-related scores where applicable.
- **Context Extraction:** Extracts relevant contextual information surrounding brand mentions.
- **Opinion Extraction:** Identifies opinions expressed about the brand.
- **Analysis Explanation:** Provides an explanation supporting the analysis result.
- **Analysis History:** Saves previous analyses and allows users to review them.
- **Interactive Dashboard:** Provides a user-friendly interface for submitting content and viewing results.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI Integration | Google Gemini API |
| AI SDK | Google Gen AI SDK |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| ASGI Server | Uvicorn |
| Deployment | Render |
| Version Control | Git, GitHub |

## 4. System Architecture

The application follows a frontend-backend architecture.

### Workflow

1. The user enters a brand name and textual content through the frontend.
2. The frontend sends the analysis request to the FastAPI backend.
3. The backend processes the request and invokes the Gemini API.
4. Gemini analyzes the content and generates structured brand-related insights.
5. The backend processes the response and prepares the analysis result.
6. SQLAlchemy handles database operations and stores the analysis in SQLite.
7. The frontend displays the analysis results.
8. Previously stored analyses can be accessed through the history interface.

### Architecture Overview

```text
              USER
                |
                v
       FRONTEND INTERFACE
         HTML / CSS / JS
                |
                v
          FASTAPI BACKEND
                |
                v
         ANALYSIS SERVICE
                |
                v
          GOOGLE GEMINI
                |
                v
       STRUCTURED AI RESPONSE
                |
                v
        RESULT PROCESSING
                |
                v
       SQLALCHEMY ORM
                |
                v
          SQLITE DATABASE
                |
                v
       ANALYSIS HISTORY
```

## 5. Analysis Output

For each submitted analysis, AirMeet maintains information such as:

| Field | Description |
|---|---|
| Company | Brand selected for analysis |
| Answer | AI-generated analysis response |
| Mentioned | Indicates whether the brand was mentioned |
| Sentiment | Identified sentiment category |
| Sentiment Score | Associated sentiment score, when applicable |
| Relevant Context | Context extracted from the content |
| Opinions | Opinions identified during analysis |
| Explanation | Explanation supporting the result |
| Created At | Date and time of analysis |

The system also handles irrelevant mentions separately. For example, mentioning Apple in a discussion about Microsoft does not automatically qualify as a relevant Microsoft mention.

## 6. Project Structure

The backend follows a modular organization that separates API routes, database operations, and business logic.

```text
ai-brand-mention-analyzer/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── analysis.py
│   │
│   ├── services/
│   │   └── database_service.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   └── main.py
│
├── init_db.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

*Note: This is a simplified representation of the main application components. Additional frontend and backend files are maintained in the repository.*

## 7. Local Installation and Setup

### Prerequisites

- Python 3.10 or later (use a version compatible with the pinned dependencies).
- Git.
- Google Gemini API key.

### Step 1: Clone the repository

```bash
git clone https://github.com/ThanishkaJ/ai-brand-mention-analyzer.git

cd ai-brand-mention-analyzer
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root and configure your Gemini API key.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Use the exact environment variable name expected by the application's configuration.

Never commit API keys or other sensitive credentials to GitHub.

### Step 5: Initialize the database

Run:

```bash
python init_db.py
```

This initializes the SQLite database and creates the tables defined by the SQLAlchemy models.

### Step 6: Start the backend

```bash
uvicorn app.main:app --reload
```

The application should be accessible at:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 8. Database Management

AirMeet uses SQLite for storing analysis results.

SQLAlchemy acts as the Object Relational Mapper (ORM), allowing Python application code to interact with database tables through models rather than writing every SQL query manually.

The database initialization script uses:

```python
Base.metadata.create_all(bind=engine)
```

This creates database tables that do not already exist.

The analysis history feature uses the stored records to retrieve previously performed analyses.

## 9. Deployment

AirMeet is deployed using Render.

**Live URL:** https://ai-brand-mention-analyzer.onrender.com

### Deployment Configuration

| Setting | Configuration |
|---|---|
| Hosting Platform | Render |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Application Server | Uvicorn |
| Backend Framework | FastAPI |

### Deployment Environment Variables

Configure the required Gemini API key in:

Render Dashboard → Web Service → Environment.

Add the environment variable expected by the application and provide its corresponding API key.

### Database Initialization During Deployment

The deployment start command executes the database initialization script before starting the FastAPI server.

```bash
python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This ensures that the required database tables are created before the application begins processing requests.

**Storage consideration:** The deployed application currently uses SQLite. Render's default filesystem is ephemeral, so database records may not persist across service restarts or redeployments. Persistent storage or PostgreSQL can be considered for future improvements.

## 10. Error Handling

The application includes error handling for failures during analysis and backend processing.

Potential failure scenarios include:

- Gemini API request failures.
- Invalid or unexpected AI responses.
- Database operation failures.
- Invalid user inputs.
- Unexpected backend exceptions.

The backend returns appropriate error responses when an analysis cannot be completed.

## 11. Future Enhancements

Potential improvements include:

- Persistent database storage using PostgreSQL.
- Analysis of multiple brands within the same content.
- Sentiment trend visualization over time.
- Brand comparison and competitor analysis.
- Advanced analytics and reporting.
- Exporting analysis results.
- User authentication and personalized analysis history.

## 12. Conclusion

AirMeet demonstrates how Generative AI can be integrated into a web application to automate brand mention detection, contextual relevance analysis, and sentiment extraction.

By combining Google's Gemini API, FastAPI, SQLAlchemy, and SQLite, the application provides an integrated platform for analyzing brand-related textual content and reviewing previous analysis results.

The project is deployed and available as a web application.

---

**Developed by:** Thanishka  
**Project:** AI-Powered Brand Mention & Sentiment Analyzer