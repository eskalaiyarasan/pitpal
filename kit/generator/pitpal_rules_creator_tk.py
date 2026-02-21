#!/usr/bin/env python3
# Copyright (C) 2026 Pitpal
#
# This file is part of PitPal.
#
# PitPal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# either version 3 of the License, or (at your option) any later version.
#
# PitPal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PitPal. If not, see <https://www.gnu.org/licenses/>.
#    Author    :  Kalaiyarasan Es
#    File name :  pitpal/kit/generator/pitpal_rules_creator_tk.py
#    Date      :  21/02/2026
#######################################################################
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from jsonschema import validate, ValidationError
#from jsonschema import Draft202012Validator, RefResolver
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


class RuleGenerator:

    def __init__(self, root, schema_path):
        self.root = root
        self.schema_path = schema_path
        self.base_dir = os.path.dirname(schema_path)

        with open(schema_path, "r") as f:
            self.schema = json.load(f)

        self.sections = list(self.schema.get("properties", {}).keys())
        self.current_index = 0

        self.widgets = {}
        self.data_store = {}

        self.build_layout()
        self.show_section()

    # ---------------------------------------------------
    # Layout with Scroll Support
    # ---------------------------------------------------

    def build_layout(self):

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Navigation (fixed bottom)
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(fill="x", pady=10)

        self.back_btn = ttk.Button(self.nav_frame, text="Back", command=self.prev_section)
        self.back_btn.pack(side="left", padx=10)

        self.next_btn = ttk.Button(self.nav_frame, text="Next", command=self.next_section)
        self.next_btn.pack(side="right", padx=10)

        self.progress_label = ttk.Label(self.nav_frame, text="")
        self.progress_label.pack()

    # ---------------------------------------------------
    # Schema Utilities
    # ---------------------------------------------------

    def resolve_ref(self, ref):
        if "#" in ref:
            file_path, path = ref.split("#", 1)
        else:
            file_path = ref
            path = ""

        full_path = os.path.join(self.base_dir, file_path)

        try:
            with open(full_path, "r") as f:
                schema = json.load(f)
        except Exception as e:
            messagebox.showerror("Schema Error", f"Error loading {full_path}\n{e}")
            raise e

        if path:
            for part in path.strip("/").split("/"):
                schema = schema[part]

        return schema

    def merge_allOf(self, schema):
        if "allOf" not in schema:
            return schema

        merged = {}

        for key, value in schema.items():
            if key != "allOf":
                merged[key] = value

        for item in schema["allOf"]:
            if "$ref" in item:
                item = self.resolve_ref(item["$ref"])

            item = self.merge_allOf(item)

            for k, v in item.items():
                if k == "properties":
                    merged.setdefault("properties", {}).update(v)
                else:
                    merged[k] = v

        return merged

    # ---------------------------------------------------
    # Section Rendering
    # ---------------------------------------------------

    def show_section(self):

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        section_name = self.sections[self.current_index]
        section_schema = self.schema["properties"][section_name]

        if "$ref" in section_schema:
            section_schema = self.resolve_ref(section_schema["$ref"])

        section_schema = self.merge_allOf(section_schema)

        ttk.Label(
            self.scrollable_frame,
            text=section_name.upper(),
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        if "type" in section_schema and section_schema["type"] != "object":
            self.build_single_field(section_schema, section_name)
        else:
            self.build_form(section_schema, section_name)

        self.update_navigation()

    # ---------------------------------------------------
    # Field Builders
    # ---------------------------------------------------

    def build_single_field(self, schema, path):

        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill="x", pady=10, padx=10)

        ttk.Label(frame, text=path).pack(side="left")

        fld_type =[]
        fldtype = schema.get("type")
        default = schema.get("default", "")
        if  isinstance(fldtype, list):
            fld_type = fld_type + fldtype
        else:
            fld_type.append(fldtype)

        for  field_type in fld_type:
            if field_type == "string":
                var = tk.StringVar(value=default)

                if "enum" in schema:
                    widget = ttk.Combobox(
                        frame,
                        textvariable=var,
                        values=schema["enum"],
                        state="readonly"
                    )
                elif "const" in schema:
                    const = schema["const"]
                    var = tk.StringVar(value=str(const) )
                    widget = ttk.Label(frame,textvariable=var)
                else:
                    widget = ttk.Entry(frame, textvariable=var)

                widget.pack(side="right")

            elif field_type == "boolean":
                var = tk.BooleanVar(value=default)
                widget = ttk.Checkbutton(frame, variable=var)
                widget.pack(side="right")
    
            elif field_type == "integer":
                var = tk.StringVar(value=str(default))
                widget = ttk.Entry(frame, textvariable=var)
                widget.pack(side="right")

            elif field_type == "array":
                def open_array_editor():
                    self.data_store[path] = []
                    self.open_array_popup(path, schema)
                widget = ttk.Button(frame,text="Edit Array",command=open_array_editor)
                widget.pack(side="right")
            elif field_type == "null":
                def open_null_editor():
                    self.data_store[path] = None
                widget = ttk.Button(frame,text="Edit Array",command=open_null_editor)
                widget.pack(side="right")
            else:
                return

        self.widgets[path] = var

    def build_form(self, schema, parent_path, parent_key=None):
        if parent_key:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill="x", pady=5, padx=20)
            ttk.Label(frame, text="----" + str(parent_key) +"----").pack(side="left")

        properties = schema.get("properties", {})

        for key, prop in properties.items():

            full_key = f"{parent_path}.{key}"

            if "$ref" in prop:
                prop = self.resolve_ref(prop["$ref"])

            prop = self.merge_allOf(prop)

            # Nested object (Parameter grouping)
            if prop.get("type") == "object":
                self.build_form(prop, full_key,key)
                continue

            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill="x", pady=5, padx=20)

            ttk.Label(frame, text=key).pack(side="left")

            field_type = prop.get("type")
            if  isinstance(field_type, list):
                for sub_type in field_type:
                    self.build_inside_form(frame, full_key, prop,sub_type)
            else:
                self.build_inside_form(frame, full_key, prop,field_type)


    def build_inside_form(self, frame , full_key,prop,field_type ):
            default = prop.get("default", "")
            var=None
            if field_type == "boolean":
                var = tk.BooleanVar(value=default)
                widget = ttk.Checkbutton(frame, variable=var)
                widget.pack(side="right")

            elif field_type == "string":
                var = tk.StringVar(value=default)
                if "enum" in prop:
                    widget = ttk.Combobox(
                        frame,
                        textvariable=var,
                        values=prop["enum"],
                        state="readonly"
                    )
                elif "const" in prop:
                    const = prop.get("const","")
                    var = tk.StringVar(value=str(const) )
                    widget = ttk.Label(frame,textvariable=var)
                else:
                    widget = ttk.Entry(frame, textvariable=var)
                widget.pack(side="right")

            elif field_type == "integer":
                var = tk.StringVar(value=str(default))
                widget = ttk.Entry(frame, textvariable=var)
                widget.pack(side="right")

            elif field_type == "array":
                def open_array_editor(full_key=full_key, prop=prop):
                    self.open_array_popup(full_key, prop)
                widget = ttk.Button(frame,text="Edit Array",command=open_array_editor)
                widget.pack(side="right")
            elif field_type == "null":
                def open_null_editor(full_key=full_key ):
                    self.data_store[full_key] = None
                widget = ttk.Button(frame,text="set NULL",command=open_null_editor)
                widget.pack(side="right")
            else:
                return

            self.widgets[full_key] = var
    
    def open_array_popup(self, key, prop):
        popup = ttk.Frame(self.scrollable_frame)
        popup.pack(side="right")
        items_schema = prop.get("items", {})
        item_type = items_schema.get("type", "string")
        ttk.Label(popup, text="Number of elements:").pack(pady=5)

        count_var = tk.IntVar(value=0)
        count_entry = ttk.Entry(popup, textvariable=count_var)
        count_entry.pack(pady=5)

        entries_frame = ttk.Frame(popup)
        entries_frame.pack(fill="both", expand=True, pady=10)
        entry_vars = []

        def generate_fields():
            for widget in entries_frame.winfo_children():
                widget.destroy()
            entry_vars.clear()
            try:
                count = count_var.get()
            except:
                return
            for i in range(count):
                row = ttk.Frame(entries_frame)
                row.pack(fill="x", pady=3)
                ttk.Label(row, text=str(i + 1)).pack(side="left", padx=5)
                var = tk.StringVar()
                entry = ttk.Entry(row, textvariable=var)
                entry.pack(side="right", padx=5)
                entry_vars.append(var)
        ttk.Button(popup, text="Generate", command=generate_fields).pack(pady=5)
        
        def submit():
            result = []
            for var in entry_vars:
                value = var.get()
                if item_type == "integer":
                    try:
                        value = int(value)
                    except:
                        messagebox.showerror("Error", "Invalid integer value")
                        return
                elif item_type == "boolean":
                    value = value.lower() in ["true", "1", "yes"]
                result.append(value)
            self.data_store[key] = result
            popup.destroy()

        def cancel():
            popup.destroy()

        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Submit", command=submit).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side="right", padx=10)
    # ---------------------------------------------------
    # Navigation
    # ---------------------------------------------------

    def next_section(self):
        self.store_current_section()

        if self.current_index < len(self.sections) - 1:
            self.current_index += 1
            self.show_section()
        else:
            self.finish()

    def prev_section(self):
        self.store_current_section()

        if self.current_index > 0:
            self.current_index -= 1
            self.show_section()

    def update_navigation(self):
        self.back_btn.config(
            state="normal" if self.current_index > 0 else "disabled"
        )

        if self.current_index == len(self.sections) - 1:
            self.next_btn.config(text="Finish")
        else:
            self.next_btn.config(text="Next")

        self.progress_label.config(
            text=f"Step {self.current_index + 1} of {len(self.sections)}"
        )

    # ---------------------------------------------------
    # Data Handling
    # ---------------------------------------------------

    def store_current_section(self):
        for key, var in self.widgets.items():
            if var is None:
                continue
            self.data_store[key] = var.get()

    def collect_data(self):
        result = {}

        for key, value in self.data_store.items():
            keys = key.split(".")
            current = result
            for part in keys[:-1]:
                current = current.setdefault(part, {})
            current[keys[-1]] = value

        return result

    # ---------------------------------------------------
    # Finish
    # ---------------------------------------------------
    def finish(self):
        final_data = self.collect_data()	
        try:
            # Load all schemas in the schema folder
            registry = Registry()
            for filename in os.listdir(self.base_dir):
                if filename.endswith(".json"):
                    full_path = os.path.join(self.base_dir, filename)
                    with open(full_path, "r") as f:
                        schema_data = json.load(f)
                    # Use $id if available, else file URI
                    schema_id = schema_data.get(
                            "$id",f"file://{full_path}")
                    registry = registry.with_resource( schema_id,
                            Resource.from_contents(schema_data))
            # Create validator with registry
            validator = Draft202012Validator(self.schema,
                registry=registry)
            #validator.validate(final_data)
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".json",
                filetypes=[("JSON files", "*.json")])
        if save_path:
            with open(save_path, "w") as f:
                json.dump(final_data, f, indent=2)
            messagebox.showinfo("Success", "Rule JSON generated successfully!")



# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    root = tk.Tk()
    root.title("PitPal Rule Wizard")
    root.geometry("800x700")

    schema_path = filedialog.askopenfilename(
        title="Select game.rule.schema.json",
        filetypes=[("JSON files", "*.json")]
    )

    if not schema_path:
        return

    RuleGenerator(root, schema_path)
    root.mainloop()


if __name__ == "__main__":
    main()
