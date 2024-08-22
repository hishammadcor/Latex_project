# UniTrier Quality Management Documents production project.

## Introduction
This project is developed under the supervision of the Quality and Management department. It is responsible for handling CSV files to produce LaTeX tables, which are later imported into the Year document. The project adheres to the LaTeX specifications of the QM department at UniTrier.

## Installation
- The project runs on Python. To get started, install the necessary dependencies by running the following command in your terminal:

  ```bash
  pip install -r requirements.txt
  ```
- After installing the required packages, run the main Python file.

- The main LaTeX project is compiled using LuaLaTeX. However, the produced tables can also be compiled in a standard PDFLaTeX environment.

- If you wish to create a desktop application for this project, use PyInstaller by running the following command:

  ```bash 
  pyinstaller --onefile --name MyApp --icon /path/to/icon.ico --windowed /path/to/Project_delta/main.py
  ```

## ToDOs:
- [x] Add a format style cell to the GUI interface to allow the users to add the number combination of the tables columns/rows format.
- [x] Radio Button for the format style box to choose between columns or rows
- [x] Develop a preprocessing class to deal with the numbers in columns or rows according to the Format style cell input & trigger Function that censor certain input according to a relation to a column.
- [x] Check box for the trigger function
- [x] 2 Text boxes for the trigger column and the censored columns
- [x] Code a function specified for the letter D, as the letter D is 90 degree orientation.
- [ ] Make a full documentation on the Column letters style. (We have 27 Uppercase letters and 27 Lower case letters "Lower case used for colored columns")
- [x] Deploy the UI on windows.
- [x] Process the header table title and add check box for the caption of the table form the csv file to be added to the table (Should be written as latex command).
- [ ] _Optional_ Table view for the CSV in the UI. This would be easy for the Format style in  case of row.
- [x] Check box for removing/putting _\hline_ after the header of a multicolumn table or not.
- [x] Check box for making the first row of the table italic or not
- [x] Predefined specific letters, if found in the letter combination then this column will have special number operations like approximations, thousands separators...etc
- [x] After seeing how could I help after 01.07.2024 Monday's meeting with our colleague, Preprocessing the UNI-Portal CSV files.
- [x] Add a Layout style cell to the GUI interface to allow the users to add the letters combination of the tables columns.

## Author:

**Name:** Hisham Ali

**Email:** s2hialii@uni-trier.de
