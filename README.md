# Iris Classifier Deployment

This project is a Flask app that serves an Iris species prediction model and includes a simple web UI.

## Local Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open `http://localhost:5000`.

## Docker Run

Build the image:

```bash
docker build -t iris-classifier .
```

Run the container:

```bash
docker run -p 5000:5000 iris-classifier
```

Open `http://localhost:5000`.

## Deploy Options

### Render

1. Push this folder to GitHub.
2. In Render, create a new **Web Service** from that repo.
3. Choose either:
   - **Docker** runtime and let Render use the existing `Dockerfile`, or
   - **Python** runtime with start command:

```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

4. Render will automatically provide the `PORT` environment variable.
5. Set the health check path to `/health`.

### Railway

1. Push the project to GitHub.
2. Create a new Railway project from the repo.
3. Railway can deploy directly from the `Dockerfile`.
4. The app already reads `PORT`, so no code changes are needed.
5. Use `/health` as the health check endpoint if you configure one.

### Any VM or Server

Install dependencies and run:

```bash
gunicorn --bind 0.0.0.0:${PORT:-5000} app:app
```

## API Example

Endpoint:

```bash
POST /predict
Content-Type: application/json
```

Request body:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Example response:

```json
{
  "prediction": 0,
  "species": "setosa"
}
```
