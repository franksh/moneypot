# Moneypot

Making money on the stock market.

## Install

Development version:

```
pip install -e ./moneypot
```

## Managing services with `supervisor`

Supervisor is userd to manage services that run in the background. It is installed during setup.

`supervisorctl` lists all processes currently managed by supervisor

## Configuration

Copy the file `moneypot.cfg` to `~/.moneypot_config` and fill in your information on API tokens.
