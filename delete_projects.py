from hasty import Client
import json
import glob
import os

API_KEY = "iv8DaE00dXbFY568-FCVmMH320KWX8UNWunQMA9YKH8cFCMay-heLM8sBOI_EJIta5GKnTud-nQyg4gnz9ZaFw"
BASE_URL = "https://api-default-none-staging.dev.hasty.ai"

h = Client(api_key=API_KEY, base_url=BASE_URL)

print(type(h.get_projects()[0]))

for x in h.get_projects():
    x.delete()