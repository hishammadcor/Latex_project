import tkinter as tk
from tkinter import filedialog, messagebox
from Project_delta.Generator.table_generator import LaTeXTableGenerator


class LaTeXTableGeneratorUI:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("LaTeX Table Generator")
        self.directory_path = ""

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

        self.radio_frame = tk.Frame(self.main_frame)
        self.radio_frame.pack(pady=5)

        # Radio buttons for choosing where to apply format style
        self.choose_which_var = tk.StringVar(value="column")
        self.column_radio = tk.Radiobutton(self.radio_frame, text="Columns", variable=self.choose_which_var,
                                           value="column")
        self.row_radio = tk.Radiobutton(self.radio_frame, text="Rows", variable=self.choose_which_var, value="row")

        self.column_radio.pack(anchor='w', pady=2)
        self.row_radio.pack(anchor='w', pady=2)

        self.censored_var = tk.BooleanVar(value=False)
        self.censored_check = tk.Checkbutton(self.main_frame, text="Is there Data to be censored? if not leave unchecked",
                                             variable=self.censored_var, command=self.toggle_censored_entries)
        self.censored_check.pack(pady=5, anchor='w')

        self.trigger_column_label = tk.Label(self.main_frame, text="Enter Trigger column number")
        self.trigger_column_entry = tk.Entry(self.main_frame, width=10)

        self.affected_columns_label = tk.Label(self.main_frame, text="Enter Affected columns numbers")
        self.affected_columns_entry = tk.Entry(self.main_frame, width=10)

        self.toggle_censored_entries()

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

    def toggle_censored_entries(self):
        if self.censored_var.get():
            self.trigger_column_label.pack(pady=5, after=self.censored_check)
            self.trigger_column_entry.pack(pady=5, after=self.trigger_column_label)
            self.affected_columns_label.pack(pady=5, after=self.trigger_column_entry)
            self.affected_columns_entry.pack(pady=5, after=self.affected_columns_label)
        else:
            self.trigger_column_label.pack_forget()
            self.trigger_column_entry.pack_forget()
            self.affected_columns_label.pack_forget()
            self.affected_columns_entry.pack_forget()

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.process_button.config(state=tk.NORMAL)

    def process_directory(self):
        layout_style: str = self.layout_style_entry.get()
        format_style: str = self.format_style_entry.get()
        choose_which: str = self.choose_which_var.get()
        first_row_italic: bool = self.first_row_italic_var.get()
        horizontal_line: bool = self.horizontal_line_var.get()
        trigger_column = self.trigger_column_entry.get() if self.censored_var.get() else None
        affected_columns = self.affected_columns_entry.get() if self.censored_var.get() else None

        generator = LaTeXTableGenerator(self.directory_path, layout_style, format_style, first_row_italic,
                                        horizontal_line, choose_which, trigger_column, affected_columns)
        result: str = generator.generate_full_tabular()
        messagebox.showinfo('Result', result)
