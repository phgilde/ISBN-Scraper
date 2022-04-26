import json
import pandas as pd
import requests


# get the json containing information on the book from the api
def call_api(isbn: str):
    url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    result = json.loads(requests.get(url).content)
    print(result)
    if result:
        return result[f"ISBN:{isbn}"]
    else:
        return False


input_path = input("Input file: ")
output_path = input("Output file: ")

df = pd.read_csv(input_path, names=["ISBN"])
df["JSON"] = df["ISBN"].apply(call_api)

df["Authors"] = df["JSON"].apply(
    lambda x: "; ".join(author["name"] for author in x["authors"])
)
df["Title"] = df["JSON"].apply(lambda x: x["title"])

df[["ISBN", "Title", "Authors"]].to_csv(output_path)
