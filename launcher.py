import os
import json
from tkinter import ttk
import tkinter as tk


def run_external_script(name: str):
    # Launches another python file as a separate process
    os.system(f"uv run {name}")


def display_selection():
    # Get the selected value.
    selection = combo.get()
    path: str = [d[selection] for d in data if selection in d]
    # print(f"{selection=}, {key=}, {path=}")
    os.system(f"uv run {path[0]}")


main_window = tk.Tk()
main_window.config(width=300, height=200)
# Quick command to center the window
main_window.eval("tk::PlaceWindow . center")

# loads apps metadata
with open("apps.json", "r") as f:
    data = json.load(f)

main_window.title("RAYGUI APPS")
combo = ttk.Combobox(state="readonly", values=[k for x in data for k in x.keys()])
combo.set("Choose an app")
combo.place(x=50, y=50)
button = ttk.Button(text="run script", command=display_selection)
button.place(x=100, y=120)
main_window.mainloop()
