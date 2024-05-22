import pandas as pd
import os


def choose_first_column_style(file_name):
    # A dictionary mapping certain phrases to letters A - I
    phrase_to_letter = {
        '32': 'A',
        '31': 'A',
        '34': 'A',
        '92': 'A',
        '32': 'B'
        # Add more mappings as necessary
    }
    for phrase, letter in phrase_to_letter.items():
        if phrase in file_name:
            return letter
    return 'Y'  # Default to 'Y' if no specific phrase is found. 'Y' is the default column


def column_style(file_name):
    """
    Extracts a column style from a csv file name.
    The substring extracted is between the last underscore and '.csv'

    :param file_name: The complete file name as a string
    :return: The extracted substring
    """
    # Find the index of the last underscore
    last_underscore_index = file_name.rfind('_')

    # Check if underscore is found and proceed
    if last_underscore_index != -1:
        # Slice from after the underscore up to '.csv'
        substring_start = last_underscore_index + 1
        substring_end = file_name.rfind('.csv')

        # Extract the substring
        if substring_end != -1:
            return file_name[substring_start:substring_end]
        else:
            return file_name[substring_start:]  # Return the end part if '.csv' is not found
    else:
        return ""  # Return empty if no underscore is found


def generate_full_tabular(dir_path):
    """
    Generates a complete LaTeX table code including headers and rows based on the provided column names and row
    values. The function dynamically handles multicolumn scenarios based on the presence of "Unnamed" columns
    following real column names.

    Parameters:
     - directory path (str): the path of the directory that have all the CSV names

    Returns:
    - .tex file: A file containing the complete LaTeX table code, ready to be included in a LaTeX document.

    The function iterates over csv file in a given directory. Iterates on `column_names` to determine the structure
    of the table, identifying multicolumn spans and applying appropriate LaTeX formatting. Real column names are
    incorporated directly into the table header, while row values are formatted and inserted according to the column
    structure given in the CSV file name. `np.nan` values in `row_values` result in blank cells in the output table.
    Additional Parameters:
    """

    # import csv files
    for file_name in os.listdir(dir_path):
        # Check if the file is a CSV file
        if file_name.endswith('.csv'):
            # Read CSV files
            csv_file = pd.read_csv(file_name, delimiter=r'[\t]*;[\t]*', engine='python')  # the regex gets only the
            # values and delete all the unnecessary spaces
            column_names = csv_file.columns
            row_values = csv_file.values.tolist()

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
                            f"\\multicolumn{{{count}}}{{{'c'}}}{{\\textit{{{column_names[i]}}}}}")
                        # TODO: \cellcolor{green40} add the cell color to the multi column when the column type is S
                        column_definitions.extend([multicolumn_type] * count)  # Extend column definition for
                        # multicolumn
                        # span
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
            tabular_header = '\\input{setup/styles}\n\\begin{tabularx}{\\textwidth}{' + ''.join(
                column_definitions) + '}'
            tabular_body = "\n".join(body_commands)
            full_table = (f"{tabular_header}\n{' & '.join(header_commands)} \\\\ \\hline\n{tabular_body}\n\\end{{"
                          f"tabularx}} \n \\normalspacing \n \\vspace{{0.5cm}}")

            # Save the table to a .tex file
            latex_file_name = os.path.splitext(file_name)[0] + '.tex'
            latex_file_path = os.path.join(dir_path, latex_file_name)
            with open(latex_file_path, 'w') as latex_file:
                latex_file.write(full_table)

    return '-----------DONE-----------'


directory_path = "C:/Users/s2hialii/Desktop/Latex_project"
generate_full_tabular(directory_path)
