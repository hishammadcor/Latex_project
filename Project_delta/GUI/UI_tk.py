import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Project_delta.Generator.table_generator import LaTeXTableGenerator
import pandas as pd
import os

APP_VERSION = "2.3.1"


class LaTeXTableGeneratorUI:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title(f"LaTeX Table Generator v{APP_VERSION}")
        self.directory_path = ""
        self.styles_data = {}
        self.styles_data_path = ""
        self.width = None

        # Configure grid layout for better structure
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(root_window)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Section 1: Table Styles
        style_frame = tk.LabelFrame(self.main_frame, text="Table Style Selection", padx=10, pady=10)
        style_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.load_table_styles_button = tk.Button(style_frame, text='Load Table Styles', command=self.load_style)
        self.load_table_styles_button.grid(row=0, column=0, sticky="w", pady=5)

        self.styles_label = tk.Label(style_frame, text="No Styles File selected")
        self.styles_label.grid(row=1, column=0, sticky="w", pady=5)

        self.table_style_name_combobox = ttk.Combobox(style_frame, values=[], width=40)
        self.table_style_name_combobox.grid(row=2, column=0, sticky="ew", pady=5)
        self.table_style_name_combobox.bind("<<ComboboxSelected>>", self.on_style_name_selected)

        # Section 2: Directory Selection
        directory_frame = tk.LabelFrame(self.main_frame, text="CSV Directory Selection", padx=10, pady=10)
        directory_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.select_button = tk.Button(directory_frame, text="Select Directory", command=self.select_directory)
        self.select_button.grid(row=0, column=0, sticky="w", pady=5)

        self.directory_label = tk.Label(directory_frame, text="No directory selected")
        self.directory_label.grid(row=1, column=0, sticky="w", pady=5)

        # Section 3: Style Options
        style_options_frame = tk.LabelFrame(self.main_frame, text="Table Style Options", padx=10, pady=10)
        style_options_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.layout_style_label = tk.Label(style_options_frame, text="Layout Style (e.g. AaBbCcDd):")
        self.layout_style_label.grid(row=0, column=0, sticky="w", pady=5)

        self.layout_style_var = tk.StringVar()
        self.layout_style_entry = tk.Entry(style_options_frame, textvariable=self.layout_style_var, width=30)
        self.layout_style_entry.grid(row=0, column=1, sticky="w", pady=5)

        self.format_style_label = tk.Label(style_options_frame, text="Format Style (e.g. 012345):")
        self.format_style_label.grid(row=1, column=0, sticky="w", pady=5)

        self.format_style_var = tk.StringVar()
        self.format_style_entry = tk.Entry(style_options_frame, textvariable=self.format_style_var, width=30)
        self.format_style_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Orientation Selection
        orientation_frame = tk.LabelFrame(style_options_frame, text="Orientation")
        orientation_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)

        self.choose_which_var = tk.StringVar(value="column")
        self.column_radio = tk.Radiobutton(orientation_frame, text="Columns", variable=self.choose_which_var,
                                           value="column")
        self.column_radio.grid(row=0, column=0, sticky="w", padx=5)

        self.row_radio = tk.Radiobutton(orientation_frame, text="Rows", variable=self.choose_which_var, value="row")
        self.row_radio.grid(row=0, column=1, sticky="w", padx=5)

        # Section 4: Censoring Options
        censoring_options_frame = tk.LabelFrame(self.main_frame, text="Censoring Options", padx=10, pady=10)
        censoring_options_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.censored_var = tk.BooleanVar(value=False)
        self.censored_check = tk.Checkbutton(censoring_options_frame, text="Censor Data?", variable=self.censored_var,
                                             command=self.toggle_censored_entries)
        self.censored_check.grid(row=0, column=0, sticky="w", pady=5)

        # Censoring Mode (Column or Cell)
        self.censor_mode_var = tk.StringVar(value="column")
        self.column_censor_radio = tk.Radiobutton(censoring_options_frame, text="Column Censoring",
                                                  variable=self.censor_mode_var, value="column")
        self.cell_censor_radio = tk.Radiobutton(censoring_options_frame, text="Cell Censoring",
                                                variable=self.censor_mode_var, value="cell")

        # Trigger-related fields (appear when Column mode is checked)
        self.column_trigger_number_var = tk.StringVar(value='5')
        self.column_trigger_number_label = tk.Label(censoring_options_frame, text="Trigger Value (e.g., less than):")
        self.column_trigger_number_entry = tk.Entry(censoring_options_frame,
                                                    textvariable=self.column_trigger_number_var, width=10)

        self.trigger_column_label = tk.Label(censoring_options_frame, text="Trigger Column Number:")
        self.trigger_column_entry = tk.Entry(censoring_options_frame, width=10)

        self.affected_columns_label = tk.Label(censoring_options_frame, text="Affected Column Numbers (e.g., 1,2,5):")
        self.affected_columns_entry = tk.Entry(censoring_options_frame, width=20)

        # Trigger-related fields (appear when Cell mode is checked)
        self.cell_trigger_number_var = tk.StringVar(value='5')
        self.cell_trigger_number_label = tk.Label(censoring_options_frame, text="Trigger Value (e.g., less than):")
        self.cell_trigger_number_entry = tk.Entry(censoring_options_frame, textvariable=self.cell_trigger_number_var,
                                                  width=10)

        self.number_affected_cells_var = tk.StringVar(value='1')
        self.number_affected_cells_label = tk.Label(censoring_options_frame, text="Number of Affected cells:")
        self.number_affected_cells_entry = tk.Entry(censoring_options_frame,
                                                    textvariable=self.number_affected_cells_var, width=10)

        # Call toggle_censored_entries initially to set the correct visibility
        self.toggle_censored_entries()
        self.censor_mode_var.trace_add("write", lambda *args: self.toggle_censored_entries())

        #Step 5: Additional options for formatting
        additional_options_frame = tk.LabelFrame(self.main_frame, text="Additional Options", padx=10, pady=10)
        additional_options_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        self.first_row_italic_var = tk.BooleanVar(value=False)
        self.first_row_italic_check = tk.Checkbutton(additional_options_frame, text="First Row Italic",
                                                     variable=self.first_row_italic_var)
        self.first_row_italic_check.grid(row=4, column=0, sticky="w", pady=5)

        self.first_row_90_degree_var = tk.BooleanVar(value=False)
        self.first_row_90_degree_check = tk.Checkbutton(additional_options_frame, text="First Row 90° Rotated",
                                                        variable=self.first_row_90_degree_var)
        self.first_row_90_degree_check.grid(row=4, column=1, sticky="w", pady=5)

        self.first_row_bold_var = tk.BooleanVar(value=False)
        self.first_row_bold_check = tk.Checkbutton(additional_options_frame, text="First Row Bold",
                                                   variable=self.first_row_bold_var)
        self.first_row_bold_check.grid(row=5, column=0, sticky="w", pady=5)

        self.horizontal_line_var = tk.BooleanVar(value=False)
        self.horizontal_line_check = tk.Checkbutton(additional_options_frame, text="Remove Horizontal Line",
                                                    variable=self.horizontal_line_var)
        self.horizontal_line_check.grid(row=5, column=1, sticky="w", pady=5)

        self.remove_table_caption_var = tk.BooleanVar(value=False)
        self.remove_table_caption_check = tk.Checkbutton(additional_options_frame, text="Remove Table Caption",
                                                         variable=self.remove_table_caption_var)
        self.remove_table_caption_check.grid(row=6, column=0, sticky="w", pady=5)

        self.remove_table_headline_var = tk.BooleanVar(value=False)
        self.remove_table_headline_check = tk.Checkbutton(additional_options_frame, text="Remove Table Headline",
                                                          variable=self.remove_table_headline_var)
        self.remove_table_headline_check.grid(row=6, column=1, sticky="w", pady=5)

        self.remove_column_names_var = tk.BooleanVar(value=False)
        self.remove_column_names_check = tk.Checkbutton(additional_options_frame, text="Table with no column names?",
                                                        variable=self.remove_column_names_var)
        self.remove_column_names_check.grid(row=7, column=0, sticky="w", pady=5)

        self.multirow_var = tk.BooleanVar(value=False)
        self.multirow_check = tk.Checkbutton(additional_options_frame, text="Multirow",
                                             variable=self.multirow_var)
        self.multirow_check.grid(row=7, column=1, sticky="w", pady=5)

        self.version_label = tk.Label(self.main_frame, text=f"Version {APP_VERSION}", font=("Arial", 10))
        self.version_label.grid(row=6, column=0, sticky="se", pady=5)

        # Section 5: Generate Button
        self.process_button = tk.Button(self.main_frame, text="Generate LaTeX Tables", command=self.process_directory)
        self.process_button.grid(row=7, column=0, sticky="e", pady=10)
        self.process_button.config(state=tk.DISABLED)

    def toggle_censored_entries(self):
        if self.censored_var.get():  # Check if the Censor checkbox is checked
            self.column_censor_radio.grid(row=1, column=0, sticky="w", pady=5)
            self.cell_censor_radio.grid(row=1, column=1, sticky="w", pady=5)

            self.column_trigger_number_label.grid_forget()
            self.column_trigger_number_entry.grid_forget()
            self.trigger_column_label.grid_forget()
            self.trigger_column_entry.grid_forget()
            self.affected_columns_label.grid_forget()
            self.affected_columns_entry.grid_forget()
            self.cell_trigger_number_label.grid_forget()
            self.cell_trigger_number_entry.grid_forget()
            self.number_affected_cells_label.grid_forget()
            self.number_affected_cells_entry.grid_forget()

            if self.censor_mode_var.get() == "column":
                self.column_trigger_number_label.grid(row=2, column=0, sticky="w", pady=5)
                self.column_trigger_number_entry.grid(row=2, column=1, sticky="w", pady=5)
                self.trigger_column_label.grid(row=3, column=0, sticky="w", pady=5)
                self.trigger_column_entry.grid(row=3, column=1, sticky="w", pady=5)
                self.affected_columns_label.grid(row=4, column=0, sticky="w", pady=5)
                self.affected_columns_entry.grid(row=4, column=1, sticky="w", pady=5)

            elif self.censor_mode_var.get() == "cell":
                self.cell_trigger_number_label.grid(row=5, column=0, sticky="w", pady=5)
                self.cell_trigger_number_entry.grid(row=5, column=1, sticky="w", pady=5)
                self.number_affected_cells_label.grid(row=3, column=0, sticky="w", pady=5)
                self.number_affected_cells_entry.grid(row=3, column=1, sticky="w", pady=5)
        else:
            self.column_censor_radio.grid_forget()
            self.cell_censor_radio.grid_forget()
            self.column_trigger_number_label.grid_forget()
            self.column_trigger_number_entry.grid_forget()
            self.trigger_column_label.grid_forget()
            self.trigger_column_entry.grid_forget()
            self.affected_columns_label.grid_forget()
            self.affected_columns_entry.grid_forget()
            self.cell_trigger_number_label.grid_forget()
            self.cell_trigger_number_entry.grid_forget()
            self.number_affected_cells_label.grid_forget()
            self.number_affected_cells_entry.grid_forget()

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.directory_label.config(text=f"Selected: {self.directory_path}")
            self.process_button.config(state=tk.NORMAL)

    @staticmethod
    def read_styles_file_column(csv_path):
        styles_data = {}
        styles = pd.read_csv(csv_path, delimiter=';', encoding='utf-8', header=0, skip_blank_lines=False)
        styles = styles.fillna('').map(lambda x: str(x).strip())

        variable_column = styles.iloc[:, 0]  # The first column contains variable names, the remaining columns represent styles
        style_columns = styles.iloc[:, 1:]  # All columns after the first column are style values

        style_names = style_columns.columns

        for style_name in style_names:
            style_values = style_columns[style_name]
            style_data = dict(zip(variable_column, style_values))
            style_data = {k: v for k, v in style_data.items() if k}  # Remove empty keys

            styles_data[style_name] = style_data

        return styles_data

    def load_style(self):
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            self.styles_data_path = os.path.dirname(os.path.abspath(csv_file_path))
            self.styles_label.config(text=f"Selected: {csv_file_path}")
            self.process_button.config(state=tk.NORMAL)
            self.styles_data = self.read_styles_file_column(csv_file_path)
            # self.styles_data = self.read_styles_file_row(csv_file_path)
            style_names = list(self.styles_data.keys())
            self.table_style_name_combobox.config(values=style_names)
            messagebox.showinfo("Success", "Table styles are loaded successfully")

    def on_style_name_selected(self, event):
        selected_style = self.table_style_name_combobox.get()
        if selected_style in self.styles_data:
            settings = self.styles_data[selected_style]
            self.apply_style_settings(settings)

    def apply_style_settings(self, settings):
        mapping = {
            'Layout': ('layout_style_var', 'stringvar'),
            'Format': ('format_style_var', 'stringvar'),
            'Orientation': ('choose_which_var', 'orientation'),
            'Censoring': ('censored_var', 'booleanvar'),
            'censoringMode': ('censor_mode_var', 'censormode'),
            'TriggerColumnValue': ('column_trigger_number_var', 'stringvar'),
            'TriggerColumn': ('trigger_column_entry', 'entry'),
            'AffectedColumns': ('affected_columns_entry', 'entry'),
            'CellTriggerValue': ('cell_trigger_number_var', 'stringvar'),
            'NumberOfCells': ('number_affected_cells_var', 'stringvar'),
            'FirstRowItalics': ('first_row_italic_var', 'booleanvar'),
            'FirstRow90': ('first_row_90_degree_var', 'booleanvar'),
            'FirstRowBold': ('first_row_bold_var', 'booleanvar'),
            'RemoveHline': ('horizontal_line_var', 'booleanvar'),
            'RemoveCaption': ('remove_table_caption_var', 'booleanvar'),
            'RemoveHeadline': ('remove_table_headline_var', 'booleanvar'),
            'RemoveColumnNames': ('remove_column_names_var', 'booleanvar'),
            'MultiRow': ('multirow_var', 'booleanvar')
        }

        for key, (ui_element_name, ui_element_type) in mapping.items():
            if key in settings:
                value = settings[key]
                if key == 'Layout' and value.startswith('A'):
                    self.width = 20
                elif key == 'Layout' and value.startswith('B'):
                    self.width = 30
                elif key == 'Layout' and value.startswith('C'):
                    self.width = 40
                elif key == 'Layout' and value.startswith('D'):
                    self.width = 50
                elif key == 'Layout' and value.startswith('E'):
                    self.width = 70
                elif key == 'Layout' and value.startswith('F'):
                    self.width = 110

                if ui_element_type == 'stringvar':
                    stringvar = getattr(self, ui_element_name)
                    stringvar.set(value)
                elif ui_element_type == 'booleanvar':
                    booleanvar = getattr(self, ui_element_name)
                    booleanvar.set(value == '1')
                elif ui_element_type == 'entry':
                    entry = getattr(self, ui_element_name)
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
                elif ui_element_type == 'orientation':
                    orientation = value.strip().lower()
                    if orientation in ('columns', 'column'):
                        self.choose_which_var.set('column')
                    elif orientation in ('rows', 'row'):
                        self.choose_which_var.set('row')
                    else:
                        self.choose_which_var.set('column')
                elif ui_element_type == 'mode':
                    mode = value.strip().lower()
                    if mode in ('columns', 'column'):
                        self.censor_mode_var.set('column')
                    elif mode in ('cells', 'cell'):
                        self.censor_mode_var.set('cell')
                    else:
                        self.censor_mode_var.set('column')

        # self.root_window.after(100, self.toggle_censored_entries)
        self.toggle_censored_entries()

    def process_directory(self):
        layout_style: str = self.layout_style_var.get()
        format_style: str = self.format_style_var.get()
        choose_which: str = self.choose_which_var.get()
        first_row_italic: bool = self.first_row_italic_var.get()
        first_row_90_degree: bool = self.first_row_90_degree_var.get()
        first_row_bold: bool = self.first_row_bold_var.get()
        horizontal_line: bool = self.horizontal_line_var.get()
        remove_table_caption: bool = self.remove_table_caption_var.get()
        remove_table_headline: bool = self.remove_table_headline_var.get()
        censored: bool = self.censored_var.get()
        censor_mode: str = self.censor_mode_var.get() if self.censored_var.get() else None
        column_trigger_number: str = self.column_trigger_number_entry.get() if self.censored_var.get() else None
        trigger_column = self.trigger_column_entry.get() if self.censored_var.get() else None
        affected_columns = self.affected_columns_entry.get() if self.censored_var.get() else None
        cell_trigger_number: str = self.cell_trigger_number_var.get() if self.censored_var.get() else None
        number_affected_cells: str = self.number_affected_cells_var.get() if self.censored_var.get() else None
        styles_dir_path = self.styles_data_path
        column_names: bool = self.remove_column_names_var.get()
        multirow: bool = self.multirow_var.get()
        width = self.width
        generator = LaTeXTableGenerator(self.directory_path,
                                        layout_style,
                                        format_style,
                                        first_row_italic,
                                        first_row_bold,
                                        first_row_90_degree,
                                        horizontal_line,
                                        remove_table_caption,
                                        remove_table_headline,
                                        choose_which,
                                        censored,
                                        censor_mode,
                                        column_trigger_number,
                                        trigger_column,
                                        affected_columns,
                                        cell_trigger_number,
                                        number_affected_cells,
                                        styles_dir_path,
                                        column_names,
                                        multirow,
                                        width
                                        )
        result = generator.generate_full_tabular
        messagebox.showinfo('Result', result)
