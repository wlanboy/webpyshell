# http web shell to test kubernetes runtimes
A simple web ui to run console commands within the container

And the build steps for the http tester itself:
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
