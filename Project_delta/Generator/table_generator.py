import os
from Project_delta.preprocessing.base_processing import Processing


class LaTeXTableGenerator:
    def __init__(self, dir_path: str, column_styles: str, first_row_italic: bool, horizontal_line: bool) -> None:
        self.dir_path = dir_path
        self.column_styles = column_styles
        self.first_row_italic = first_row_italic
        self.horizontal_line = horizontal_line
        self.processor = Processing(self.dir_path, self.column_styles, self.first_row_italic)

    @property
    def generate_full_tabular(self):
        try:
            for file_name in os.listdir(self.dir_path):
                if file_name.endswith('.csv'):
                    self.processor.process_file(file_name, self.horizontal_line)
            return '-----------DONE-----------'
        except Exception as e:
            return f'An error occurred: {e}'
