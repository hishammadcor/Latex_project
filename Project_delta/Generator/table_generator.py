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
            remove_table_caption: bool,
            remove_table_headline:bool,
            choose_which: str,
            censored: bool,
            censor_mode: str,
            column_trigger_number: str,
            trigger_column,
            affected_columns,
            cell_trigger_number: str,
            number_affected_cells: str,
            style_dir_path,
            column_names: bool,
            multirow: bool,
            width

    ) -> None:

        self.dir_path = dir_path
        self.layout_style = layout_style
        self.format_style = format_style
        self.first_row_italic = first_row_italic
        self.first_row_bold = first_row_bold
        self.first_row_90_degree = first_row_90_degree
        self.horizontal_line = horizontal_line
        self.remove_table_caption = remove_table_caption
        self.remove_table_headline = remove_table_headline
        self.choose_which = choose_which
        self.censored = censored
        self.censor_mode = censor_mode
        self.column_trigger_number = column_trigger_number
        self.trigger_column = trigger_column
        self.affected_columns = affected_columns
        self.cell_trigger_number = cell_trigger_number
        self.number_affected_cells = number_affected_cells
        self.style_dir_path = style_dir_path
        self.column_names = column_names
        self.multirow = multirow
        self.width = width

    @property
    def generate_full_tabular(self):
        try:
            for file_name in os.listdir(self.dir_path):
                if file_name.endswith('.csv'):
                    Project_delta.Processing(file_name, self)

            # Generate the main.tex file in the same directory as the generated LaTeX files
            from Project_delta.preprocessing.preview_tex_files import PreviewTexFiles
            base_directory = self.dir_path
            PreviewTexFiles(base_directory, self.style_dir_path)

            done = '-----------DONE-----------'
            return done
        except Exception as e:
            return f'An error occurred: {e}'
