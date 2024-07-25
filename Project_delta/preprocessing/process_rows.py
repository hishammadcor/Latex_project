import pandas as pd


class ProcessRows:

    @staticmethod
    def rows(row_values) -> list[str]:
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

    @staticmethod
    def format_style(data, format_string):
        def apply_format(value, style):
            try:
                if style == '1':
                    return str(value)
                elif style == '2':
                    return f"{int(float(value))}"
                elif style == '3':
                    return f"{int(float(value))}%"
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

        formatted_data = data.apply(lambda row: format_row(row, format_string[row.name % len(format_string)]), axis=1)

        return formatted_data
