import sys

path = "/home/dimonade/geoplotnik"
if path not in sys.path:
    sys.path.append(path)

from src.geoplotnik.main import create_app  # noqa

application = create_app().server