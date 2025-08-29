# http web shell to test kubernetes runtimes
A simple web ui to run console commands within the container

And the build steps for the http tester itself:
## get uv - makes python life easier
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## run
```
uv sync
uv run main.py
```

### from scratch
- uv sync
- uv pip compile pyproject.toml -o requirements.txt
- uv pip install -r requirements.txt
- uv run main.pys

## build
```
docker build -t webpyshell .
```

## run local
```
docker run -p 2100:2100 webpyshell
```

## publish
```
docker login
docker tag webpyshell wlanboy/webpyshell:latest
docker push wlanboy/webpyshell:latest
```

## run
```
docker run -d -p 2100:2100 wlanboy/webpyshell
```
