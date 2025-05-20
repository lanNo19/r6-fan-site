# Rainbow Six Siege Fan Application

## Table of Contents
1.  [About](#about)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Setup and Installation (Local Development)](#setup-and-installation-local-development)
5.  [Deployment (Render)](#deployment-render)
6.  [Design and Development Process](#design-and-development-process)
7.  [Unique Approaches & Methodologies](#unique-approaches--methodologies)
8.  [Trade-offs Made](#trade-offs-made)
9.  [Known Issues & Limitations](#known-issues--limitations)
10. [Why This Tech Stack?](#why-this-tech-stack)
11. [Usage](#usage)
12. [Contributing](#contributing)
13. [License](#license)

## 1. About

The Rainbow Six Siege Fan Application is a web-based platform designed for enthusiasts of the popular tactical shooter, Tom Clancy's Rainbow Six Siege. It provides a centralized hub to explore detailed information about in-game operators and maps, and offers a unique "Lineup Suggestor" feature powered by a Large Language Model (LLM) to help players strategize their team compositions.

This application aims to be a valuable resource for both new players looking to understand core mechanics and experienced players seeking strategic insights.

## 2. Features

* **Operator Database:** Browse a comprehensive list of Rainbow Six Siege operators, categorized by Attacker and Defender. Each operator has a dedicated detail page with information on their ability, secondary gadgets, armor, speed, role, short bio, and strategic synergies/counters.
* **Map Database:** Explore various in-game maps with descriptions and key defender sites.
* **Game Information:** An interactive accordion-style section providing essential game mechanics, general tips, recommended content creators, and developer information, perfect for new players.
* **Lineup Suggestor (LLM-Powered):** Get intelligent operator suggestions for specific maps, defender sites, and team compositions (solo queue vs. team play), based on a described in-game situation. This feature leverages the Gemini 2.0 Flash model.
* **Global Search:** Easily find operators from any page using the integrated search bar.
* **Responsive Design:** Optimized for viewing on various devices (desktop, tablet, mobile).

## 3. Technologies Used

* **Backend:**
    * **Flask:** Python web framework for building the application.
    * **Flask-SQLAlchemy:** ORM for interacting with the PostgreSQL database.
    * **Supabase:** Backend-as-a-Service providing PostgreSQL database and API.
    * **`python-dotenv`:** For managing environment variables locally.
    * **`requests`:** For making HTTP requests to the Gemini API.
    * **`gunicorn`:** WSGI HTTP Server for production deployment.
* **Frontend:**
    * **HTML5:** Structure of web pages.
    * **CSS3:** Styling and responsive design.
    * **JavaScript:** Client-side interactivity (e.g., operator filtering, map site population, accordion).
* **AI/ML:**
    * **Google Gemini 2.0 Flash API:** Powers the "Lineup Suggestor" feature.
* **Deployment:**
    * **Render.com:** Cloud platform for deploying the Flask web service.

## 4. Setup and Installation (Local Development)

To run this project locally, follow these steps:

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)
* Git
* A Supabase project with a PostgreSQL database.
* A Google API Key with access to the Gemini 2.0 Flash model.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd r6-fan-site
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory of your project (where `Procfile` and `r6_fan_app` folder are located). Add the following variables, replacing the placeholders with your actual Supabase and Google API credentials:

    ```
    SUPABASE_URL="YOUR_SUPABASE_URL"
    SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"
    user="YOUR_SUPABASE_DB_USER"
    password="YOUR_SUPABASE_DB_PASSWORD"
    host="YOUR_SUPABASE_DB_HOST"
    port="5432" # Usually 5432 for Supabase PostgreSQL
    dbname="YOUR_SUPABASE_DB_NAME"
    LLM_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
    ```
    * You can find your Supabase URL and Key in your Supabase project settings under "API".
    * Database credentials are under "Database" -> "Connection String" (look for `host`, `user`, `password`, `dbname`).
    * Your Google API Key can be obtained from the Google AI Studio or Google Cloud Console.

5.  **Set up Supabase Database Schema:**
    Ensure your Supabase database has the following tables and columns. You can use the Supabase SQL Editor to create them:

    * **`operators` table:**
        ```sql
        CREATE TABLE operators (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            side TEXT NOT NULL,
            ability TEXT NOT NULL,
            secondary_gadgets TEXT,
            armor INTEGER,
            speed INTEGER,
            role TEXT,
            short_bio TEXT,
            synergy_examples TEXT,
            counter_examples TEXT,
            solo_friendly BOOLEAN
        );
        ```
    * **`maps` table:**
        ```sql
        CREATE TABLE maps (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            image_url TEXT NOT NULL,
            defender_sites TEXT NOT NULL,
            electricity_needed BOOLEAN NOT NULL,
            description TEXT
        );
        ```
    * **`game_info` table:**
        ```sql
        CREATE TABLE game_info (
            id SERIAL PRIMARY KEY,
            section_title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL
        );
        ```

6.  **Populate Database with Initial Data:**
    Run the provided population scripts to fill your database with initial operator, map, and game info data.
    **Important:** Before running, consider running `TRUNCATE TABLE <table_name> RESTART IDENTITY;` in your Supabase SQL Editor for each table (`operators`, `maps`, `game_info`) to ensure clean data and fresh IDs.

    ```bash
    python populate_db.py
    python populate_maps.py
    python populate_game_info.py
    ```

7.  **Run the Flask application:**
    ```bash
    export FLASK_APP=r6_fan_app  # On Windows: set FLASK_APP=r6_fan_app
    flask run
    ```
    The application should now be running at `http://127.0.0.1:5000/`.

## 5. Deployment (Render)

This application is configured for deployment on Render.com.

### Prerequisites for Deployment

* A Git repository (e.g., GitHub, GitLab, Bitbucket) with your project code.
* A Render.com account.
* Your Supabase and Google API credentials ready for Render environment variables.

### Deployment Steps

1.  **Ensure `requirements.txt` is updated:**
    In your project root, run:
    ```bash
    pip freeze > requirements.txt
    ```
    Verify `gunicorn` and `requests` are listed.

2.  **Ensure `Procfile` is correct:**
    In your project root, ensure `Procfile` contains:
    ```
    web: gunicorn run:app
    ```

3.  **Commit and Push to Git:**
    Ensure all your latest changes (including `__init__.py`, `run.py`, updated imports, `Procfile`, and `requirements.txt`) are committed and pushed to your remote Git repository.
    ```bash
    git add .
    git commit -m "Prepare for Render deployment"
    git push origin main # Or your main branch name
    ```

4.  **Create Web Service on Render:**
    * Log in to [Render.com](https://render.com/).
    * Click "New" -> "Web Service".
    * Connect your Git repository and select your project.
    * **Configure settings:**
        * **Name:** `r6-fan-app` (or a unique name)
        * **Region:** Choose a region close to your users.
        * **Branch:** `main` (or your deployment branch)
        * **Root Directory:** Leave empty (if your `r6_fan_app` folder is in the root).
        * **Runtime:** `Python 3`
        * **Build Command:** `pip install -r requirements.txt`
        * **Start Command:** `gunicorn run:app` (Crucial: ensure this matches your `Procfile`)
        * **Plan Type:** "Free" or "Starter" for initial testing.

5.  **Add Environment Variables on Render:**
    In your Render service settings, go to "Environment" (or "Advanced" -> "Environment Variables") and add the following, using your actual values:
    * `SUPABASE_URL`
    * `SUPABASE_KEY`
    * `user`
    * `password`
    * `host`
    * `port`
    * `dbname`
    * `LLM_API_KEY` (Your Google Gemini API Key)

6.  **Deploy:** Click "Create Web Service". Render will now build and deploy your application. Monitor the logs for any issues.

## 6. Design and Development Process

The development of this application followed an iterative approach, focusing on building core functionalities and progressively enhancing them.

* **Initial Setup:** Establishing the Flask application structure, integrating Flask-SQLAlchemy, and connecting to Supabase as the database backend.
* **Data Modeling & Population:** Defining SQLAlchemy models for Operators, Maps, and Game Info, and creating dedicated Python scripts to populate these tables with initial, comprehensive data.
* **Core Feature Development:** Implementing routes and templates for browsing operators and maps, including detailed views.
* **Interactive Enhancements:** Adding client-side JavaScript for features like filtering operators, populating map sites dynamically, and creating the accordion-style game info section for improved user experience.
* **LLM Integration:** Incorporating the Google Gemini 2.0 Flash API to power the "Lineup Suggestor," demonstrating advanced AI capabilities within the application. This involved crafting effective prompts and parsing AI responses.
* **Deployment Preparation:** Structuring the Flask application as a Python package, configuring `Procfile` and `requirements.txt`, and setting up environment variables for seamless deployment on Render.com.
* **Debugging & Refinement:** Addressing various import errors, environment variable issues, and front-end display bugs to ensure stability and responsiveness across different environments.

## 7. Unique Approaches & Methodologies

* **LLM-Powered Dynamic Content:** The "Lineup Suggestor" stands out by leveraging a large language model to provide context-aware, intelligent operator recommendations, moving beyond static data lookups.
* **Modular Flask Structure:** The application utilizes Flask Blueprints (though simplified for this scale) and a clear separation of concerns (models, routes, main app initialization) to promote maintainability and scalability.
* **External Database for Content:** By using Supabase as a PostgreSQL backend, all dynamic content (operators, maps, game info) is managed externally, allowing for easy updates without redeploying the entire application code.
* **Responsive Frontend Design:** Emphasis was placed on ensuring the application is fully responsive and user-friendly across various devices, utilizing modern CSS techniques.

## 8. Trade-offs Made

* **Mock Map Site Data:** For the `map-sites` API endpoint, mock data is currently used instead of a more complex database schema for map sites. This was a trade-off for development speed and simplicity, avoiding the need for a nested database structure or complex joins for a relatively small dataset. In a larger application, map sites would ideally be a separate table linked to maps.
* **Basic Search Functionality:** The global search is a simple `LIKE` query on operator names. For a more robust search experience (e.g., searching by ability, role, or fuzzy matching), a dedicated search engine (like Elasticsearch) or a more advanced database indexing strategy would be required.
* **Limited LLM Context:** The LLM prompt for lineup suggestions is concise. For even more nuanced suggestions, a more extensive prompt with detailed game state, player skill levels, or specific operator loadouts could be provided, but this would increase complexity and latency.
* **No User Authentication/Profiles:** The application is purely informational and does not include user authentication or personalized features. This simplifies development but means no user-specific data can be stored or retrieved.

## 9. Known Issues & Limitations

* **Image Placeholders:** Operator portraits and map images are currently placeholders or static paths. A more robust solution would involve dynamic image serving or integration with a CDN.
* **LLM Latency:** The "Lineup Suggestor" may experience slight delays due to the API call to the Gemini model.
* **Error Handling:** While basic error pages are in place, more granular error logging and user feedback could be implemented for a production-grade application.
* **No Database Migrations:** The current setup relies on manual SQL commands for schema changes. For a production environment, a tool like Flask-Migrate (Alembic) would be recommended for managing database schema evolution.

## 10. Why This Tech Stack?

The chosen technology stack was selected for a combination of developer familiarity, rapid prototyping capabilities, and suitability for the application's features:

* **Python/Flask:** Python is a versatile language, and Flask is a lightweight, flexible web framework ideal for building small to medium-sized web applications quickly. It allows for fine-grained control and has a large ecosystem of libraries.
* **Flask-SQLAlchemy:** Provides an Object-Relational Mapper (ORM) that simplifies database interactions, allowing developers to work with Python objects instead of raw SQL queries, which speeds up development and reduces errors.
* **Supabase (PostgreSQL):** Chosen for its ease of use as a Backend-as-a-Service that provides a robust PostgreSQL database. It simplifies database management, authentication (though not used extensively here), and offers real-time capabilities for future expansion. PostgreSQL is a powerful and reliable relational database.
* **Google Gemini 2.0 Flash API:** Selected for its advanced natural language processing capabilities, making it suitable for generating intelligent and context-aware operator suggestions, which is a core unique feature of this application. Its "Flash" variant offers a good balance of performance and cost-effectiveness.
* **Render.com:** A convenient and developer-friendly cloud platform for deploying Python web services. Its integration with Git, automatic dependency installation, and environment variable management streamline the deployment process.
* **HTML/CSS/JavaScript:** The standard trio for web development, offering maximum flexibility and control over the frontend user interface and experience.

## 11. Usage

Once deployed, navigate to the provided Render URL to access the application.

* Use the navigation bar to browse Operators, Maps, and Game Info.
* On the Operators page, use the buttons to filter between Attackers and Defenders.
* Use the global search bar in the header to find operators by name from any page.
* Visit the Lineup Suggestor to input a situation and get AI-powered operator recommendations.

## 12. Contributing

Feel free to fork the repository, make improvements, and submit pull requests.

## 13. License

This project is open-source and available under the [MIT License](LICENSE).