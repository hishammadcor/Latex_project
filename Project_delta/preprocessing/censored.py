import pandas as pd


def column_censoring(data: pd.DataFrame, trigger_number: str, trigger_column: str, affected_columns: str)-> pd.DataFrame:

    data_columns = data.columns
    trigger_column = int(trigger_column) - 1
    affected_columns = affected_columns.split(',')

    for index, row in data.iterrows():
        try:
            trigger_value = int(row[data_columns[trigger_column]])
            if trigger_value < int(trigger_number):
                for col_index in affected_columns:
                    data.at[index, data_columns[int(col_index)-1]] = 'XXX'
        except (ValueError, TypeError):
            continue

    return data


def cell_censoring(data: pd.DataFrame, trigger_number: str, affected_cells: str) -> pd.DataFrame:

    trigger_number = int(trigger_number)
    affected_cells = int(affected_cells)
    for col in data.columns:
        try:
            i = 0
            while i < len(data):
                if pd.to_numeric(data.at[i, col], errors='coerce') < trigger_number:
                    for j in range(1, affected_cells + 1):
                        if i + j < len(data):
                            data.at[i + j, col] = 'XXX'
                    i += affected_cells
                i += affected_cells

        except (ValueError, TypeError):
            continue

    return data


def row_censoring(data: pd.DataFrame, trigger_number: str, trigger_row: str, affected_rows: str) -> pd.DataFrame:
    trigger_row = int(trigger_row) - 1  # Convert to 0-based index
    affected_rows = affected_rows.split(',')

    # Check each cell in the trigger row
    for col_index in range(len(data.columns)):
        try:
            trigger_value = int(data.iloc[trigger_row, col_index])

            # If trigger value is less than trigger_number, censor this column in affected rows
            if trigger_value < int(trigger_number):
                for row_index in affected_rows:
                    data.iloc[int(row_index) - 1, col_index] = 'XXX'
        except (ValueError, TypeError, IndexError):
            continue

    return data
