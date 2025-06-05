Project Setup and Usage

This is a college group project repository which contains a functional Docker setup with a PostgreSQL database. Follow the instructions below to ensure a successful installation and usage.





## Starting the program


Firstly you have to build the docker image so in a terminal write the following command:

```bash
docker-compose build --no-cache
```

To run the program if not already started, in a terminal write the following command:

```bash
  docker compose up -d
```

If you make any changes in the backend part of the program (any Python or HTML file) you have to firstly turn off the program with the following command; then start again with the second written command:

```bash
  docker compose downn -v
```

