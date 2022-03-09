# steam-deals-backend

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

The Back-end of our application - that is, this repository, is hosted on two environments at two different addresses -
production and development:

- developing: http://nwta.eastus.cloudapp.azure.com:5555
- production: http://nwta.eastus.cloudapp.azure.com:5000

Those two addresses correspond to the master and develop branches in our repository.

> API documentation is available under the `/docs` endpoint
> - Example: http://nwta.eastus.cloudapp.azure.com:5000/docs

## Installation

1. `git clone https://gitlab.com/rafit/steam-deals-backend.git`
2. `cd steam-deals-backend/`
3. `pip install .`

## Usage

When you are in the `steam-deals-backend/` directory, you can run the API server by:

- `python3 steam-deals-backend/main.py`

Available arguments are listed under the:

- `python3 steam-deals-backend/main.py --help`

## Authors and acknowledgment

There are 3 contributors of this project:

- [mzebrak](https://gitlab.com/mzebrak)
- [kchrobok](https://github.com/Avsterx9)
- [rav-zyla](https://gitlab.com/rav-zyla)
