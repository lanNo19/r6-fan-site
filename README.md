# Rainbow Six Siege Fan Application

**Deployed Version:** https://r6-fan-site.onrender.com

## Table of Contents
1.  [About](#about)
2.  [Installation and Launch](#installation-and-launch)
3.  [Design Process](#design-process)
4.  [Unique Approach](#unique-approach)
5.  [Tradeoffs](#tradeoffs)
6.  [Limitations](#limitations)
7.  [Tech Stack](#tech-stack)

## 1. About

The Rainbow Six Siege Fan Application is a web platform for enthusiasts of Tom Clancy's Rainbow Six Siege. It offers detailed information on in-game operators and maps, and features an AI-powered "Lineup Suggestor" to help players strategize team compositions. This app serves as a valuable resource for both new and experienced players.

## 2. Installation and Launch

To run this project locally:

### Prerequisites

* Python 3.8+
* `pip`, Git
* A Supabase project (PostgreSQL database)
* A Google API Key with Gemini 2.0 Flash access

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd r6-fan-site
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up Environment Variables:**
    Create a `.env` file in the project root (`r6-fan-site/`) with your Supabase and Google API credentials:
    ```
    SUPABASE_URL="YOUR_SUPABASE_URL"
    SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"
    user="YOUR_SUPABASE_DB_USER"
    password="YOUR_SUPABASE_DB_PASSWORD"
    host="YOUR_SUPABASE_DB_HOST"
    port="5432"
    dbname="YOUR_SUPABASE_DB_NAME"
    LLM_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
    ```
5.  **Set up Supabase Database Schema:**
    Manually create `operators`, `maps`, and `game_info` tables in your Supabase SQL Editor as defined in the project's models.
6.  **Populate Database with Initial Data:**
    ```bash
    python populate_db.py
    python populate_maps.py
    python populate_game_info.py
    ```
    *(Consider `TRUNCATE TABLE <table_name> RESTART IDENTITY;` in Supabase before populating for clean data.)*
7.  **Run the Flask application:**
    ```bash
    export FLASK_APP=r6_fan_app  # Windows: set FLASK_APP=r6_fan_app
    flask run
    ```
    Access at `http://127.0.0.1:5000/`.

## 3. Design Process

The application's development followed an iterative process. It began with establishing a modular Flask structure, integrating the database, and building core informational pages for operators and maps. Subsequent iterations focused on enhancing user experience through client-side JavaScript for dynamic filtering and interactive UI components (like the accordion). The integration of the LLM-powered lineup suggestor was a key later phase, adding an advanced, intelligent feature. Emphasis was consistently placed on ensuring a responsive and intuitive user interface.

## 4. Unique Approach

The standout feature is the **LLM-Powered Lineup Suggestor**, which leverages the Google Gemini 2.0 Flash API to provide dynamic, context-aware operator recommendations based on user-described in-game situations. This moves beyond static data, offering intelligent strategic insights. Additionally, the project utilizes a **modular Flask package structure** for improved maintainability and scalability, separating concerns into distinct `__init__.py`, `routes.py`, and `models.py` files within a dedicated application package.

## 5. Tradeoffs

* **Mock Map Site Data:** For simplicity and rapid development, map site data is currently mocked within the application code rather than being stored in a more complex database schema.
* **Basic Search:** The global search uses a simple database `LIKE` query. A more advanced search solution (e.g., full-text search) was not implemented to keep the project scope focused.
* **Limited LLM Context:** The LLM prompt is concise for efficiency. More detailed in-game context could be provided for even more nuanced suggestions, but this would increase complexity and API latency.
* **No User Authentication:** The application is purely informational, omitting user authentication or personalized features to simplify development.

## 6. Limitations

* **Image Placeholders:** Operator portraits and map images are currently static files. A more robust solution for image serving (e.g., CDN integration) is not implemented.
* **LLM Latency:** Users may experience slight delays when using the Lineup Suggestor due to the external API call to the Gemini model.
* **Basic Error Handling:** While general error pages exist, more granular error logging and specific user feedback mechanisms could be enhanced for a production environment.
* **No Database Migrations:** Database schema changes currently require manual SQL commands. A migration tool (e.g., Flask-Migrate/Alembic) is not integrated.

## 7. Tech Stack

The chosen tech stack balances rapid development, flexibility, and powerful features:

* **Python/Flask:** For its speed, flexibility, and suitability for building web applications efficiently.
* **Flask-SQLAlchemy:** Simplifies database interactions through an ORM, abstracting raw SQL.
* **Supabase (PostgreSQL):** A managed PostgreSQL database solution that streamlines backend setup and offers scalability.
* **Google Gemini 2.0 Flash API:** Provides advanced AI capabilities for the core "Lineup Suggestor" feature, chosen for its balance of performance and cost.
* **Render.com:** A convenient and developer-friendly platform that facilitates seamless deployment of Python web services from Git.
* **HTML/CSS/JavaScript:** Standard web technologies providing complete control over the frontend user experience and responsiveness.