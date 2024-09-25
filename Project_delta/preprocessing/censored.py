import pandas as pd


def censored_numbers(file, trigger_number: str, trigger_column: str, affected_columns: str):
    data = file
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


if __name__ == '__main__':
    csv_file = pd.read_csv(
        "C:/Users/s2hialii/Desktop/Latex_project/censor_test.csv",
        delimiter=r'[\t]*;[\t]*',
        engine='python'
    )
    trigger = '2'
    affected = "10,11"
    modified_data = censored_numbers(csv_file, trigger, affected)

