# Geoplotnik

## Introduction

This is a `Dash` based reimplementation of 
[geochem-streamlit](https://geochem-app-x8wt6zxsp6csnwztd9nvgz.streamlit.app/).

Currently it only supports a basic subset of the features.

## Installation

### Using `uv`

- Clone the repository: `git clone https://github.com/dimonade/geoplotnik.git`;
- Step inside the repository: `cd geoplotnik`;
- Create a virtual environment: `uv venv`;
- Activate the environment, i.e., `source ./venv/bin/activate`, according to your OS;
- Install the requirements:
  - If you only want to try it: `uv sync --no-dev`;
  - If you want to develop, test or contribute: `uv sync --dev`;
- Install the editable package: `uv pip install -e .`;
- Execute the application: `uv run src/geoplotnik/main.py`;
- Navigate to the newly open page in your browser, or go to `127.0.0.1:8050`;
  _the address of the `Dash` application is printed in the terminal._
