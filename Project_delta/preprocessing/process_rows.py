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
