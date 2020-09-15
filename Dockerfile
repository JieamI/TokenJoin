FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./backend /app
COPY ./requirement.txt /app
RUN pip install -r requirements.txt