# Artemis
Python service developed following a simple architecture. Centered around the concept of events, provides a REST layer to perform CRUD operations on them.

This is a simple rewrite of the very same Go [service](https://github.com/nanchano/bastet), with the intention of keeping it simpler and to provide a Python & ORM example. 

To test the server: `make all-requests`

To test the code: `make test`

## Project structure

```bash
├── Makefile
├── README.md
├── artemis
│   ├── __init__.py
│   ├── db.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── poetry.lock
├── pyproject.toml
└── tests
    ├── __init__.py
    ├── test_db.py
    └── test_routes.py
```

The `Makefile` contains some handy rules for development and testing

`artemis` contains the actual code for the service, with `db` being the database layer to interact with sqlite, `routes` being the REST layer, `schemas` containing the DTOs for the main model of the app as well as some requests, and `main` containing the app entrypoing.

`tests` contains the unit tests for the DB and the router.

`poetry.lock` and `pyproject.toml` are just to handle dependencies and overall project settings through `poetry`.
