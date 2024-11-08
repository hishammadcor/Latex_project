import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Project_delta.Generator.table_generator import LaTeXTableGenerator
import pandas as pd


class LaTeXTableGeneratorUI:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("LaTeX Table Generator")
        self.directory_path = ""
        self.styles_data = {}

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
        self.column_radio = tk.Radiobutton(orientation_frame, text="Columns", variable=self.choose_which_var, value="column")
        self.column_radio.grid(row=0, column=0, sticky="w", padx=5)

        self.row_radio = tk.Radiobutton(orientation_frame, text="Rows", variable=self.choose_which_var, value="row")
        self.row_radio.grid(row=0, column=1, sticky="w", padx=5)

        # Section 4: Additional Options
        additional_options_frame = tk.LabelFrame(self.main_frame, text="Additional Options", padx=10, pady=10)
        additional_options_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        self.censored_var = tk.BooleanVar(value=False)
        self.censored_check = tk.Checkbutton(additional_options_frame, text="Censor Data?", variable=self.censored_var, command=self.toggle_censored_entries)
        self.censored_check.grid(row=0, column=0, sticky="w", pady=5)

        # Trigger-related fields (appear when Censor Data is checked)
        self.trigger_number_var = tk.StringVar(value='5')
        self.trigger_number_label = tk.Label(additional_options_frame, text="Trigger Value (e.g., less than):")
        self.trigger_number_entry = tk.Entry(additional_options_frame, textvariable=self.trigger_number_var, width=10)

        self.trigger_column_label = tk.Label(additional_options_frame, text="Trigger Column Number:")
        self.trigger_column_entry = tk.Entry(additional_options_frame, width=10)

        self.affected_columns_label = tk.Label(additional_options_frame, text="Affected Column Numbers (e.g., 1,2,5):")
        self.affected_columns_entry = tk.Entry(additional_options_frame, width=20)

        # Call toggle_censored_entries initially to set the correct visibility
        self.toggle_censored_entries()

        # Additional options for formatting rows
        self.first_row_italic_var = tk.BooleanVar(value=False)
        self.first_row_italic_check = tk.Checkbutton(additional_options_frame, text="First Row Italic", variable=self.first_row_italic_var)
        self.first_row_italic_check.grid(row=4, column=0, sticky="w", pady=5)

        self.first_row_90_degree_var = tk.BooleanVar(value=False)
        self.first_row_90_degree_check = tk.Checkbutton(additional_options_frame, text="First Row 90° Rotated", variable=self.first_row_90_degree_var)
        self.first_row_90_degree_check.grid(row=4, column=1, sticky="w", pady=5)

        self.first_row_bold_var = tk.BooleanVar(value=False)
        self.first_row_bold_check = tk.Checkbutton(additional_options_frame, text="First Row Bold", variable=self.first_row_bold_var)
        self.first_row_bold_check.grid(row=5, column=0, sticky="w", pady=5)

        self.horizontal_line_var = tk.BooleanVar(value=False)
        self.horizontal_line_check = tk.Checkbutton(additional_options_frame, text="Remove Horizontal Line", variable=self.horizontal_line_var)
        self.horizontal_line_check.grid(row=5, column=1, sticky="w", pady=5)

        self.remove_table_caption_var = tk.BooleanVar(value=False)
        self.remove_table_caption_check = tk.Checkbutton(additional_options_frame, text="Remove Table Caption",
                                                         variable=self.remove_table_caption_var)
        self.remove_table_caption_check.grid(row=6, column=0, sticky="w", pady=5)

        self.remove_table_headline_var = tk.BooleanVar(value=False)
        self.remove_table_headline_check = tk.Checkbutton(additional_options_frame, text="Remove Table Headline",
                                                          variable=self.remove_table_headline_var)
        self.remove_table_headline_check.grid(row=6, column=1, sticky="w", pady=5)

        # Section 5: Generate Button
        self.process_button = tk.Button(self.main_frame, text="Generate LaTeX Tables", command=self.process_directory)
        self.process_button.grid(row=4, column=0, sticky="e", pady=10)
        self.process_button.config(state=tk.DISABLED)

    def toggle_censored_entries(self):
        if self.censored_var.get():  # Check if the Censor checkbox is checked
            self.trigger_number_label.grid(row=1, column=0, sticky="w", pady=5)
            self.trigger_number_entry.grid(row=1, column=1, sticky="w", pady=5)
            self.trigger_column_label.grid(row=2, column=0, sticky="w", pady=5)
            self.trigger_column_entry.grid(row=2, column=1, sticky="w", pady=5)
            self.affected_columns_label.grid(row=3, column=0, sticky="w", pady=5)
            self.affected_columns_entry.grid(row=3, column=1, sticky="w", pady=5)
        else:
            self.trigger_number_label.grid_forget()
            self.trigger_number_entry.grid_forget()
            self.trigger_column_label.grid_forget()
            self.trigger_column_entry.grid_forget()
            self.affected_columns_label.grid_forget()
            self.affected_columns_entry.grid_forget()

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.directory_label.config(text=f"Selected: {self.directory_path}")
            self.process_button.config(state=tk.NORMAL)

    @staticmethod
    def read_styles_file_column(csv_path):
        styles_data = {}

        styles = pd.read_csv(csv_path, delimiter=';', encoding='utf-8', header=None, skip_blank_lines=False)
        styles = styles.fillna('').map(lambda x: str(x).strip())

        for col in range(0, len(styles.columns), 2):  # Assuming style names and settings are in pairs of columns
            style_column = col
            value_column = col + 1 if col + 1 < len(styles.columns) else col

            style_name_indices = styles.index[(styles[style_column] != '') & (styles[value_column] == '')].tolist()

            for idx, style_idx in enumerate(style_name_indices):
                style_name = styles.loc[style_idx, style_column]

                start = style_idx + 1
                end = style_name_indices[idx + 1] if idx + 1 < len(style_name_indices) else len(styles)

                settings_style = styles.iloc[start:end, [style_column, value_column]].copy()
                settings_style = settings_style[(settings_style[style_column] != '') | (settings_style[value_column] != '')]

                current_style = dict(zip(settings_style[style_column], settings_style[value_column]))
                styles_data[style_name] = current_style

        return styles_data

    def load_style(self):
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            self.styles_label.config(text=f"Selected: {csv_file_path}")
            self.process_button.config(state=tk.NORMAL)
            self.styles_data = self.read_styles_file_column(csv_file_path)
            # self.styles_data = self.read_styles_file_row(csv_file_path)
            style_names = list(self.styles_data.keys())
            self.table_style_name_combobox.config(values=style_names)
            messagebox.showinfo("Success", "Table styles are loaded successfully")

    def on_style_name_selected(self, event):
        selected_style = self.table_style_name_combobox.get()
        if selected_style and selected_style in self.styles_data:
            settings = self.styles_data[selected_style]
            self.apply_style_settings(settings)

    def apply_style_settings(self, settings):
        mapping = {
            'Layout': ('layout_style_var', 'stringvar'),
            'Format': ('format_style_var', 'stringvar'),
            'Orientation': ('choose_which_var', 'orientation'),
            'Censoring': ('censored_var', 'booleanvar'),
            'TriggerValue': ('trigger_number_var', 'stringvar'),
            'TriggerColumn': ('trigger_column_entry', 'entry'),
            'AffectedColumns': ('affected_columns_entry', 'entry'),
            'FirstRowItalics': ('first_row_italic_var', 'booleanvar'),
            'FirstRow90': ('first_row_90_degree_var', 'booleanvar'),
            'FirstRowBold': ('first_row_bold_var', 'booleanvar'),
            'RemoveHline': ('horizontal_line_var', 'booleanvar'),
            'RemoveCaption': ('remove_table_caption_var', 'booleanvar'),
            'RemoveHeadline': ('remove_table_headline_var', 'booleanvar'),
        }
        for key, (ui_element_name, ui_element_type) in mapping.items():
            if key in settings:
                value = settings[key]

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
        trigger_number: str = self.trigger_number_entry.get() if self.censored_var.get() else None
        trigger_column = self.trigger_column_entry.get() if self.censored_var.get() else None
        affected_columns = self.affected_columns_entry.get() if self.censored_var.get() else None

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
                                        trigger_number,
                                        trigger_column,
                                        affected_columns
                                        )
        result = generator.generate_full_tabular
        messagebox.showinfo('Result', result)
