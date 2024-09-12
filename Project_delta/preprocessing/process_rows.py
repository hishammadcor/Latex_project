import pandas as pd


class ProcessRows:

    @staticmethod
    def rows(row_values) -> list[str]:
        body_commands = []
        for i, row in enumerate(row_values):
            processed_row = []
            for value in row:
                if pd.isna(value):
                    processed_row.append('')
                else:
                    processed_row.append(str(value))
            if i == len(row_values) - 1:
                body_commands.append(' & '.join(processed_row) + " \\\\ ")
            else:
                body_commands.append(' & '.join(processed_row) + ' \\\\ \\hline')

        return body_commands

    @staticmethod
    def format_style(data, format_string):
        def apply_format(value, style):
            try:
                if style == '1':
                    return str(value)
                elif style == '2':
                    return f"{int(float(value))}"
                elif style == '3':
                    return f"{int(float(value))}\\%"
                elif style == '4':
                    return f"{float(value):.1f}"
                elif style == '5':
                    return f"{float(value):.2f}"
                else:
                    return value
            except ValueError:
                return value

        def format_row(row, style):
            return pd.Series([apply_format(value, style) for value in row], index=row.index)
        if all(no.isdigit() for no in format_string):
            formatted_data = data.apply(lambda row: format_row(row, format_string[row.name % len(format_string)]), axis=1)

            return formatted_data
        raise ValueError(
            "The format style is either contains non-numeric characters or empty. Please make sure that you enter only numeric values.")
