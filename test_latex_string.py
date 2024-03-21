import re
import pandas as pd


# style92 = r"""
#                 \begin{tabular}{l s c c s s s}
#                     \textit{ }   &    \textit{ }  &   \multicolumn{2}{c}{\textit{ }}  &
#                     \multicolumn{3}{c}{\cellcolor{green40}\textit{ }} \\\hline
#
#                     &   &   &   &   &   &  \\ \hline
#                     &   &   &   &   &   &   \\ \hline
#                     &   &   &   &   &   &
#
#                 \end{tabular}
#            """

style92 = r"""
\begin{tabular}{l s c c s s s}
    \textit{ }   &    \textit{ }  &   \multicolumn{2}{c}{\textit{ }}  &
    \multicolumn{3}{c}{\cellcolor{green40}\textit{ }} \\\hline
    
    %s
    
\end{tabular}
"""
path = 'style92.csv'

df = pd.read_csv(path, delimiter=";")


table_content = ""


for index, row in df.iterrows():

    table_content += ' & '.join(map(str, row)) + ' \\\\\n'

styled_table = re.sub(r'(?<=\\\\hline\n\n)(.*?)(?=\\\\hline)', table_content.strip(), style92, flags=re.DOTALL)

print(styled_table)


