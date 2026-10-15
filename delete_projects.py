from hasty import Client
import json
import glob
import os

API_KEY = os.environ["HASTY_API_KEY"]
BASE_URL = "https://api-default-none-staging.dev.hasty.ai"

h = Client(api_key=API_KEY, base_url=BASE_URL)

for x in h.get_projects():
    x.delete()

print("All projects deleted!")