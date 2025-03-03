import pandas as pd
from ..utils.utils import (apply_format)


class ProcessRows:
    @staticmethod
    def rows(row_values) -> list[str]:
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


if __name__ == "__main__":
    csv_file = pd.read_csv(
        "U:/Latex_project/tex/A-4-5_tbl11_sächliche Ausstattung VWL.csv",
        delimiter=r'[\t]*;[\t]*',
        engine='python',
        encoding='utf-8'
    )

    header_title = csv_file.columns[0]
    caption = csv_file.columns[-1]
    main_data = csv_file.drop(columns=[header_title, caption])
    header_as_row = pd.DataFrame([main_data.columns.tolist()], columns=main_data.columns)
    main_data = pd.concat([header_as_row, main_data], ignore_index=True)
    main_data.columns = range(main_data.shape[1])
    print(main_data)