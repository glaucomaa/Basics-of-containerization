# Check-in/Check-out app

2 Docker containers:

- One Hosts the SQLite database

- Other is entry point


### Requirements

- Docker
- Docker Compose

### Steps

Step 0: Clone the repo:

```bash
git clone https://github.com/glaucomaa/Basics-of-containerization.git
```

Step 1: Navigate to the cloned repo:

```bash
cd Basics-of-containerization
```

Step 2: Build docker images:

```bash
docker compose up --build -d
```

### Usage

Check-in:

```bash
curl -X POST http://localhost:5000/checkin  
```

Check-out:

```bash
curl -X POST http://localhost:5000/checkout 
```

List of last checkins:

```bash
curl http://localhost:5000/last_checkins
```

To stop the containers:

```bash
docker compose down
```

#### Additional information

Instead of

```bash
docker compose
```

can be used 
```bash
docker-compose
```
