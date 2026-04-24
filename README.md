# 🔗 URL Shortener & Analytics Dashboard

A full-stack, high-performance URL shortening service with an integrated analytics dashboard. This project works as a simplified version of Bitly, allowing users to generate short links, handle redirection, and track detailed user engagement.

## 💡 Project Idea & What It Does
This project converts long URLs into short, shareable links (e.g., `http://localhost:8000/1`).

In addition to redirection, the system tracks every click. Before redirecting the user, the backend captures useful analytics data, which is then displayed in an interactive dashboard.


### Core Features
- **Fast URL Shortening:** Uses Base62 encoding to generate the shortest possible unique links.
- **Instant Redirection:** Handles HTTP redirects efficiently using FastAPI.
- **Click Tracking:** Logs timestamps, IP addresses, and User-Agent data for every single click.
- **Interactive Dashboard:** A pure Python frontend to visualize traffic trends over time and view raw click logs.

---

## 🛠️ Technology & Tools Used

**Backend (API & Database)**
* **[FastAPI](https://fastapi.tiangolo.com/):** High-performance Python web framework for building the API endpoints.
* **[SQLite](https://www.sqlite.org/):** Lightweight, file-based relational database.
* **[SQLAlchemy](https://www.sqlalchemy.org/):** The Object-Relational Mapper (ORM) used to interact with the database.
* **[Pydantic](https://docs.pydantic.dev/):** For strict data validation and schema definitions.
* **[Uvicorn](https://www.uvicorn.org/):** The ASGI server used to run the FastAPI application.

**Frontend (Dashboard)**
* **[Streamlit](https://streamlit.io/):** Rapid web app framework used to build the interactive UI without HTML/JS.
* **[Pandas](https://pandas.pydata.org/):** For structuring and manipulating the click data.
* **[Plotly Express](https://plotly.com/python/plotly-express/):** For rendering interactive line charts.

---

📊 Dashboard Features
Total clicks
Click trends over time
Activity logs
Original URL preview

🔐 Key Concept
Short URLs are generated using Base62 encoding:
Uses characters: 0-9, a-z, A-Z
Converts numeric IDs → short strings
Ensures unique and compact URLs


## 📂 Project Detail (Architecture & Files)

The project is strictly modular, separating the backend business logic from the frontend user interface.

fastapi-shortener/
├── requirements.txt      # Lists all Python dependencies
├── backend/              # Core API Logic
│   ├── database.py       # Configures the SQLite database engine and session maker
│   ├── models.py         # Defines the SQL tables (URLs and Clicks)
│   ├── schemas.py        # Defines Pydantic models to validate API requests/responses
│   ├── utils.py          # Contains the Base62 mathematical encoding logic
│   └── main.py           # The FastAPI app, defining the POST and GET routes
└── frontend/             # User Interface
    └── app.py            # The Streamlit dashboard that consumes the FastAPI endpoints


## 🚀 How to Run the Project Locally
You will need two separate terminal windows to run the Backend and Frontend simultaneously.

1. Initial Setup
Clone the repository and install the dependencies:

Bash
## Create and activate a virtual environment (Recommended)
create: python -m venv venv

run: venv\Scripts\activate

## Install required packages
pip install -r requirements.txt

2. Start the Backend API
In your first terminal, start the FastAPI server:
```Bash
uvicorn backend.main:app --reload --port 8000
``` 
The API is now running at http://localhost:8000. The SQLite database (shortener.db) will be created automatically.

3. Start the Frontend Dashboard
Open a second terminal, activate the virtual environment again, and run:
```Bash
streamlit run frontend/app.py
```
The dashboard will automatically open in your browser at http://localhost:8501.

4. stop the server (ctrl + c)
