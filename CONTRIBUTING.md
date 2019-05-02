# Contributing

Our development process is centered around Python 3.7 and Pipenv.

## Environment Setup

### Prerequisites

Before getting started, you will need Python 3.7 and Pipenv installed.

### Source Code and Dependencies

```
git clone git@github.com:UltiManager/ultimanager-web
cd ultimanager-web
pipenv install --dev
```

### Linting Hooks

Code style is checked during the CI build using `flake8` and `black`. To assist
with these requirements, we use `pre-commit` to run these checks before each
commit. To install the hooks, run:

```
pipenv run pre-commit install
```

## The Django Project

Before running any commands related to the project, we recommend creating a
`.env` file that will be picked up by Pipenv when running any commands. The
recommended contents are:

```
DEBUG=True
```

Any commands of the form `pipenv run ...` will run with the variables defined
here.

### Local Server

```
pipenv run ultimanager/manage.py migrate
pipenv run ultimanager/manage.py runserver
```
