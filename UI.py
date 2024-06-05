import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


class LaTeXTableGenerator:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    @staticmethod
    def choose_first_column_style(file_name):
        phrase_to_letter = {
            '32': 'A',
            '31': 'A',
            '34': 'A',
            '92': 'A',
        }
        for phrase, letter in phrase_to_letter.items():
            if phrase in file_name:
                return letter
        return 'Y'

    @staticmethod
    def column_style(file_name):
        last_underscore_index = file_name.rfind('_')
        if last_underscore_index != -1:
            substring_start = last_underscore_index + 1
            substring_end = file_name.rfind('.csv')
            if substring_end != -1:
                return file_name[substring_start:substring_end]
            else:
                return file_name[substring_start:]
        else:
            return ""

    def generate_full_tabular(self):
        for file_name in os.listdir(self.dir_path):
            if file_name.endswith('.csv'):
                csv_file = pd.read_csv(os.path.join(self.dir_path, file_name), delimiter=r'[\t]*;[\t]*',
                                       engine='python')
                column_names = csv_file.columns
                row_values = csv_file.values.tolist()

                first_column_letter = self.choose_first_column_style(file_name)
                column_definitions = []
                header_commands = []
                body_commands = []

                real_column_index = 0
                i = 0

                while i < len(column_names):
                    count = 1
                    if not column_names[i].startswith("Unnamed"):
                        real_column_index += 1
                        column_type = first_column_letter if real_column_index == 1 else (
                            'S' if real_column_index % 2 == 0 else 'Y')

                        j = i + 1
                        while j < len(column_names) and column_names[j].startswith("Unnamed"):
                            count += 1
                            j += 1

                        if count > 1:
                            multicolumn_type = 'S' if real_column_index % 2 == 0 else 'Y'
                            header_commands.append(
                                f"\\multicolumn{{{count}}}{{{'c'}}}{{\\textit{{{column_names[i]}}}}}")
                            column_definitions.extend([multicolumn_type] * count)
                        else:
                            header_commands.append(f"\\textit{{{column_names[i]}}}")
                            column_definitions.append(column_type)

                        i = j - 1
                    i += 1

                for row in row_values:
                    processed_row = []
                    for value in row:
                        if pd.isna(value):
                            processed_row.append('')
                        else:
                            processed_row.append(str(value))
                    body_commands.append(' & '.join(processed_row) + ' \\\\ \\hline')

                tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(
                    column_definitions) + '}'
                tabular_body = "\n".join(body_commands)
                full_table = (f"{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline\n{tabular_body}\n\\end{{"
                              f"tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}")

                latex_file_name = os.path.splitext(file_name)[0] + '.tex'
                latex_file_path = os.path.join(self.dir_path, latex_file_name)
                with open(latex_file_path, 'w') as latex_file:
                    latex_file.write(full_table)

        return '-----------DONE-----------'


class LaTeXTableGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX Table Generator")
        self.directory_path = ""

        self.label = tk.Label(root, text="Select a directory containing CSV files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=10)

        self.process_button = tk.Button(root, text="Generate LaTeX Tables", command=self.process_directory)
        self.process_button.pack(pady=10)
        self.process_button.config(state=tk.DISABLED)

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.process_button.config(state=tk.NORMAL)

    def process_directory(self):
        generator = LaTeXTableGenerator(self.directory_path)
        result = generator.generate_full_tabular()
        messagebox.showinfo("Result", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = LaTeXTableGeneratorUI(root)
    root.mainloop()
