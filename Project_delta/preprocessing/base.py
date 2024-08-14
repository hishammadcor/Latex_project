import os
import pandas as pd


class Processing:
    def __init__(self, file_name, generator):
        self.file_name = file_name
        self.generator = generator
        self.process_file()

    def process_file(self) -> None:

        # noinspection PyTypeChecker
        csv_file = pd.read_csv(
            os.path.join(self.generator.dir_path, self.file_name),
            delimiter=r'[\t]*;[\t]*',
            engine='python'
        )

        header_title = csv_file.columns[0]
        main_data = csv_file.drop(columns=[header_title])
        column_names = main_data.columns

        from .process_columns import ProcessColumns
        from .process_rows import ProcessRows
        from .censored import censored_numbers

        column_definitions, header_commands = ProcessColumns.normal_columns(column_names,
                                                                            self.generator.layout_style,
                                                                            self.generator.first_row_italic,
                                                                            self.generator.first_row_bold,
                                                                            self.generator.first_row_90_degree
                                                                            )

        if self.generator.censored:
            data = censored_numbers(csv_file, self.generator.trigger_column, self.generator.affected_columns)

            if self.generator.choose_which == 'column':
                row_values = ProcessColumns.format_style(data, self.generator.format_style).values.tolist()
            elif self.generator.choose_which == 'row':
                row_values = ProcessRows.format_style(data, self.generator.format_style).values.tolist()
            else:
                row_values = data.values.tolist()

        else:
            if self.generator.choose_which == 'column':
                row_values = ProcessColumns.format_style(csv_file, self.generator.format_style).values.tolist()
            elif self.generator.choose_which == 'row':
                row_values = ProcessRows.format_style(csv_file, self.generator.format_style).values.tolist()
            else:
                row_values = csv_file.values.tolist()

        body_commands = ProcessRows.rows(row_values)

        if self.generator.horizontal_line:
            tabular_header = '\\input{setup/styles}\n \\begin{tabularx}{\\textwidth}{' + ''.join(
                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)
            full_table = (f"\\tblheadline{{{header_title}}}\n{tabular_header}\n{' & '.join(header_commands)} \\\\ \n{tabular_body}\n\\end{{"
                          f"tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}")
        else:
            tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(
                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)
            full_table = (
                f'\\tblheadline{{{header_title}}}\n{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                f'tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}')

        latex_file_name = os.path.splitext(self.file_name)[0] + '.tex'
        latex_file_path = os.path.join(self.generator.dir_path, latex_file_name)
        with open(latex_file_path, 'w') as latex_file:
            latex_file.write(full_table)
