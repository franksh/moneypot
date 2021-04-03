# Moneypot

Making money on the stock market.

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

## Overview

Moneypot consists of multiple modules and services that can run independently of each other. Services can run in the background and can be managed via supervisor.

- exchange (service): An API to the database

## Managing services with supervisor

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
