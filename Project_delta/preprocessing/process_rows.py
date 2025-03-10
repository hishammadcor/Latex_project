import pandas as pd
from Project_delta.utils.utils import apply_format, multi_row


class ProcessRows:
    @staticmethod
    def rows(row_values, multirow) -> list[str]:
        body_commands = []
        for i, row in enumerate(row_values):
            processed_row = []
            for value in row:
                if pd.isna(value):
                    processed_row.append('-')
                else:
                    processed_row.append(str(value))
            if i == len(row_values) - 1:
                body_commands.append(' & '.join(processed_row) + " \\\\ ")
            else:
                body_commands.append(' & '.join(processed_row) + ' \\\\ \\hline')

        if multirow is True:
            return multi_row(body_commands)

        return body_commands

    @staticmethod
    def format_style(data, format_string):
        def format_row(row, style):
            return pd.Series([apply_format(value, style) for value in row], index=row.index)

        if all(no.isdigit() for no in format_string):
            formatted_data = data.apply(lambda row: format_row(row, format_string[row.name % len(format_string)]),
                                        axis=1)

            return formatted_data
        raise ValueError(
            "The format style is either contains non-numeric characters or empty. Please make sure that you enter only numeric values.")


if __name__ == '__main__':
    from Project_delta.preprocessing.process_columns import ProcessColumns

    csv_file = pd.read_csv(
        'U:/Latex_project/tex/A-3-1_Aktuelle Personalstruktur_Betriebswirtschaftslehre.csv',
        delimiter=r'[\t]*;[\t]*',
        engine='python',
        encoding='utf-8'
    )

    header_title = csv_file.columns[0]
    caption = csv_file.columns[-1]
    main_data = csv_file.drop(columns=[header_title, caption])
    rows = ProcessColumns.format_style(main_data, '113112').values.tolist()
    print("rows", rows)
    row_values = ProcessRows.rows(rows, multirow=True)
    print("rowvalues:   ", row_values)
    tabular_body = "\n".join(row_values)
    print("tbaular:  ", tabular_body)
