from typing import Any
from Project_delta.utils.utils import apply_format


class ProcessColumns:

    @staticmethod
    def normal_columns(column_names, columns_number, column_styles, first_row_italic, first_row_bold, first_row_90_degree) -> tuple[list[Any], list[str]]:
        if all(char.isalpha() for char in column_styles) and column_styles:

            column_definitions = list(column_styles)[:columns_number]
            header_commands = []
            real_column_index = 1
            i = 0

            while len(column_names) > i:
                count = 1
                if not column_names[i].startswith("Unnamed"):
                    real_column_index += 1

                    j = i + 1
                    while j < len(column_names) and column_names[j].startswith("Unnamed"):
                        count += 1
                        j += 1

                    if first_row_90_degree:
                        if first_row_italic:
                            if count > 1:
                                if real_column_index % 2 == 0:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\rotatebox{{{'90'}}}{{\\textit{{{column_names[i]}}}}}}}")
                                else:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\rotatebox{{{'90'}}}{{\\textit{{{column_names[i]}}}}}}}")
                            else:
                                header_commands.append(f"\\multicolumn{{{1}}}{{{'c'}}}{{\\rotatebox{{{'90'}}}{{\\textit{{{column_names[i]}}}}}}}")

                        elif first_row_bold:
                            if count > 1:
                                if real_column_index % 2 == 0:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\rotatebox{{{'90'}}}{{\\textbf{{{column_names[i]}}}}}}}")
                                else:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\rotatebox{{{'90'}}}{{\\textbf{{{column_names[i]}}}}}}}")
                            else:
                                if i % 2 == 0:  # Check if the index is even
                                    header_commands.append(f"\\multicolumn{{{1}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\rotatebox{{{'90'}}}{{\\textbf{{{column_names[i]}}}}}}}")
                                else:
                                    header_commands.append(f"\\multicolumn{{{1}}}{{{'c'}}}{{\\rotatebox{{{'90'}}}{{\\textbf{{{column_names[i]}}}}}}}")

                        else:
                            if count > 1:
                                if real_column_index % 2 == 0:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\rotatebox{{{'90'}}}{{{column_names[i]}}}}}")
                                else:
                                    header_commands.append(f"\\multicolumn{{{count}}}{{{'c'}}}{{\\rotatebox{{{'90'}}}{{{column_names[i]}}}}}")
                            else:
                                header_commands.append(f"\\rotatebox{{{'90'}}}{{{column_names[i]}}}")

                    elif not first_row_90_degree:
                        if first_row_italic:
                            if count > 1:
                                if real_column_index % 2 == 0:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\textit{{{column_names[i]}}}}}")
                                else:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\textit{{{column_names[i]}}}}}")
                            else:
                                header_commands.append(f"\\textit{{{column_names[i]}}}")

                        elif first_row_bold:
                            if count > 1:
                                if real_column_index % 2 == 0:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}\\textbf{{{column_names[i]}}}}}")
                                else:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\textbf{{{column_names[i]}}}}}")
                            else:
                                header_commands.append(f"\\textbf{{{column_names[i]}}}")

                        else:
                            if count > 1:
                                if real_column_index % 2 == 0:
                                    header_commands.append(
                                        f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}{column_names[i]}}}")
                                else:
                                    header_commands.append(f"\\multicolumn{{{count}}}{{{'c'}}}{{{column_names[i]}}}")
                            else:
                                header_commands.append(f"{column_names[i]}")

                    i = j - 1
                else:
                    if real_column_index == 1:
                        header_commands.append(' ')
                i += 1

            # Ensure column_definitions matches the number of columns
            if len(column_definitions) < columns_number:
                column_definitions.extend(['X'] * (columns_number - len(column_definitions)))

            return column_definitions, header_commands
        raise ValueError(
            'Layout style is either contains non-alphabet characters or empty. You should choose between (A,a,B,b,C,c,F,f,G,g)')

    @staticmethod
    def format_style(data, format_string):
        if all(no.isdigit() for no in format_string) and format_string:
            for col_idx, style in enumerate(format_string):
                if col_idx < len(data.columns):
                    data.iloc[:, col_idx] = data.iloc[:, col_idx].apply(lambda x: apply_format(x, style))

            return data

        raise ValueError(
            "The format style is either contains non-numeric characters or empty. Please make sure that you enter only numeric values.")
