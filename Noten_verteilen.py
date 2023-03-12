#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2023 Andreas Janzen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tkinter as tk
from tkinter import filedialog
import shutil
import re
from datetime import datetime
import pathlib
import fnmatch

def clean_instruments(src_folder, instruments):
    # Liste, um bereinigte Instrumente zu speichern
    cleaned_instruments = []

    # Alle Instrumente durchlaufen
    for instrument in instruments:
        # Überprüfen, ob es für das Instrument Noten gibt
        for filename in os.listdir(src_folder):
            if filename.endswith(".pdf") and instrument.lower() in filename.lower():
                cleaned_instruments.append(instrument)
                break

    return cleaned_instruments

def copy_notes(src_folder, dst_folder, composition_name, instruments):
    new_data = 0
    data = 0
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for instrument in instruments:
        src_path = find_note(src_folder, f"*{instrument}*", ignore_case=False)
        if not src_path:
            continue

        dst_instrument_folder = os.path.join(dst_folder, instrument.capitalize())
        if not os.path.exists(dst_instrument_folder):
            os.makedirs(dst_instrument_folder)

        dst_path = os.path.join(dst_instrument_folder, f"{composition_name} ({instrument.capitalize()}).pdf")
        if os.path.exists(dst_path):
            src_path_date = os.path.getmtime(src_path)
            dst_path_date = os.path.getmtime(dst_path)
            if  src_path_date > dst_path_date:
                date_suffix = datetime.fromtimestamp(dst_path_date).strftime("%Y%m%d%H%M%S")
                dst_folder_backup = os.path.join(dst_instrument_folder, 'alte Noten')
                dst_path_backup = os.path.join(dst_folder_backup, f"{composition_name} ({instrument.capitalize()})_({date_suffix}).pdf")
                if not os.path.exists(dst_folder_backup):
                    os.makedirs(dst_folder_backup)
                shutil.move(dst_path, dst_path_backup)
                shutil.copy2(src_path, dst_path)
                new_data = 1
        else:
           shutil.copy2(src_path, dst_path)
           data = 1
           
    if new_data == 1 and data == 1:
        return  "Es wurden neue und aktualisierte Noten kopiert."
    if new_data == 1:
        return "Es wurden aktualisierte Noten kopiert."
    if data == 1:
        return "Es wurden neue Noten kopiert."
    if new_data == 0 and data == 0:
        return  "Es wurden keine Noten kopiert."

def check_and_format_date(date_str):
    valid_formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y.%m.%d", "%d.%m.%Y", "%Y/%m/%d", "%d/%m/%Y"]
    today = datetime.now().date()

    for format in valid_formats:
        try:
            date = datetime.strptime(date_str, format).date()
            if date >= today:
                return date.strftime("%Y.%m.%d")
            else:
                return 1
        except ValueError:
            pass

    return 0

def find_note(folder, pattern, ignore_case=False):
    if ignore_case:
        pattern = pattern.lower()

    for filename in os.listdir(folder):
        if ignore_case:
            filename = filename.lower()

        if fnmatch.fnmatch(filename, pattern):
            return os.path.join(folder, filename)

    return None

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        root_folder = pathlib.Path(__file__).parent.absolute()
        self.title("Noten ausrollen")
        self.geometry("400x200")

        self.base_folder = root_folder
        self.src_folder = None
        self.dst_folder = None
        self.instruments = []

        self.composition_label = tk.Label(self, text="Komposition:")
        self.composition_label.pack()
        self.composition_var = tk.StringVar(self)
        self.composition_var.set("Bitte auswählen")
        self.composition_menu = tk.OptionMenu(self, self.composition_var, *self.get_compositions())
        self.composition_menu.pack()

        self.date_label = tk.Label(self, text="Probedatum:")
        self.date_label.pack()
        self.date_entry = tk.Entry(self)
        self.date_entry.pack()
        self.instruments = []
        with open(os.path.join(root_folder, "instruments.txt")) as file:
            self.instruments = file.read().strip().split("\n")

        self.copy_button = tk.Button(self, text="Noten kopieren", command=self.copy)
        self.copy_button.pack()
        
    def get_compositions(self):
        compositions = []
        for filename in os.listdir(os.path.join(self.base_folder, "Kompositionen")):
            if os.path.isdir(os.path.join(self.base_folder, "Kompositionen", filename)):
                compositions.append(filename)
        return compositions

    def copy(self):
        composition_name = self.composition_var.get()
        if composition_name == "Bitte auswählen":
            tk.messagebox.showerror("Fehler", "Bitte eine Komposition auswählen.")
            return

        date = self.date_entry.get().strip()
        if not date:
            tk.messagebox.showerror("Fehler", "Bitte ein Probedatum eingeben.")
            return

        date = check_and_format_date(date)
        if date == 0:
            tk.messagebox.showerror("Fehler", "Datum hat falsches Format.")
            return

        if date == 1:
            tk.messagebox.showerror("Fehler", "Das Datum darf nicht in der Vergangenheit liegen.")
            return

        if not self.instruments:
            tk.messagebox.showerror("Fehler", "Bitte Instrumente auswählen.")
            return

        self.src_folder = os.path.join(self.base_folder, "Kompositionen", composition_name, "Einzelstimmen")
        self.dst_folder = os.path.join(self.base_folder, "Probenmaterial", f"Vortrag {date}")
        self.instruments = clean_instruments(self.src_folder, self.instruments)
        
        
        info = copy_notes(self.src_folder, self.dst_folder, composition_name, self.instruments)
        tk.messagebox.showinfo("Erfolg", info)
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
