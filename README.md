# steam-deals-backend

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

The back-end of steam-deals project - that is, this repository, is hosted on two environments at two different addresses
production and development:

- development: http://nwta.eastus.cloudapp.azure.com:5555
- production: http://nwta.eastus.cloudapp.azure.com:5000

Those two addresses correspond to the `master` and `develop` branches in this repository.

> API documentation is available under the `/docs` endpoint.
> - Example: http://nwta.eastus.cloudapp.azure.com:5000/docs

## Requirements

1. `python3.8` or higher
2. `python3.8-venv` or higher (only when you're installing this package in a virtual environment)

## Installation

We assume that you have already cloned this repository and you are in the project directory, so you have done:

```bash
git clone https://gitlab.com/rafit/steam-deals-backend.git
cd steam-deals-backend/
```

Then you can choose:
<details>
<summary>Install in virtual environment manually</summary>

```bash
python3.8 -m venv venv/ # Create virtual environment in the `./venv/` directory
. venv/bin/activate     # Activate it
pip3 install -e .       # Install steam-deals
```

</details>

<details>
<summary>Install in your operating system scope (not recommended)</summary>

```bash
pip3 install -e .
```

</details>

## Usage

When you are in the `steam-deals-backend/` directory, you can run the API server by running those command:

> `steam-deals` OR `python3 steam-deals-backend/main.py`

Available arguments are listed under the:

> `steam-deals -h` OR `python3 steam-deals-backend/main.py --help`

## Authors and acknowledgment

There are 3 contributors of this project:

- [mzebrak](https://gitlab.com/mzebrak)
- [kchrobok](https://github.com/Avsterx9)
- [rav-zyla](https://gitlab.com/rav-zyla)
