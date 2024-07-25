import os
import pandas as pd


class Processing:

    def __init__(self, dir_path: str, layout_style: str, first_row_italic: bool, **args):

        self.dir_path = dir_path
        self.layout_style = layout_style
        self.first_row_italic = first_row_italic

    def process_file(self, file_name, horizontal_line, format_style, choose_which) -> None:
        # noinspection PyTypeChecker
        csv_file = pd.read_csv(
            os.path.join(self.dir_path, file_name),
            delimiter=r'[\t]*;[\t]*',
            engine='python'
        )
        column_names = csv_file.columns

        from .process_columns import ProcessColumns
        from .process_rows import ProcessRows

        column_definitions, header_commands = ProcessColumns.columns(column_names, self.layout_style, self.first_row_italic)

        if choose_which == 'column':
            row_values = ProcessColumns.format_style(csv_file, format_style).values.tolist()
        elif choose_which == 'row':
            row_values = ProcessRows.format_style(csv_file,format_style).values.tolist()
        else:
            row_values = csv_file.values.tolist()

        body_commands = ProcessRows.rows(row_values)

        if horizontal_line:
            tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(
                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)
            full_table = (f"{tabular_header}\n{' & '.join(header_commands)} \\\\ \n{tabular_body}\n\\end{{"
                          f"tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}")
        else:
            tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(
                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)
            full_table = (f'{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                          f'tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}')

        latex_file_name = os.path.splitext(file_name)[0] + '.tex'
        latex_file_path = os.path.join(self.dir_path, latex_file_name)
        with open(latex_file_path, 'w') as latex_file:
            latex_file.write(full_table)
