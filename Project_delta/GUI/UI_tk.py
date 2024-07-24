import tkinter as tk
from tkinter import filedialog, messagebox
from Project_delta.Generator.table_generator import LaTeXTableGenerator


class LaTeXTableGeneratorUI:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("LaTeX Table Generator")
        self.directory_path = ""

        self.label = tk.Label(root_window, text="Select a directory containing CSV files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root_window, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=10)

        self.column_style_label = tk.Label(root_window, text="Enter column styles (e.g., ABCdeFE):")
        self.column_style_label.pack(pady=5)

        self.column_styles_entry = tk.Entry(root_window)
        self.column_styles_entry.pack(pady=5)

        self.first_row_italic_var = tk.BooleanVar(value=False)
        self.first_row_italic_check = tk.Checkbutton(root_window, text="First Row Italic",
                                                     variable=self.first_row_italic_var)
        self.first_row_italic_check.pack(pady=5)

        self.horizontal_line_var = tk.BooleanVar(value=False)
        self.horizontal_line_check = tk.Checkbutton(root_window, text="Remove Horizontal Line under the First Row",
                                                    variable=self.horizontal_line_var)
        self.horizontal_line_check.pack(pady=5)

        self.process_button = tk.Button(root_window, text="Generate LaTeX Tables", command=self.process_directory)
        self.process_button.pack(pady=10)
        self.process_button.config(state=tk.DISABLED)

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.process_button.config(state=tk.NORMAL)

    def process_directory(self):
        column_styles = self.column_styles_entry.get()
        first_row_italic = self.first_row_italic_var.get()
        horizontal_line = self.horizontal_line_var.get()
        generator = LaTeXTableGenerator(self.directory_path, column_styles, first_row_italic, horizontal_line)
        result = generator.generate_full_tabular
        messagebox.showinfo("Result", result)
