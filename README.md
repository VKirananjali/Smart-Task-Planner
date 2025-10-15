# Smart Task Planner

The Smart Task Planner is a web application that uses a locally-hosted Large Language Model (LLM) via **LM Studio** to break down a high-level goal into a detailed, actionable project plan. Simply provide a goal in natural language (e.g., "Launch a new website in 3 weeks"), and the AI will generate a structured plan complete with phases, tasks, dependencies, and timelines, all running on your own machine.

This version is designed to run completely offline, ensuring privacy and zero API costs.

-----

## Features

  * **100% Local & Private**: All AI processing is done on your machine using LM Studio. No data is sent to external cloud services.
  * **Natural Language Input**: Understands goals and timelines written in plain English.
  * **AI-Powered Task Generation**: Leverages a local LLM to create a logical and complete breakdown of tasks.
  * **Simple File Storage**: Saves all generated plans as easy-to-read `.json` files.
  * **RESTful API**: A clean backend API to handle requests and serve the generated plans.
  * **Simple Web Interface**: An intuitive frontend to input goals and view the formatted plan.

-----

## Tech Stack

  * **Backend**: Python, Flask
  * **AI Model Server**: [LM Studio](https://lmstudio.ai/) (running any GGUF-compatible model)
  * **AI Client Library**: `openai` (configured for a local endpoint)
  * **Storage**: Flat Files (.json)
  * **Frontend**: HTML, CSS, JavaScript (Fetch API)

-----

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

  * Python 3.8+
  * [LM Studio](https://lmstudio.ai/) installed on your machine.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/smart-task-planner.git
cd smart-task-planner
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment.

  * **Windows**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
  * **macOS / Linux**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 4. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
Flask
openai
python-dotenv
```

Then, install the packages from the file:

```bash
pip install -r requirements.txt
```

### 5. Configure LM Studio

1.  **Download a Model**: Open LM Studio. In the search tab (🔍), download a model suitable for JSON generation and instruction-following. Good options include models from `Meta Llama 3`, `Mistral`, or `Phi-3`.
2.  **Start the Server**: Go to the local server tab (↔️). Select the model you downloaded and click **Start Server**. This will expose an API endpoint at `http://localhost:1234/v1`.

### 6. Prepare the Project

1.  **Create Storage Directory**: In your project folder, create a directory to store the generated plans.
    ```bash
    mkdir saved_plans
    ```
2.  **Environment File**: Create a `.env` file. It can be empty, as no API keys are needed for this local setup.

### 7. Run the Application

Now, you can start the Flask server.

```bash
python app.py
```

The application will be running at `http://127.0.0.1:5000`. Open this URL in your browser to use the web interface. Make sure your LM Studio server is running in the background\!

-----

## API Usage

You can also interact directly with the API.

### Generate a New Plan

  * **Endpoint**: `POST /api/plan`
  * **Description**: Takes a natural language query and returns a structured project plan.
  * **Request Body**:
    ```json
    {
        "query": "Organize a community tech meetup in 2 months"
    }
    ```
  * **Example `curl` command**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"query": "Organize a community tech meetup in 2 months"}' http://127.0.0.1:5000/api/plan
    ```

### Retrieve All Saved Plans

  * **Endpoint**: `GET /api/plans`
  * **Description**: Retrieves a list of all previously generated plans from the `saved_plans` directory.

-----

## Project Structure

```
.
├── saved_plans/        # Directory for flat file storage
├── static/
│   └── scripts.js      # Frontend HTML, CSS, and JS
│   └── styles.css
├── templates/
│   └── index.html
├── .env                # Optional environment file
├── app.py              # Main Flask application logic
├── README.md           # You are here
└── requirements.txt    # Python dependencies
```
