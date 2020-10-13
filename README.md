# Legal Process Crawler

It is a simple API to get legal process detail on TJAL or TJMS website and convert the search result HTML to JSON

# Courts
* TJAL
* TJMS 

# Stack
* Python 3.8
* FastApi
* Parsel
* Aiohttp

# How to create the Development environment

## Docker
Use docker to create the development environment
- [docker](https://www.docker.com)
- [docker-compose](https://github.com/docker/compose)

Build and run
```shell script
docker-compose up
```

Force build
```shell script
docker-compose up --build
```

Run a sh into container
```shell script
docker-compose run api sh
```

## Virtualenv
Install python version using the [pyenv](https://github.com/pyenv/pyenv)
```shell script
pyenv install 3.8.0
```

Set 3.8.0 as global python version
```shell script
pyenv global 3.8.0
```

Create and active a virtualenv
```shell script
python -m venv .venv
source .venv/bin/active
```

Install the requirements
```shell script
pip install -r requirements.txt
```