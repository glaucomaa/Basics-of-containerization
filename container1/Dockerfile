FROM alpine:latest

RUN apk add --no-cache sqlite

WORKDIR /app

COPY database.db /app/

CMD ["sqlite3", "database.db"]
