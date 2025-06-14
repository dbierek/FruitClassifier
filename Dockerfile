# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
RUN useradd appuser && groupadd dockergroup
COPY --chown=appuser:dockergroup . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--certfile", "cert.pem", "--keyfile", "privkey.pem", "--bind", "0.0.0.0:5000", "app:app"]
