import csv
import pandas as pd
import numpy as np
from pylatex import Document, Tabular, math 
from pylatex.utils import italic, NoEscape
import string

file = "test.csv"
df = pd.read_csv(file, delimiter=";")
columns = df.columns
array = df.to_numpy()

doc = Document()

# Define the table with explicit column widths and alignments
# Here we use 'l' for left alignment as a placeholder; you will need to adjust this based on your exact needs
# For coloring even columns, you would manually apply background colors to each cell in those columns if PyLaTeX does not support conditional column styling
with doc.create(Tabular('lcccc')) as table:
    # Add the header row with italic formatting
    table.add_row([NoEscape(r'\textit{' + col + r'}') for col in columns], strict=False)
    table.add_hline()
    
    for row in array:
        # Manually apply coloring or other styles to individual cells as needed
        # This loop assumes 'array' is an iterable of iterables, each inner iterable representing a row
        formatted_row = [row[0]]  # First cell unmodified
        for i, cell in enumerate(row[1:], start=1):
            # Example conditional formatting for even columns (by index)
            if i % 2 == 0:  # Assuming even columns need specific styling
                formatted_row.append(NoEscape(r'\textcolor{green}{' + str(cell) + r'}'))
            else:
                formatted_row.append(cell)
        table.add_row(formatted_row, strict=False)
        table.add_hline()

doc.generate_pdf("fixed_report", clean_tex=False)





# TODO: Fully code the styles in Pylatex >> Learn how to do it on little examles and try to mimmic this in the style above.
# TODO: transform all the styels>> BAD APPROACH, try to find good ways to work on the styles without transforming all of them to PyLatex 
# TODO: after making sure of the style >> extract the tex and try it on the whole project																			