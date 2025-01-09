import os


class PreviewTexFiles:
    def __init__(self, base_directory, output_file_name='main.tex'):
        self.base_directory = base_directory
        self.output_file_name = output_file_name
        self.main_tex_content = r"""\input{../setup/pageSetup}                                                            
\input{../setup/customCommands}                                                  
\input{../setup/styles}

\begin{document}
    \section*{Vorschau der Tabellen}

"""
        self.generate_main_tex()

    def collect_tex_files(self, current_dir):
        tex_files = []
        for root, dirs, files in os.walk(current_dir):
            dirs[:] = [d for d in dirs if d != "setup"]  # Exclude the "setup" directory
            for file in files:
                if file.endswith('.tex') and file != self.output_file_name:
                    full_path = os.path.relpath(os.path.join(root, file), self.base_directory)
                    tex_files.append(os.path.join('..', full_path).replace(os.sep, '/'))
        return tex_files

    def generate_main_tex(self):
        tex_files = self.collect_tex_files(self.base_directory)

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