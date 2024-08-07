import os
import Project_delta


class LaTeXTableGenerator:
    def __init__(

            self, dir_path: str,
            layout_style: str,
            format_style: str,
            first_row_italic: bool,
            first_row_bold: bool,
            first_row_90_degree: bool,
            horizontal_line: bool,
            choose_which: str,
            censored: bool,
            trigger_column,
            affected_columns
    ) -> None:

        self.dir_path = dir_path
        self.layout_style = layout_style
        self.format_style = format_style
        self.first_row_italic = first_row_italic
        self.first_row_bold = first_row_bold
        self.first_row_90_degree = first_row_90_degree
        self.horizontal_line = horizontal_line
        self.choose_which = choose_which
        self.censored = censored
        self.trigger_column = trigger_column
        self.affected_columns = affected_columns

    @property
    def generate_full_tabular(self):
        try:
            for file_name in os.listdir(self.dir_path):
                if file_name.endswith('.csv'):
                    Project_delta.Processing(file_name,self)
            done = '-----------DONE-----------'
            return done
        except Exception as e:
            return f'An error occurred: {e}'
