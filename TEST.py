import csv
from pylatex import Document, Tabular, NoEscape
from pylatex.utils import italic
def create_custom_latex_table(csv_file_path, latex_file_path):
    # Start a new document
    doc = Document()

    # Custom LaTeX table setup using your style
    # Define your custom column types and table settings here.
    # Note: Ensure your LaTeX document preamble includes necessary packages.
    custom_table_preamble = """
\\usepackage{tabularray}
\\usepackage[ngerman]{babel}
\\usepackage[T1]{fontenc}
\\usepackage{fontspec}
\\usepackage[official]{eurosym}
\\usepackage{colortbl}
\\usepackage{xcolor}
\\usepackage{array}
\\definecolor{green40}{RGB}{ 196, 229, 218}
"""

    # Include the custom preamble in the document
    doc.preamble.append(NoEscape(custom_table_preamble))

    # Prepare the table environment with your specifications
    table_environment = """
\\begin{{tblr}}{{
      column type = {{
                      @{{}}
                      Q[l, wd=12.0cm]
                      Q[c, 1, bg=green40]
                      Q[c, 1]
                      Q[c, 1, bg=green40]
                      Q[c, 1]
                      @{{}}
                    }},
      highlight_italics first row,
      every nth row = {{1}}{{before row = \\hline}},
    }}
"""

    # Read the CSV data and append rows to the table environment
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        table_content = ""
        for row in reader:
            # Join the row items with & and end with \\
            table_content += " & ".join(row) + " \\\\\n"
        # Finalize the table environment
        table_environment = table_environment.format(table_content)

    # Add the complete table environment to the document
    doc.append(NoEscape(table_environment))

    # Generate the LaTeX document
    doc.generate_pdf(latex_file_path)

# Example usage
csv_file_path = 'test.csv'
latex_file_path = 'test'
create_custom_latex_table(csv_file_path, latex_file_path)


# TODO: Fully code the styles in Pylatex >> Learn how to do it on little examles and try to mimmic this in the style above.
# TODO: transform all the styels>> BAD APPROACH, try to find good ways to work on the styles without transforming all of them to PyLatex 
# TODO: after making sure of the style >> extract the tex and try it on the whole project																			