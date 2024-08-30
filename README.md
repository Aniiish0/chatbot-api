## Setup & Run
1. Setup virtual environment using following command: `python3 -m venv .venv`
2. Activate the virtual environment using: `source .venv/bin/activate`
3. Install `requirements.txt` using: `pip install -r requirements.txt`
4. Add your data to `knowledge_base.json`
5. Feed your knowledge base using: `python3 feed_or_search.py`
6. Setup `.env` file using `.env.example` if you want
4. Run `app.py` using: `python3 app.py`
5. Now you can hit `localhost:<APP_PORT (set in .env) or 3000 (default)>/ask?question=<your_question>`

Note: `python3` and `python` are interchangeable according to your system.