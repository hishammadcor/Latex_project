import os
from Project_delta.preprocessing.base_processing import Processing


class LaTeXTableGenerator:
    def __init__(

            self, dir_path: str,
            layout_style: str,
            format_style: str,
            first_row_italic: bool,
            horizontal_line: bool,
            choose_which: str,
            trigger_column,
            affected_columns
                    ) -> None:

        self.dir_path = dir_path
        self.layout_style = layout_style
        self.format_style = format_style
        self.first_row_italic = first_row_italic
        self.horizontal_line = horizontal_line
        self.choose_which = choose_which
        self.trigger_column = trigger_column
        self.affected_column = affected_columns
        self.processor = Processing(self.dir_path, self.layout_style, self.first_row_italic)

    @property
    def generate_full_tabular(self):
        try:
            for file_name in os.listdir(self.dir_path):
                if file_name.endswith('.csv'):
                    self.processor.process_file(file_name, self.horizontal_line)
            return '-----------DONE-----------'
        except Exception as e:
            return f'An error occurred: {e}'
