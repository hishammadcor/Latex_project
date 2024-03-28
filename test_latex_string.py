import pandas as pd

# import csv file
CSV_file = pd.read_csv('style92.csv', delimiter=r'[\t]*;[\t]*', engine='python')  # the regex gets only the values
# and delete all the unnecessary spaces
columns = CSV_file.columns
values = CSV_file.values.tolist()  # get all the values into a list


def generate_full_tabular_with_names_and_rows(column_names, row_values):
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
    """

    column_definitions = []  # Stores LaTeX column specifications
    header_commands = []  # Stores header column names with formatting
    body_commands = []  # Stores the data rows

    real_column_index = 0  # Tracks non-"Unnamed" columns
    i = 0  # General iteration index

    while i < len(column_names):
        count = 1  # Counts "Unnamed" columns for multicolumn span, starting with 1 for the current column
        if not column_names[i].startswith("Unnamed"):
            real_column_index += 1  # Increment for each real (non-"Unnamed") column encountered
            column_type = 'l' if real_column_index == 1 else ('s' if real_column_index % 2 == 0 else 'c')

            # Check ahead for consecutive "Unnamed" columns to determine multicolumn span
            j = i + 1
            while j < len(column_names) and column_names[j].startswith("Unnamed"):
                count += 1
                j += 1

            # Formatting for multicolumn if necessary
            if count > 1:
                multicolumn_type = 's' if real_column_index % 2 == 0 else 'c'
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
    tabular_header = '\\begin{tabular}{' + ''.join(column_definitions) + '}'
    tabular_body = "\n".join(body_commands)
    full_table = f"{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline\n{tabular_body}\n\\end{{tabular}}"

    return full_table


latex_table = generate_full_tabular_with_names_and_rows(columns, values)

print(latex_table)

# TODO: add a funtion that iterates on the CSV files, transfrom them into LaTex files.
