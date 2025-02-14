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
            engine='python',
            encoding='utf-8'
        )

        header_title = csv_file.columns[0]
        caption = csv_file.columns[-1]
        main_data = csv_file.drop(columns=[header_title, caption])
        column_names = main_data.columns.str.strip()

        if not (header_title and not header_title.startswith('Unnamed')):
            header_title = ''
        if not (caption and not caption.startswith('Unnamed')):
            caption = ''

        from .process_columns import ProcessColumns
        from .process_rows import ProcessRows
        from .censored import column_censoring
        from .censored import cell_censoring

        column_definitions, header_commands = ProcessColumns.normal_columns(column_names,
                                                                            self.generator.layout_style,
                                                                            self.generator.first_row_italic,
                                                                            self.generator.first_row_bold,
                                                                            self.generator.first_row_90_degree
                                                                            )

        if self.generator.censored:
            if self.generator.censor_mode == 'column':
                data = column_censoring(main_data, self.generator.column_trigger_number, self.generator.trigger_column,
                                        self.generator.affected_columns)
                if self.generator.choose_which == 'column':
                    row_values = ProcessColumns.format_style(data, self.generator.format_style).values.tolist()
                elif self.generator.choose_which == 'row':
                    row_values = ProcessRows.format_style(data, self.generator.format_style).values.tolist()
                else:
                    row_values = data.values.tolist()

            elif self.generator.censor_mode == 'cell':
                data = cell_censoring(main_data, self.generator.cell_trigger_number, self.generator.number_affected_cells)
                if self.generator.choose_which == 'column':
                    row_values = ProcessColumns.format_style(data, self.generator.format_style).values.tolist()
                elif self.generator.choose_which == 'row':
                    row_values = ProcessRows.format_style(data, self.generator.format_style).values.tolist()
                else:
                    row_values = data.values.tolist()

        else:
            if self.generator.choose_which == 'column':
                row_values = ProcessColumns.format_style(main_data, self.generator.format_style).values.tolist()
            elif self.generator.choose_which == 'row':
                row_values = ProcessRows.format_style(main_data, self.generator.format_style).values.tolist()
            else:
                row_values = main_data.values.tolist()

        body_commands = ProcessRows.rows(row_values)

        if self.generator.horizontal_line:
            # tabular_header = '\\input{"setup/styles"}\n \\begin{tabularx}{\\textwidth}{' + ''.join(
            tabular_header = '\\tblfont\n\\begin{tabularx}{\\textwidth}{' + ''.join(

                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)

            if self.generator.remove_table_caption and not self.generator.remove_table_headline:  # remove_caption & ^remove_headline
                full_table = (
                    f"\\begin{{table}}[H] \n\\tblheadline{{{header_title}}}\n{tabular_header}\n{' & '.join(header_commands)} \\\\ \n{tabular_body}\n\\end{{"
                    f"tabularx}}\n \\end{{table}} \n \\normalspacing \n \\vspace{{0.5cm}}")

            elif self.generator.remove_table_headline and not self.generator.remove_table_caption:  # ^remove_caption & remove_headline
                full_table = (
                    f'\\begin{{table}}[H] \n{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                    f'tabularx}}\n \\end{{table}} \n \\tblcaption{{{caption}}}\n \\normalspacing \n \\vspace{{0.5cm}}')

            elif not self.generator.remove_table_headline and not self.generator.remove_table_caption:  # ^ remove_caption & ^remove_headline
                full_table = (
                    f"\\begin{{table}}[H] \n\\tblheadline{{{header_title}}}\n{tabular_header}\n{' & '.join(header_commands)} \\\\ \n{tabular_body}\n\\end{{"
                    f"tabularx}}\n \\end{{table}} \n \\tblcaption{{{caption}}} \n \\normalspacing \n \\vspace{{0.5cm}}")

            else:  # remove_caption & remove_headline
                full_table = (
                    f"\\begin{{table}}[H] \n{tabular_header}\n{' & '.join(header_commands)} \\\\ \n{tabular_body}\n\\end{{"
                    f"tabularx}} \n \\end{{table}}  \n \\normalspacing \n \\vspace{{0.5cm}}")

        else:
            # tabular_header = '\\input{"setup/styles"}\n\\begin{tabularx}{\\textwidth}{' + ''.join(
            tabular_header = '\\tblfont\n\\begin{tabularx}{\\textwidth}{' + ''.join(

                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)

            if self.generator.remove_table_caption and not self.generator.remove_table_headline:  # remove_caption & ^remove_headline
                full_table = (
                    f'\\begin{{table}}[H] \n\\tblheadline{{{header_title}}}\n{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                    f'tabularx}} \n \\end{{table}} \n \\normalspacing \n \\vspace{{0.5cm}}')

            elif self.generator.remove_table_headline and not self.generator.remove_table_caption:  # ^remove_caption & remove_headline
                full_table = (
                    f'\\begin{{table}}[H] \n{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                    f'tabularx}}\n \\end{{table}}\n \\tblcaption{{{caption}}} \n \\normalspacing \n \\vspace{{0.5cm}}')

            elif not self.generator.remove_table_headline and not self.generator.remove_table_caption:  # ^ remove_caption & ^remove_headline
                full_table = (
                    f'\\begin{{table}}[H] \n \\tblheadline{{{header_title}}}\n{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                    f'tabularx}} \n \\end{{table}} \n \\tblcaption{{{caption}}} \n \\normalspacing \n \\vspace{{0.5cm}}')

            else:  # remove_caption & remove_headline
                full_table = (
                    f'\\begin{{table}}[H] \n{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline \n{tabular_body}\n\\end{{'
                    f'tabularx}} \n \\end{{table}} \n \\normalspacing \n \\vspace{{0.5cm}}')

        latex_file_name = os.path.splitext(self.file_name)[0] + '.tex'
        latex_file_path = os.path.join(self.generator.dir_path, latex_file_name)
        with open(latex_file_path, 'w', encoding='utf-8') as latex_file:
            latex_file.write(full_table)
