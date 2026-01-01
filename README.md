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
- uv run gunicorn main:app

## build
```
docker build -t webpyshell .
```

## run local
```
docker run --name webshell -d -p 2100:2100 wlanboy/webpyshell
```
* see logfile for access key
* Log output:
```
[2025-08-30 18:00:43 +0000] [1898413] [INFO] Starting gunicorn 23.0.0
[2025-08-30 18:00:43 +0000] [1898413] [INFO] Listening at: http://0.0.0.0:2100 (1898413)
[2025-08-30 18:00:43 +0000] [1898413] [INFO] Using worker: sync
[2025-08-30 18:00:43 +0000] [1898414] [INFO] Booting worker with pid: 1898414
[2025-08-30 18:00:43 +0000] [1898414] [INFO] Access Key: xxxxxxxxxxxxxxx
```

## run
```
docker run -d -p 2100:2100 wlanboy/webpyshell
```
