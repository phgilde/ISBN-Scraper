import json
import pandas as pd
from os.path import exists
import re
import sys

import requests


def validate_input_path(path):
    if not exists(path):
        return False
    if re.search("([^\\s]+(\\.(?i)(csv))$)", path):
        return True
    else:
        return False


def call_api(isbn: str):
    url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    result = json.loads(requests.get(url).content)
    print(result)
    if result:
        return result[f"ISBN:{isbn}"]
    else:
        return False


input_path = input("Input file: ")
if not validate_input_path(input_path):
    print("Invalid input path!")
    sys.exit(0)

output_path = input("Output file: ")

df = pd.read_csv(input_path, names=["ISBN"])
print(df)
df["JSON"] = df["ISBN"].apply(call_api)
df["Authors"] = df["JSON"].apply(
    lambda x: "; ".join(author["name"] for author in x["authors"])
)
df["Title"] = df["JSON"].apply(lambda x: x["title"])

df[["ISBN", "Title", "Authors"]].to_csv(output_path)