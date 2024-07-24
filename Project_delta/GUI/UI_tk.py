import tkinter as tk
from tkinter import filedialog, messagebox
from Project_delta.Generator.table_generator import LaTeXTableGenerator


class LaTeXTableGeneratorUI:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("LaTeX Table Generator")
        self.directory_path = ""

        # Configure grid layout to make the root window dynamic
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(root_window)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.label = tk.Label(self.main_frame, text="Select a directory containing CSV files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self.main_frame, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=10)

        self.layout_style_label = tk.Label(self.main_frame, text="Enter Layout style (e.g., AaBbCcDd):")
        self.layout_style_label.pack(pady=5)

        self.layout_style_entry = tk.Entry(self.main_frame, width=40)
        self.layout_style_entry.pack(pady=5)

        self.format_style_label = tk.Label(self.main_frame, text="Enter Format style (e.g., 012345):")
        self.format_style_label.pack(pady=5)

        self.format_style_entry = tk.Entry(self.main_frame, width=40)
        self.format_style_entry.pack(pady=5)

        # Frame for the radio buttons
        self.radio_frame = tk.Frame(self.main_frame)
        self.radio_frame.pack(pady=5)

        # Radio buttons for format style
        self.choose_which_var = tk.StringVar(value="column")
        self.column_radio = tk.Radiobutton(self.radio_frame, text="Columns", variable=self.choose_which_var, value="column")
        self.row_radio = tk.Radiobutton(self.radio_frame, text="Rows", variable=self.choose_which_var, value="row")

        self.column_radio.pack(anchor='w', pady=2)
        self.row_radio.pack(anchor='w', pady=2)

        self.first_row_italic_var = tk.BooleanVar(value=False)
        self.first_row_italic_check = tk.Checkbutton(self.main_frame, text="First Row Italic",
                                                     variable=self.first_row_italic_var)
        self.first_row_italic_check.pack(anchor='w', pady=5)

        self.horizontal_line_var = tk.BooleanVar(value=False)
        self.horizontal_line_check = tk.Checkbutton(self.main_frame, text="Remove Horizontal Line under the First Row",
                                                    variable=self.horizontal_line_var)
        self.horizontal_line_check.pack(pady=5, anchor='w')

        self.process_button = tk.Button(self.main_frame, text="Generate LaTeX Tables", command=self.process_directory)
        self.process_button.pack(anchor='w', pady=10)
        self.process_button.config(state=tk.DISABLED)

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.process_button.config(state=tk.NORMAL)

    def process_directory(self):
        layout_style = self.layout_style_entry.get()
        format_style = self.format_style_entry.get()
        choose_which = self.choose_which_var.get()
        first_row_italic = self.first_row_italic_var.get()
        horizontal_line = self.horizontal_line_var.get()
        generator = LaTeXTableGenerator(self.directory_path, layout_style, format_style, first_row_italic, horizontal_line, choose_which)
        result = generator.generate_full_tabular()
        messagebox.showinfo("Result", result)