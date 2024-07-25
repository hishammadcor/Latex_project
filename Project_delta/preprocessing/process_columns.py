from typing import Any


class ProcessColumns:

    @staticmethod
    def columns(column_names, column_styles, first_row_italic) -> tuple[list[Any], list[str]]:
        column_definitions = list(column_styles)[:len(column_names)]
        header_commands = []
        real_column_index = 0
        i = 0

        while len(column_names) > i:
            count = 1
            if not column_names[i].startswith("Unnamed"):
                real_column_index += 1

                j = i + 1
                while j < len(column_names) and column_names[j].startswith("Unnamed"):
                    count += 1
                    j += 1

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

                else:
                    if count > 1:
                        if real_column_index % 2 == 0:
                            header_commands.append(
                                f"\\multicolumn{{{count}}}{{{'c'}}}{{\\cellcolor{{{'green40'}}}{{{column_names[i]}}}}}")
                        else:
                            header_commands.append(f"\\multicolumn{{{count}}}{{{'c'}}}{{{{{column_names[i]}}}}}")
                    else:
                        header_commands.append(f"{{{column_names[i]}}}")

                i = j - 1
            else:
                if real_column_index == 0:
                    header_commands.append(' ')
            i += 1

        # Ensure column_definitions matches the number of columns
        if len(column_definitions) < len(column_names):
            column_definitions.extend(['X'] * (len(column_names) - len(column_definitions)))

        return column_definitions, header_commands

    @staticmethod
    def format_style(data, format_string):
        def apply_format(value, style):
            try:
                if style == '1':
                    return str(value)
                elif style == '2':
                    return f"{int(float(value))}"
                elif style == '3':
                    return f"{int(float(value))}%"
                elif style == '4':
                    return f"{float(value):.1f}"
                elif style == '5':
                    return f"{float(value):.2f}"
                else:
                    return value
            except ValueError:
                return value

        for col_idx, style in enumerate(format_string):
            if col_idx < len(data.columns):
                data.iloc[:, col_idx] = data.iloc[:, col_idx].apply(lambda x: apply_format(x, style))

        return data
