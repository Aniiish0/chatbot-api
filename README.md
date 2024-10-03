## Setup & run in local machine
1. Setup virtual environment using following command: `python3 -m venv .venv`
2. Activate the virtual environment using: `source .venv/bin/activate`
3. Install `requirements.txt` using: `pip install -r requirements.txt`
4. Add your data to `knowledge_base.json`
5. Feed your knowledge base using: `python3 helpers/feed_or_search.py`
6. Setup `.env` file using `.env.example` if you want
4. Run `app.py` using: `python3 app.py`
5. Now you can hit `localhost:<APP_PORT (set in .env) or 3000 (default)>/ask?question=<your_question>`

Note: `python3` and `python` are interchangeable according to your system.

## Run using docker
### Docker build
Run the following command to build an image for the app:

`docker build -t <app-name> .`

Example command: `docker build -t chatbot .`


### Docker run
To run the image, execute the following command:

`docker run -p <host-port>:5000 -v <host-knowledge-base-file-path>:/app/<knowledge-base-file-name> -e INPUT_PATH=/app/<knowledge-base-file-name> <app-name>`

Example command: `docker run -p 3001:5000 -v /usr/app/knowledge_base.json:/app/knowledge_base.json -e INPUT_PATH=/app/knowledge_base.json chatbot`

Wondering how to find the absolute path to the host knowledge base file?
1. Try running the following `pwd` command in the host knowledge base file directory.
2. Append the knowledge base file name to the result of the `pwd` command.
3. Example path: `/Users/abc/app/knowledge_base.json`.