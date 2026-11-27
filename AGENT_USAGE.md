# Coding Agent Usage Documentation

This document describes how AI tools were used during the development of the AI-Powered Brand Mention & Sentiment Analyzer, including the work they assisted with, the verification performed, and the changes made manually.

## 1. Agents Used

### ChatGPT – Code Generation and Development Assistance

ChatGPT was used as the primary coding assistant throughout development.

Its responsibilities included:
- Generating and refining Python implementation code.
- Assisting with FastAPI backend development.
- Helping develop and refine the Gemini API integration and analysis prompt.
- Assisting with database models and SQLAlchemy operations.
- Supporting frontend implementation and backend integration.
- Identifying bugs and suggesting debugging approaches.
- Helping configure and troubleshoot deployment.

### Claude – Code Understanding and Technical Explanation

Claude was used primarily to understand the implementation and review technical concepts.

Its responsibilities included:
- Explaining generated code and its execution flow.
- Clarifying the application architecture.
- Explaining the interaction between the frontend, FastAPI backend, Gemini API, and database.
- Helping understand implementation decisions and technical trade-offs.
- Supporting the understanding of errors and debugging approaches.

The two tools served different purposes: ChatGPT primarily assisted with generation, while Claude primarily assisted with understanding.

## 2. What They Generated

AI coding assistance was used during different stages of development.

The generated and AI-assisted implementation work included:

- **Project implementation:** Initial code drafts and implementation guidance for organizing the application.
- **Backend:** Assistance with FastAPI endpoints and request-response handling.
- **AI integration:** Assistance with the Gemini API integration and the prompt used for brand analysis.
- **Database:** Assistance with SQLAlchemy models, database operations, and analysis persistence.
- **Frontend:** Assistance with frontend code and communication with the backend API.
- **Debugging:** Suggested fixes and troubleshooting approaches for errors encountered during development.
- **Deployment:** Assistance with deployment configuration and resolving deployment issues.

AI-generated code was treated as development assistance rather than automatically accepted output. Implementation decisions and changes were reviewed during development.

## 3. What Was Verified

The application was tested and reviewed during development to check whether its major components worked as expected.

Verification activities included:

### Backend and API Behaviour
- Checked whether the FastAPI application started successfully.
- Verified communication between the frontend and the `/api/analyze` endpoint.
- Checked whether analysis requests reached the backend and produced responses.
- Verified that the Gemini integration returned analysis results.

### Brand Analysis Behaviour
- Checked brand mention detection.
- Examined whether irrelevant brand references were correctly distinguished from relevant mentions.
- Reviewed the generated sentiment and contextual information.
- Checked the explanation returned for an analysis.

### Database Behaviour
- Verified that analysis records could be saved.
- Checked database initialization and the creation of required tables.
- Verified that the analysis history functionality worked.

### Deployment
- Verified that the application was accessible through its Render deployment.
- Checked the deployed API and frontend behaviour.
- Tested brand analysis after correcting the database initialization issue.

The repository also contains test-related scripts, including `test_brand_analysis.py`, `test_gemini_connection.py`, `test_prompt.py`, and `check_evaluation_dataset.py`.

The existence of these scripts should not be interpreted as evidence that every test or evaluation was successfully executed.

## 4. What Was Changed Manually

AI-generated suggestions were reviewed and adjusted during development. The following are examples of implementation and debugging decisions made during the project.

### Database Initialization Fix

During deployment, the application returned an HTTP 500 error when saving an analysis.

The traceback revealed:

```text
sqlite3.OperationalError: no such table: analyses
```

The analysis itself had been generated, but the required SQLite table had not been initialized.

The deployment configuration was corrected to execute the database initialization script before starting the FastAPI server:

```bash
python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This ensured that the required SQLAlchemy tables were created before the application started accepting requests.

### Relevance Handling

An important distinction was maintained between simply detecting a brand name and determining whether the content is actually relevant to that brand.

For example, when the requested brand is Microsoft but the provided text discusses Apple, the system should not classify the content as a relevant Microsoft mention merely because another brand is present.

This behaviour was checked during analysis testing.

### Implementation Review and Refinement

Generated code and suggestions were reviewed against the actual application requirements. Changes were made where necessary to resolve integration issues, improve application behaviour, and ensure that the frontend, backend, AI service, and database worked together.

### Final Responsibility

AI tools assisted with code generation, explanations, and debugging. The final implementation, testing decisions, integration, and deployment verification were reviewed and carried out by the developer.

AI-generated output was not treated as automatically correct.