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

This is a website for Rainbow 6 Siege help for people that only start playing. Since R6 is a character based tactical shooter, choosing the right character can usually win you rounds. So this website features information about operators, their abilities and usages, maps and their peculiarities, and an AI-powered "Lineup Suggestor" to help players choose operators based on their situation.

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
7.  **Run the Flask application:**
    ```bash
    export FLASK_APP=r6_fan_app  # Windows: set FLASK_APP=r6_fan_app
    flask run
    ```
    Access at `http://127.0.0.1:5000/`.

## 3. Design Process

I started with a white list and generating ideas. Since most of my summers of high school were spent playin Siege with my friends, I chose what I know well. The problem for new coming players is complexity of the game: soft walls, one shot headshots. Which is further worsened by almost 60 characters each with a unique ability. I drafted the design of application on paper and UML state machine (which was very simple), then connection with db. Since I am not very proficient with frontend technologies I used templating in Jinja2 and ChatGPT to generate basic templates and styling. Then I connected it with backend using Flask, and at the end added Google's Gemini for LLM support. 

## 4. Unique Approach

The standout feature is the **LLM-Powered Lineup Suggestor**, which utilises  Google Gemini 2.0 Flash API to provide dynamic operator recommendations based on user-described in-game situations. This moves beyond static data, offering intelligent strategic insights. 

## 5. Tradeoffs

* **Basic Search:** The global search uses a simple database `LIKE` query and only works on names of characters. Further development would bring search based on words, since most players would not know specific names of gadgets in the game.
* **Limited LLM Context:** The LLM prompt is concise for efficiency. More detailed in-game context could be provided for even more specific suggestions, but this would increase complexity.
* **No User Authentication:** The application is purely informational, omitting user authentication or personalized features to simplify development.

## 6. Limitations

* **Potential for Outdated Data:** As game updates frequently change operators and existing data was written by hand, it is not adaptive and would require human involvement for updates. The fix would be implementation of web scraper from original game website or official API.
* **Limited Styling:** As the emphasis was placed on features, application does not stand out graphically.
* **Cold Start Latency on Render:** Due to using Render's free plan, the application may experience a "cold start" delay (up to minute) when accessed after a period of inactivity.


## 7. Tech Stack

Tech stack was chosen due to familiarity with Python and Flask being industry standard (some would argue better than Django/FastAPI) and popularity of following services:

* **Flask-SQLAlchemy:** Simplifies database interactions through an ORM, abstracting raw SQL.
* **Supabase (PostgreSQL):** A managed PostgreSQL database solution that is easy to deploy.
* **Google Gemini 2.0 Flash API:** Provides advanced AI capabilities for the core "Lineup Suggestor" feature, chosen for its cost.
* **Render.com:** A convenient and developer-friendly platform that facilitates seamless deployment of Python web services from Git.
* **HTML/CSS/JavaScript:** Standard web technologies providing complete control over the frontend user experience and responsiveness.
