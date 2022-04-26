import json
import pandas as pd
import requests
from tkinter import filedialog, Tk, messagebox


# get the json containing information on the book from the api
def call_api(isbn: str):
    url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    result = json.loads(requests.get(url).content)
    print(result)
    if result:
        return result[f"ISBN:{isbn}"]
    else:
        return False


parent = Tk()


input_path = filedialog.askopenfilename(title="Choose input File", parent=parent)
output_path = filedialog.asksaveasfilename(title="Choose output Location", parent=parent)

df = pd.read_csv(input_path, names=["ISBN"])
df["JSON"] = df["ISBN"].apply(call_api)

df["Authors"] = df["JSON"].apply(
    lambda x: "; ".join(author["name"] for author in x["authors"])
)
df["Title"] = df["JSON"].apply(lambda x: x["title"])
print(df[["ISBN", "Title", "Authors"]])
df[["ISBN", "Title", "Authors"]].to_csv(output_path, errors="ignore", encoding="iso-8859-1")
messagebox.showinfo("Done", "The file was successfully augmented!", parent=parent)