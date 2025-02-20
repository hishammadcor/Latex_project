import pandas as pd
import locale


class ProcessRows:

    try:
        locale.setlocale(locale.LC_ALL, 'German_Germany.1252') # this is locale windows settings
        # locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # I think this is linux/macOS locale settings # Adjust based on your system
    except locale.Error:
        print("Locale not supported or settings are not correctly adjusted, return to class ProcessRows and ProcessColumns.")

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
        def apply_format(value, style):
            try:
                if style == '1':
                    value = str(value)
                    float_value = float(value)
                    if pd.isna(value) or pd.isna(float_value):
                        return ''
                    return str(value)

                value = str(value).replace('%', '').replace(',', '.')
                float_value = float(value)
                if pd.isna(value) or pd.isna(float_value):
                    return '-'
                elif style == '2':
                    return locale.format_string("%d",  round(float_value), grouping=True)
                elif style == '3':
                    return locale.format_string("%d",  round(float_value), grouping=True) + '\\%'
                elif style == '4':
                    return locale.format_string("%.1f",  round(float_value, 1), grouping=True)
                elif style == '5':
                    return locale.format_string("%.2f",  round(float_value, 2), grouping=True)
                elif style == '6':
                    return locale.format_string("%.2f",  round(float_value, 2), grouping=True) + '\\%'
                else:
                    return str(value)
            except (ValueError, TypeError, OverflowError):
                return str(value)

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
        "tex/C-6-2_tbl10_Studienverlauf und -erfolg_GES_MA_1F_phil.csv",
        delimiter=r'[\t]*;[\t]*',
        engine='python',
        encoding='utf-8'
    )

    row_values = ProcessRows.format_style(csv_file, "33333").values.tolist()
    print(row_values)