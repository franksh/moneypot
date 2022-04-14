# Moneypot 💰🍯

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

Making money on the stock market.

Moneypot is intended as an application to develop and deploy trading strategies. It will offer:

- Support for different asset types (stocks, crypto) and exchanges.
- Connection to data providers to store ticker information.
- A Streamlit dashboard to display tickers and analyze trading strategies.
- Backtesting of trading strategies
- Deployment of trading strategies

Moneypot is currently in development and offers limited functionality (yet).

## Install

Development version:

```
make
```

or

```
python setup.py develop
```

## Configuration

Before using moneypot, you have to fill in some necessary configuration details (database location, API tokens).

Config files are create at `~/.moneypot`.

Moneypot assumes a running PostgreSQL database with the timescaleDB extension installed.

## Usage (Dev notes)

Moneypot consists of multiple modules and services that can run independently of each other. Services can run in the background and can be managed via supervisor.

- exchange (service): An API to the database
- monitor (service): A Streamlit dashboard to visualize tickers and trading strategies performance
- broker (service)(tbd): A service to schedule and deploy trading strategies via connected exchanges/brokers.

### Managing services with supervisor

Moneypot uses a package called `supervisor` to manage services that run in the background.

Services are python scripts that will be executed and kept running in the background, and their runtime managed like a classic service, using `start`, `stop`, `status` commands, etc. New services can be registered in the `supervisor.cfg` file.

The supervisor can be invoked via

```
moneypot supervisor *command*
```

Some useful commands:

- `moneypot supervisor status all/*service*`: List the status of all running services / a particular service.
- `moneypot supervisor start/stop all/*service*`: Start or stop a service.

New services can be registered

_Note:_ `moneypot supervisor` is just an alias for `supervisorctl`.

Supervisor is used to manage services that run in the background.

Services can be controlled via `supervisorctl`. Some useful commands:

- `supervisorctl status all`: Lists all running services
