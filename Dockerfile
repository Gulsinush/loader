FROM python:3.9.19-alpine3.20
WORKDIR /app
COPY /output/app.exe /app/loader.exe
ENTRYPOINT ["python", "loader.exe"]