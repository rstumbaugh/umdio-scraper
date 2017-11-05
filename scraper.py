import requests
from bs4 import BeautifulSoup
from os import environ as env

print(env.get('DB_URI'))