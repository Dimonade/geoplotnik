![Python](https://img.shields.io/badge/Python-3.13%2B-yellow?logo=python&logoColor=blue)(https://python.org)
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Geoplotnik

**Geoplotnik** is an interactive web application for visualizing and exploring geochemical data
 — starting with TAS (Total Alkali-Silica) diagrams for igneous rock classification, 
 and planned to expand into a broader suite of geological plotting tools.

It is built on Dash for interactive data visualization, 
and designed to make it easy for geoscientists, students, and hobbyists to quickly load data, 
explore patterns, and create publication-quality plots without having to code.

## Deployment

The application is currently deployed [here](https://dimonade.eu.pythonanywhere.com), 
on PythonAnywhere.

> ⚠️ **Note:** Hosted on the free tier — please be gentle, no stress testing or DDoS =) .

## What it does

- **Data Upload & Parsing** — Drop your geological dataset (CSV, Excel, etc.) 
  into the app and it will parse and prepare it for plotting.
- **TAS Diagram Generation** — Automatically plots Total Alkali vs. Silica diagrams, 
  with correct classification fields according to IUGS standards.
- **Interactive Visualization** — Hover tooltips, zoom, pan, filter, and save plots 
  as images directly from the browser.
- **Grouping Options** — Group samples by any column in your dataset for color-coding 
  and comparison.
- **Automatic Handling of Missing Data** — Missing or invalid points are either dropped 
  or assigned to an `"Ungrouped"` category (customizable).

## Why It’s Useful

Currently, Geoplotnik is a fast, no-fuss TAS diagram tool:

- Perfect for teaching petrology or geochemistry without having to draw diagrams by hand.
- Lets researchers quickly explore datasets and check rock type classification.
- Works in any browser — no local GIS or plotting software needed.

## Roadmap

We plan to expand Geoplotnik to support a range of geological plots and tools.
The scope and the priority of each feature request can be tracked in the Issues.

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

## Usage

Upon loading the application, a default dataset appears.
If you have not set a default data loaction, a dummy set is  used.

### Default values

It is possible to use a `DEFAULT_DATA` environment variable to set the defalut data
location. The parameter can be set either in the invoking terminal, or in a `.env`
file. 

## Notes

This is a `Dash` based reimplementation of 
[geochem-streamlit](https://geochem-app-x8wt6zxsp6csnwztd9nvgz.streamlit.app/).

Currently it only supports a basic subset of the features.
