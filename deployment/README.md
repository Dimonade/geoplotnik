# Deployment instructions for PythonAnywhere

1. Create an account on PythonAnywhere.
2. Create a web application, select manual environment:
    1. Choose Python 3.13.
3. Open a bash console:
    1. Clone the repository to the home directory.
    2. Go to the repository directory: `cd geoplotnik`.
    2. Create a virtual environment: `python -m venv .venv`.
    3. Activate the virtual environment: `source ./.venv/bin/activate`.
    4. Install the requirements: `python -m pip install -e .`.
4. In the application page:
    1. Source code: `/home/dimonade/geoplotnik/src/geoplotnik/main.py`.
    2. Working directory: `/home/dimonade/geoplotnik`
    3. WSGI configuration file: copy the contents of `wsgi_template.py`.
    4. Virtualenv: choose `/home/dimonade/geoplotnik/.venv`.

        1
5. Reload the app.