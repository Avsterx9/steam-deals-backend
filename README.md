# steam-deals-backend

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

This project aims to familiarize ourselves with a modern and more professional approach to creating web applications
thanks to the use of such technologies as:

- [Python 3.8](https://docs.python.org/3.8/)  - (as it is natively available in the latest ubuntu 20.04 LTS)
- [FastAPI](https://fastapi.tiangolo.com/)  - web framework for building APIs
- [pytest](https://docs.pytest.org/en/6.2.x/index.html) - testing framework
- [bash](https://www.gnu.org/software/bash/manual/bash.html) - auxiliary scripts


#### Code quality:

- [sonarcloud](sonarcloud.io/) - cloud-based code quality and security service
- [Black](https://black.readthedocs.io/en/stable/) - code formatter
- [pylint](https://pylint.pycqa.org/en/latest/) - code linter
- [pre-commit](https://pre-commit.com/) - pre commit hooks


#### Others:

- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Gitlab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [Gitlab Issue Tracking System](https://docs.gitlab.com/ee/topics/plan_and_track.html)
- [Docker](https://docs.docker.com/)
- [Microsoft Azure](https://azure.microsoft.com) - VM instance
- [PostgreSQL 12](https://www.postgresql.org/docs/12/index.html) - permanent database
- [SQLite](https://www.sqlite.org/docs.html) - temporary database
- [make](https://www.gnu.org/software/make/manual/make.html) - build automation tool


#### Additional:

- [bcrypt](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html) - password hashing
- [OAuth2](https://oauth.net/2/) - access authorization protocol
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/) - object-relational mapper
- [Dynaconf](https://www.dynaconf.com/) - object-settings mapper

---

The back-end of steam-deals project - that is, this repository, is hosted on two environments at two different
addresses - production and development:

- development: http://nwta.eastus.cloudapp.azure.com:5555
- production: http://nwta.eastus.cloudapp.azure.com:5000

Those two addresses correspond to the `master` and `develop` branches in this repository.

> API documentation is available under the `/api/v1/docs` and `/api/v1/redocs` endpoints.
> - Example: http://nwta.eastus.cloudapp.azure.com:5000/api/v1/docs

## Requirements

1. `python3.8` or higher
2. `python3.8-venv` or higher (only when you're installing this package in a virtual environment)

## Installation

We assume that you have already cloned this repository and you are in the project directory, so you have done:

```bash
git clone https://gitlab.com/rafit/steam-deals-backend.git
cd steam-deals-backend/
```

Check if you don't know what is [PEP 517](https://setuptools.pypa.io/en/latest/build_meta.html?highlight=pep%20517)

Then you can choose:
<details>
<summary>Install automatically with make</summary>

> You can check available commands with `make` or `make help`.\
> There are several variations of installation - all using a virtual environment installed in the `venv/` directory.
>
> For example if you want to build entire project with `development tools`:
> ```bash
> make build-dev       # Create virtual environment in the `venv/` directory and build the package with development tools
> . venv/bin/activate  # Activate virtual environment
> ```
</details>

<details>
<summary>Install in virtual environment manually</summary>

> -   <details>
>     <summary>Use PEP 517 - install everything automatically  </summary>
>
>     ```bash
>     pip3 install build                          # Install PyPA correct PEP 517 build frontend
>     python3.8 -m build --wheel                  # Build the package in an isolated environment, generating a wheel in the directory `dist/`
>     python3.8 -m venv venv/                     # Create virtual environment in the `venv/` directory
>     . venv/bin/activate                         # Activate it
>     find dist/ -name *.whl | xargs pip install  # Find `steam-deals` .whl in the `dist/` directory and install it
>     ```
>
>     </details>
>
> -   <details>
>     <summary>Upgrade your system packages and install as editable</summary>
>
>     ```bash
>     python3.8 -m venv venv/               # Create virtual environment in the `./venv/` directory
>     . venv/bin/activate                   # Activate it
>     pip3 install -U pip setuptools wheel  # Upgrade your packages used for building
>     pip3 install -e .                     # Install `steam-deals` as editable
>     ```
>
>    </details>

</details>

<details>
<summary>Install in your operating system scope (not recommended)</summary>

> Do as above, but just omit the following parts:
>
> ```bash
> pip3 install build
> pythom3.8 -m build --wheel
> python3.8 -m venv venv/
> . venv/bin/activate
> ```

</details>

## Usage

When you are in the `steam-deals-backend/` directory, you can run the API server by running those command:

> `steam-deals` OR `python3 steam_deals/main.py`

Available arguments are listed under the:

> `steam-deals -h` OR `python3 steam_deals/main.py --help`

You can specify the environment by using the `ENVIRONMENT_NAME` environment variable like:

> `ENVIRONMENT_NAME=testing steam-deals -h` OR `ENVIRONMENT_NAME=testing python3 steam_deals/main.py --help`

## Authors and acknowledgment

There are 3 contributors of this project:

- [mzebrak](https://gitlab.com/mzebrak)
- [kchrobok](https://github.com/Avsterx9)
- [rav-zyla](https://gitlab.com/rav-zyla)
