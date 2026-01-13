import os
import re


def natural_key(s: str):
    """
    Key for natural/human sorting:
    'table2a.tex' < 'table10.tex' etc.
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


class PreviewTexFiles:
    def __init__(self, base_directory, styles_absolute_path, output_file_name='main.tex'):
        self.base_directory = base_directory
        self.output_file_name = output_file_name
        self.styles_absolute_path = styles_absolute_path.replace("\\", "/")
        self.main_tex_content = f"""\input{{{self.styles_absolute_path}/setup/pageSetup}}                                                             
\input{{{self.styles_absolute_path}/setup/customCommands}}                                                  
\input{{{self.styles_absolute_path}/setup/styles}} 

\\begin{{document}}
    \section*{{Vorschau der Tabellen}}
"""
        self.generate_main_tex()

    @staticmethod
    def _has_matching_source_file(dir_path: str, tex_filename: str) -> bool:
        """Only include generated table .tex files (those with a matching csv/xlsx/... source)."""
        base, _ = os.path.splitext(tex_filename)
        source_exts = ('.csv', '.xlsx', '.xls', '.xlsm', '.tsv')
        return any(os.path.exists(os.path.join(dir_path, base + ext)) for ext in source_exts)

    def collect_tex_files(self, current_dir):
        tex_files = []
        for root, dirs, files in os.walk(current_dir):
            # Don’t scan internal folders
            dirs[:] = [d for d in dirs if d not in {"setup", "preview"}]

            for file in files:
                if not file.endswith('.tex'):
                    continue
                if file == self.output_file_name:
                    continue

                # Only include converted tables, not arbitrary .tex (like a section-file)
                if not self._has_matching_source_file(root, file):
                    continue

                full_path = os.path.relpath(os.path.join(root, file), self.base_directory)
                tex_files.append(os.path.join('..', full_path).replace(os.sep, '/'))
        return tex_files

    def generate_main_tex(self):
        tex_files = self.collect_tex_files(self.base_directory)
        # Sort tables
        tex_files = sorted(tex_files, key=natural_key)

        for tex_file in tex_files:
            self.main_tex_content += f"\\input{{{tex_file}}}\n"

        self.main_tex_content += r"\end{document}"

        preview_dir = os.path.join(self.base_directory, 'preview')
        if not os.path.exists(preview_dir):
            os.mkdir(preview_dir)

        output_path = os.path.join(preview_dir, self.output_file_name)
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(self.main_tex_content)


if __name__ == "__main__":
    # Example usage
    base_dir = r"C:\Users\s2hialii\Desktop\asb"  # Current directory
    preview_generator = PreviewTexFiles(base_dir)
    print("Preview file generated successfully!")
