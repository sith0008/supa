# supa

## Prerequisites
- docker
- docker-compose
- Python 3+

## Starting just the Flask server
```bash
cd backend
python3 run.py
```

## Starting all services
```bash
docker-compose up --build
```
The build option can be omitted if no building of images is needed

To check that the services are working,
- Backend: type http://localhost:5000 on a browser -> should return "hello world."
- MySQL: type http://localhost:8080 on a browser to launch adminer. Use the following configurations to login to the database

| field  | value |
| ------------- | ------------- |
| server  | mysql  |
| username  | user  |
| pasword | password |
| database | supa |

## Tear down all services
```bash
docker-compose down
```