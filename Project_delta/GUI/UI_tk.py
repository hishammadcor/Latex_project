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

        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(root_window)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.table_style_name_label = tk.Label(self.main_frame, text='Table style name')
        self.table_style_name_label.pack(pady=5)

        self.load_table_styles_button = tk.Button(self.main_frame, text='Load Table Styles', command=self.load_style)
        self.load_table_styles_button.pack(pady=10)

        self.table_style_name_combobox = ttk.Combobox(self.main_frame, values=[], width=40)
        self.table_style_name_combobox.pack(pady=5)
        self.table_style_name_combobox.bind("<<ComboboxSelected>>", self.on_style_name_selected)

        self.label = tk.Label(self.main_frame, text="Select a directory containing CSV files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self.main_frame, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=10)

        self.directory_label = tk.Label(self.main_frame, text="No directory selected")
        self.directory_label.pack(pady=5)

        self.layout_style_label = tk.Label(self.main_frame, text="Enter Layout style (e.g. AaBbCcDd):")
        self.layout_style_label.pack(pady=5)

        self.layout_style_combobox = ttk.Combobox(self.main_frame, values=[], width=40)
        self.layout_style_combobox.pack(pady=5)

        # self.layout_style_entry = tk.Entry(self.main_frame, width=40)
        # self.layout_style_entry.pack(pady=5)

        self.format_style_label = tk.Label(self.main_frame, text="Enter Format style (e.g. 012345):")
        self.format_style_label.pack(pady=5)

        self.format_style_combobox = ttk.Combobox(self.main_frame, values=[], width=40)
        self.format_style_combobox.pack(pady=5)

        # self.format_style_entry = tk.Entry(self.main_frame, width=40)
        # self.format_style_entry.pack(pady=5)

        self.radio_frame = tk.Frame(self.main_frame)
        self.radio_frame.pack(pady=5)

        # Radio buttons for choosing where to apply format style
        self.choose_which_var = tk.StringVar(value="column")
        self.column_radio = tk.Radiobutton(self.radio_frame, text="Columns", variable=self.choose_which_var,
                                           value="column")
        self.row_radio = tk.Radiobutton(self.radio_frame, text="Rows", variable=self.choose_which_var, value="row")
        self.row_note = tk.Label(self.radio_frame,
                                 text="Note if Rows is chosen: Start counting from the second row. eg. If the table has 6 rows, enter only 5 format style numbers.",
                                 font=("Arial", 10, "italic"), fg="gray", wraplength=300)

        self.column_radio.pack(anchor='w', pady=2)
        self.row_radio.pack(anchor='w', pady=2)
        self.row_note.pack(anchor='w', pady=2)

        self.censored_var = tk.BooleanVar(value=False)
        self.censored_check = tk.Checkbutton(self.main_frame,
                                             text="Is there Data to be censored? if not leave unchecked",
                                             variable=self.censored_var, command=self.toggle_censored_entries)
        self.censored_check.pack(pady=5, anchor='w')

        self.trigger_number_var = tk.StringVar(value='5')

        self.trigger_number_label = tk.Label(self.main_frame, text="Enter Trigger Value")

        self.trigger_number_frame = tk.Frame(self.main_frame)

        self.note_label = tk.Label(self.trigger_number_frame, text="less than/kleiner als")
        self.trigger_number_entry = tk.Entry(
            self.trigger_number_frame, width=10, textvariable=self.trigger_number_var
        )

        self.note_label.pack(side=tk.LEFT, padx=(0, 5))
        self.trigger_number_entry.pack(side=tk.LEFT)

        self.trigger_column_label = tk.Label(self.main_frame, text="Enter Trigger column number")
        self.trigger_column_entry = tk.Entry(self.main_frame, width=10)

        self.affected_columns_label = tk.Label(self.main_frame, text="Enter Affected columns numbers (e.g. 1,2,5,6):")
        self.affected_columns_entry = tk.Entry(self.main_frame, width=10)

        self.toggle_censored_entries()

        self.first_row_italic_var = tk.BooleanVar(value=False)
        self.first_row_italic_check = tk.Checkbutton(self.main_frame, text="First Row Italic",
                                                     variable=self.first_row_italic_var)
        self.first_row_italic_check.pack(anchor='w', pady=5)

        self.first_row_90_degree_var = tk.BooleanVar(value=False)
        self.first_row_90_degree_check = tk.Checkbutton(self.main_frame,
                                                        text="First row is 90 degree rotated",
                                                        variable=self.first_row_90_degree_var)
        self.first_row_90_degree_check.pack(anchor='w', pady=5)

        self.first_row_bold_var = tk.BooleanVar(value=False)
        self.first_row_bold_check = tk.Checkbutton(self.main_frame,
                                                   text="First Row Bold (Mostly checked if First row is 90 degree rotated)",
                                                   variable=self.first_row_bold_var)
        self.first_row_bold_check.pack(anchor='w', pady=5)

        self.horizontal_line_var = tk.BooleanVar(value=False)
        self.horizontal_line_check = tk.Checkbutton(self.main_frame, text="Remove Horizontal Line under the First Row",
                                                    variable=self.horizontal_line_var)
        self.horizontal_line_check.pack(pady=5, anchor='w')

        self.remove_table_caption_var = tk.BooleanVar(value=False)
        self.remove_table_caption_check = tk.Checkbutton(self.main_frame, text="Remove Table Caption",
                                                         variable=self.remove_table_caption_var)
        self.remove_table_caption_check.pack(pady=5, anchor='w')

        self.remove_table_headline_var = tk.BooleanVar(value=False)
        self.remove_table_headline_check = tk.Checkbutton(self.main_frame, text="Remove Table Headline",
                                                          variable=self.remove_table_headline_var)
        self.remove_table_headline_check.pack(pady=5, anchor='w')

        self.process_button = tk.Button(self.main_frame, text="Generate LaTeX Tables", command=self.process_directory)
        self.process_button.pack(anchor='w', pady=10)
        self.process_button.config(state=tk.DISABLED)

    def read_styles_file(self, csv_path):
        styles_data = {}
        styles = pd.read_csv(csv_path, delimiter=';', encoding='utf-8', header=None, skip_blank_lines=False)

        styles = styles.fillna('').applymap(lambda x: str(x).strip())

        styles['is_style_name'] = styles[1] == ''

        style_names = styles.index[styles['is_style_name']].tolist()

        for idx, style_idx in enumerate(style_names):

            style_name = styles.loc[style_idx, 0]

            start = style_idx + 1
            if idx + 1 < len(style_names):
                end = style_names[idx + 1]
            else:
                end = len(styles)

            settings_style = styles.iloc[start:end,[0,1]].copy()
            settings_style = settings_style[(settings_style[0] != '') | (settings_style[1] != '')]

            current_style = dict(zip(settings_style[0],settings_style[1]))

            styles_data[style_name] = current_style

        return styles_data

    def load_style(self):
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            self.styles_data = self.read_styles_file(csv_file_path)
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
            'Layout': ('layout_style_combobox', 'combobox'),
            'Format': ('format_style_combobox', 'combobox'),
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
                if ui_element_type == 'combobox':
                   combobox = getattr(self, ui_element_name)
                   combobox.set(value)
                elif ui_element_type == 'stringvar':
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

        self.toggle_censored_entries()

    def toggle_censored_entries(self):
        if self.censored_var.get():
            self.trigger_number_label.pack(pady=5, after=self.censored_check)
            self.trigger_number_frame.pack(pady=5, after=self.trigger_number_label)
            self.trigger_column_label.pack(pady=5, after=self.trigger_number_frame)
            self.trigger_column_entry.pack(pady=5, after=self.trigger_column_label)
            self.affected_columns_label.pack(pady=5, after=self.trigger_column_entry)
            self.affected_columns_entry.pack(pady=5, after=self.affected_columns_label)
        else:
            self.trigger_number_label.pack_forget()
            self.trigger_number_frame.pack_forget()
            self.trigger_column_label.pack_forget()
            self.trigger_column_entry.pack_forget()
            self.affected_columns_label.pack_forget()
            self.affected_columns_entry.pack_forget()

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.directory_label.config(text=f"Selected: {self.directory_path}")
            self.process_button.config(state=tk.NORMAL)

    def process_directory(self):
        layout_style: str = self.layout_style_combobox.get()
        format_style: str = self.format_style_combobox.get()
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

# if __name__ == "__main__":
#     def read_styles_file(csv_path):
#         styles_data = {}
#         styles = pd.read_csv(csv_path, delimiter=';', encoding='utf-8', header=None, skip_blank_lines=False)
#
#         styles = styles.fillna('').applymap(lambda x: str(x).strip())
#
#         styles['is_style_name'] = styles[1] == ''
#
#         style_names = styles.index[styles['is_style_name']].tolist()
#
#         for idx, style_idx in enumerate(style_names):
#
#             style_name = styles.loc[style_idx, 0]
#
#             start = style_idx + 1
#             if idx + 1 < len(style_names):
#                 end = style_names[idx + 1]
#             else:
#                 end = len(styles)
#
#             settings_style = styles.iloc[start:end,[0,1]].copy()
#             settings_style = settings_style[(settings_style[0] != '') | (settings_style[1] != '')]
#
#             current_style = dict(zip(settings_style[0],settings_style[1]))
#
#             styles_data[style_name] = current_style
#
#         return styles_data
#
#
#
#     csv_path = "U:/Latex_project/tex/StudienverlaufUndErfolg.csv"
#     print(read_styles_file(csv_path))
#     # read_styles_file(csv_path)