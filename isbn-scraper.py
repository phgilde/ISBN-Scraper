import json
import pandas as pd
import requests
from tkinter import filedialog, Tk, messagebox, ttk, DISABLED, NORMAL


class App:
    def __init__(self):
        self.root = Tk()
        self.frame = ttk.Frame(self.root, padding=10)

        self.frame.grid()
        self.input_file_button = ttk.Button(
            self.frame, text="Select input file...", command=self.choose_file
        )
        self.input_file_button.grid(row=0, column=0)

        self.input_file_label = ttk.Label(self.frame, text="No file selected")
        self.input_file_label.grid(row=0, column=1)

        self.input_file = None

        self.augment_button = ttk.Button(
            self.frame,
            text="Augment!",
            state=DISABLED,
            command=self.augment_data,
        )
        self.augment_button.grid(row=1, column=0)

        self.save_button = ttk.Button(
            self.frame, text="Save to file...", state=DISABLED, command=self.save
        )
        self.save_button.grid(row=1, column=1)

        self.root.mainloop()

    def choose_file(self):
        self.input_file = filedialog.askopenfilename(
            title="Select input file", parent=self.root
        )
        self.input_file_label.config(text=self.input_file)
        self.augment_button.config(state=NORMAL)

    @staticmethod
    def call_api(isbn):
        url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
        result = json.loads(requests.get(url).content)
        if result:
            return result[f"ISBN:{isbn}"]
        else:
            return False

    def augment_data(self):
        df = pd.read_csv(self.input_file, names=["ISBN"])
        df["JSON"] = df["ISBN"].apply(App.call_api)
        df["Authors"] = df["JSON"].apply(
            lambda x: "; ".join(author["name"] for author in x["authors"]) if x else None
        )
        df["Title"] = df["JSON"].apply(lambda x: x["title"] if x else None)

        self.df = df

        self.save_button.config(state=NORMAL)
        messagebox.showinfo(title="Done!", message="Data successfully augmented!", parent=self.root)

    def save(self):
        save_path = filedialog.asksaveasfilename(
            title="Choose output Location", parent=self.root
        )
        self.df[["ISBN", "Authors", "Title"]].to_csv(save_path)


App()