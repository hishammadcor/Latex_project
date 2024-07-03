import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


class LaTeXTableGenerator:
    def __init__(self, dir_path, column_styles, first_row_italic):
        self.dir_path = dir_path
        self.column_styles = column_styles
        self.first_row_italic = first_row_italic

    def generate_full_tabular(self):
        for file_name in os.listdir(self.dir_path):
            if file_name.endswith('.csv'):
                self.process_file(file_name)

        return '-----------DONE-----------'

    def process_file(self, file_name):
        csv_file = pd.read_csv(os.path.join(self.dir_path, file_name), delimiter=r'[\t]*;[\t]*', engine='python')
        column_names = csv_file.columns
        row_values = csv_file.values.tolist()

        column_definitions, header_commands = self.process_columns(column_names, self.column_styles, self.first_row_italic)

        body_commands = self.process_rows(row_values)

        tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(column_definitions) + '}'
        tabular_body = "\n".join(body_commands)
        full_table = (f"{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline\n{tabular_body}\n\\end{{"
                      f"tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}")

        latex_file_name = os.path.splitext(file_name)[0] + '.tex'
        latex_file_path = os.path.join(self.dir_path, latex_file_name)
        with open(latex_file_path, 'w') as latex_file:
            latex_file.write(full_table)

    @staticmethod
    def process_columns(column_names, column_styles, first_row_italic):
        column_definitions = list(column_styles)[:len(column_names)]
        header_commands = []
        real_column_index = 0
        i = 0

        while i < len(column_names):
            count = 1
            if not column_names[i].startswith("Unnamed"):
                real_column_index += 1

                j = i + 1
                while j < len(column_names) and column_names[j].startswith("Unnamed"):
                    count += 1
                    j += 1
                if first_row_italic:

                    if count > 1:
                        if real_column_index % 2 == 0:
                            header_commands.append(
                                f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\textit{{{column_names[i]}}}}}")
                        else:
                            header_commands.append(f"\\multicolumn{{{count}}}{{{'c'}}}{{\\textit{{{column_names[i]}}}}}")
                    else:
                        header_commands.append(f"\\textit{{{column_names[i]}}}")

                else:
                    if count > 1:
                        if real_column_index % 2 == 0:
                            header_commands.append(
                                f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}{{column_names[i]}}}}")
                        else:
                            header_commands.append(f"\\multicolumn{{{count}}}{{{'c'}}}{{{{column_names[i]}}}}")
                    else:
                        header_commands.append(f"{{column_names[i]}}")

                i = j - 1
            else:
                if real_column_index == 0:
                    header_commands.append(' ')
            i += 1

        # Ensure column_definitions matches the number of columns
        if len(column_definitions) < len(column_names):
            column_definitions.extend(['X'] * (len(column_names) - len(column_definitions)))

        return column_definitions, header_commands

    @staticmethod
    def process_rows(row_values):
        body_commands = []
        for row in row_values:
            processed_row = []
            for value in row:
                if pd.isna(value):
                    processed_row.append('')
                else:
                    processed_row.append(str(value))
            body_commands.append(' & '.join(processed_row) + ' \\\\ \\hline')

        return body_commands


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

        self.first_row_italic_var = tk.BooleanVar(value=True)
        self.first_row_italic_check = tk.Checkbutton(root_window,  text="First Row Italic", variable=self.first_row_italic_var)
        self.first_row_italic_check.pack(pady=5)

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
        generator = LaTeXTableGenerator(self.directory_path, column_styles, first_row_italic)
        result = generator.generate_full_tabular()
        messagebox.showinfo("Result", result)


if __name__ == "__main__":
    root_window = tk.Tk()
    app = LaTeXTableGeneratorUI(root_window)
    root_window.mainloop()
