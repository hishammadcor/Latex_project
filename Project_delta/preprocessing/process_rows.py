import pandas as pd
from Project_delta.utils.utils import apply_format, multi_row


class ProcessRows:
    @staticmethod
    def rows(row_values, multirow, width) -> list[str]:
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
            return multi_row(body_commands, width)

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
    import pandas as pd

    # Change the file path to your Excel file
    excel_file_path = 'U:/Latex_project/tex/C-2-2_Rechtswissenschaft_ES.xlsx'

    # Read the Excel file (first sheet)
    excel_file = pd.read_excel(excel_file_path, sheet_name=0, engine='openpyxl')

    # Extract the header and caption, assuming first and last columns are header and caption respectively
    header_title = excel_file.columns[0]
    caption = excel_file.columns[-1]

    # Drop the first and last columns
    main_data = excel_file.drop(columns=[header_title, caption])
    print(main_data)
    row_values = ProcessRows.format_style(main_data, '233333')
    print("rowvalues:   ", row_values)

    # Generate the tabular body and print it
    tabular_body = "\n".join(row_values)
    print("tabular:  ", tabular_body)