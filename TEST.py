import csv
from pylatex import Document, NoEscape

def create_custom_latex_table(csv_file_path, latex_file_path):
    # Start a new document
    doc = Document()

    # Custom LaTeX table setup using your style
    # Define your custom column types and table settings here.
    # Note: Ensure your LaTeX document preamble includes necessary packages.
    custom_table_preamble = """
\\usepackage{tabularray}
\\UseTblrLibrary{booktabs, siunitx}
\\NewColumnType{Q}[1]{X[#1]}
\\definecolor{green40}{RGB}{0,255,0}
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
    doc.generate_tex(latex_file_path)

# Example usage
csv_file_path = 'test.csv'
latex_file_path = 'test'
create_custom_latex_table(csv_file_path, latex_file_path)
