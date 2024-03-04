# A4S Sealer Module

A python driver and WEI-compatible REST server for controlling and communicating with an A4S Sealer.

## User Guide

### Python Installation

```
git clone https://github.com/ad-sdl/a4s_sealer_module.git
cd a4s_sealer_module
python -m venv .venv && src .venv/bin/activate
pip install -e .
```

To run the WEI REST node, use the following command (updating arguments as needed)

```
python -m a4s_sealer_rest_node --port 3001 --device /dev/ttyUSB2
```

### Docker Installation

After installing and configuring docker, run

```
git clone https://github.com/ad-sdl/brooks_xpeel_module.git
cd a4s_sealer_module
cp example.env .env
# Set appropriate values in the .env file before running the next commands
docker compose build
docker compose up
```
