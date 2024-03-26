import re
import pandas as pd

# ToDo: add more styles

# import csv file
style92_csv = pd.read_csv('style92.csv', delimiter=r'[\t]*;[\t]*', engine='python')  # the regex gets only the values
# and delete all the unnecessary spaces
columns = style92_csv.columns
values = style92_csv.values.tolist()  # get all the values into a list
rows = [item for sublist in values for item in sublist]  # each row is only in one list, so combine all the
# lists in only one list

# Define the style
style92 = r"""
                \begin{tabular}{l s c c s s s}
                    \textit{ # }   &    \textit{ # }  &   \multicolumn{2}{c}{\textit{ # }}  &
                    \multicolumn{3}{c}{\cellcolor{green40}\textit{ # }} \\\hline

                    &   & $  & $  & $  &  $ & $ \\ \hline
                    $ & $  &  $ & $  &  $ & $  & $ \\ \hline
                    $ &  $ & $  &  $ &  $ & $  & $

                \end{tabular}
         """


def replace_placeholders(template, row_values, column_names):
    """
    :param template: the style wanted
    :param row_values: contains only the rows
    :param column_names: only the column names
    :return: a latex file contains the formatted style
    """

    for name in column_names:
        if not name.startswith("Unnamed"): # in multicolumn CSV files, some columns are blank, so this makes sure
            # that the unnamed columns are not included
            template = re.sub(r'#', name, template, count=1) # replaces the # with the column name in the style

    for value in row_values:
        if not pd.isna(value): # in multicolumn CSV files, some cells are null,, so this make sure that those null
            # are omitted
            template = re.sub(r'\$', str(value), template, count=1)

    # ToDO: return a latex file
    return template


style92_table = replace_placeholders(style92, rows, columns)

