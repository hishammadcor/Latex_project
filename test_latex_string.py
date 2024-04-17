import pandas as pd


def choose_first_column_style(file_name):
    # A dictionary mapping certain phrases to letters A - I
    phrase_to_letter = {
        '33': 'A',
        '31': 'A',
        '34': 'A',
        '92': 'A',
        '32': 'B'
        # Add more mappings as necessary
    }
    for phrase, letter in phrase_to_letter.items():
        if phrase in file_name:
            return letter
    return 'I'  # Default to 'A' if no specific phrase is found


def generate_full_tabular_with_names_and_rows(column_names, row_values, file_name):
    """
    Generates a complete LaTeX table code including headers and rows based on the provided column names and row
    values. The function dynamically handles multicolumn scenarios based on the presence of "Unnamed" columns
    following real column names.

    Parameters:
    - column_names (list): A list of strings representing the column names. Columns intended for multicolumn spans
      should be followed by "Unnamed" placeholders.
    - row_values (list): A flattened list of row values corresponding to the table content. The values are expected
      to match the structure defined by `column_names`, with handling for `np.nan` values to leave cells blank.

    Returns:
    - str: A string containing the complete LaTeX table code, ready to be included in a LaTeX document.

    The function iterates over `column_names` to determine the structure of the table, identifying multicolumn spans
    and applying appropriate LaTeX formatting. Real column names are incorporated directly into the table header,
    while row values are formatted and inserted according to the column structure. `np.nan` values in `row_values`
    result in blank cells in the output table.
    Additional Parameters:
    - file_name (str): The name of the CSV file being processed, used to determine the first column letter.
    """

    first_column_letter = choose_first_column_style(file_name)
    column_definitions = []  # Stores LaTeX column specifications
    header_commands = []  # Stores header column names with formatting
    body_commands = []  # Stores the data rows

    real_column_index = 0  # Tracks non-"Unnamed" columns
    i = 0  # General iteration index

    while i < len(column_names):
        count = 1  # Counts "Unnamed" columns for multicolumn span, starting with 1 for the current column
        if not column_names[i].startswith("Unnamed"):
            real_column_index += 1  # Increment for each real (non-"Unnamed") column encountered
            column_type = first_column_letter if real_column_index == 1 else (
                'S' if real_column_index % 2 == 0 else 'Y')

            # Check ahead for consecutive "Unnamed" columns to determine multicolumn span
            j = i + 1
            while j < len(column_names) and column_names[j].startswith("Unnamed"):
                count += 1
                j += 1

            # Formatting for multicolumn if necessary
            if count > 1:
                multicolumn_type = 'S' if real_column_index % 2 == 0 else 'Y'
                header_commands.append(
                    f"\\multicolumn{{{count}}}{{{multicolumn_type}}}{{\\textit{{{column_names[i]}}}}}")
                column_definitions.extend([multicolumn_type] * count)  # Extend column definition for multicolumn span
            else:
                header_commands.append(f"\\textit{{{column_names[i]}}}")
                column_definitions.append(column_type)

            i = j - 1  # Adjust index to skip "Unnamed" columns
        i += 1

    # Process row values to form the table body
    for row in row_values:  # Reshape based on the number of real columns
        processed_row = []
        for value in row:
            if pd.isna(value):  # Leave cell blank for NaN values
                processed_row.append('')
            else:
                processed_row.append(str(value))
        body_commands.append(' & '.join(processed_row) + ' \\\\ \\hline')  # Construct each row command

    # Construct the full LaTeX table
    tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(column_definitions) + '}'
    tabular_body = "\n".join(body_commands)
    full_table = f"{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline\n{tabular_body}\n\\end{{tabularx}} \\normalspacing \\vspace{{0.5cm}}"

    return full_table


# import csv file
CSV_file = pd.read_csv('style32.csv', delimiter=r'[\t]*;[\t]*', engine='python')  # the regex gets only the values
# and delete all the unnecessary spaces
columns = CSV_file.columns
values = CSV_file.values.tolist()  # get all the values into a list
csv_file_name = 'style32.csv'
latex_table = generate_full_tabular_with_names_and_rows(columns, values, csv_file_name)

print(latex_table)

# TODO: Add a function that iterates on the CSV files, transform them into LaTex files.
# TODO: Extract the styles numbers form CSV files.
