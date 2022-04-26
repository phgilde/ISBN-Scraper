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
    url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data"
    result_str = requests.get(url)
    if result_str:
        return json.loads(result_str)[f"ISBN:{isbn}"]
    else:
        return False


def isbn_to_tuple(isbn):
    data_json = call_api(isbn)
    if not data_json:
        return "false", None, None
    
    authors = ", ".join(author["name"] for author in data_json["authors"])
    title = data_json["title"]
    return "true", authors, title


input_path = input("Input file: ")
if not validate_input_path(input_path):
    print("Invalid input path!")
    sys.exit(0)

output_path = input("Output file: ")

df = pd.read_csv(input_path, header=0, names="ISBN")
df["Exists"], df["Authors"], df["Title"] = df["ISBN"]
df.to_csv(output_path)
