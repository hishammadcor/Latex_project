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

## Column Types with Formatting Styles Documentation Old_Version 2025

This table provides a description of the custom LaTeX column types, along with their corresponding format styles.

| Layout Style | Description                                                       | Format Style | Format Description                                                          |
|--------------|-------------------------------------------------------------------|--------------|-----------------------------------------------------------------------------|
| A            | Centered column with flexible width                               | 1            | Normal Text                                                                 |
| B            | Centered column with flexible width and green background          | 2            | Normal Numbers with no decimal places (integers)                            |
| C            | Left-aligned column with flexible width                           | 3            | Percent numbers with no decimal places                                      |
| D            | Left-aligned column with flexible width and green background      | 4            | Decimal numbers with 1 decimal place                                        |
| E            | Right-aligned column with flexible width                          | 5            | Decimal numbers with 2 decimal places                                       |
| F            | Right-aligned column with flexible width and green background     | 6            | Percent numbers with 2 decimal places                                       |
| G            | Left-aligned column with fixed width of 2cm                       | 7            | Normal Numbers with no decimal places rounded to the nearest 100 (integers) |
| H            | Left-aligned column with fixed width of 2cm and green background  |              |                                                                             |
| J            | Left-aligned column with fixed width of 5cm and green background  |              |                                                                             |
| I            | Left-aligned column with fixed width of 5cm                       |              |                                                                             |
| K            | Left-aligned column with fixed width of 12 cm                     |              |                                                                             |
| L            | Left-aligned column with fixed width of 12cm and green background |              |                                                                             |
| R            | Left-aligned column with fixed width of 7cm                       |              |                                                                             |
| S            | Centered column with fixed width of 0.5cm and green background    |              |                                                                             |
| T            | Centered column with fixed width of 0.5cm                         |              |                                                                             |
| U            | Left-aligned column with fixed width of 10.5cm                    |              |                                                                             |
| V            | Left-aligned column with fixed width of 2.5cm                     |              |                                                                             |
| Y            | Left-aligned column with fixed width of 3.5cm                     |              |                                                                             |
| Z            | Left-aligned column with fixed width of 4cm                       |              |                                                                             |

## Column Types with Formatting Styles Documentation New_Version 2026

| Category      | Layout | Description                                               | Format Style | Format Description                                                          |
|---------------|--------|-----------------------------------------------------------|--------------|-----------------------------------------------------------------------------|
| First column  | A      | Left-aligned column with fixed width of 20 mm             | 1            | Normal Text                                                                 |
| First column  | B      | Left-aligned column with fixed width of 30 mm             | 2            | Normal Numbers with no decimal places (integers)                            |
| First column  | C      | Left-aligned column with fixed width of 40 mm             | 3            | Percent numbers with no decimal places                                      |
| First column  | D      | Left-aligned column with fixed width of 50 mm             | 4            | Decimal numbers with 1 decimal place                                        |
| First column  | E      | Left-aligned column with fixed width of 70 mm             | 5            | Decimal numbers with 2 decimal places                                       |
| First column  | F      | Left-aligned column with fixed width of 110 mm            | 6            | Percent numbers with 2 decimal places                                       |
| Left          | R      | Left-aligned column with flexible width, green background | 7            | Normal Numbers with no decimal places rounded to the nearest 100 (integers) |
| Left          | S      | Left-aligned column with flexible width                   |              |                                                                             |
| Centered      | T      | Centered column with flexible width, green background     |              |                                                                             |
| Centered      | U      | Centered column with flexible width                       |              |                                                                             |
| Right         | V      | Right-aligned column with flexible width, green background|              |                                                                             |
| Right         | W      | Right-aligned column with flexible width                  |              |                                                                             |


## Author:

**Name:** Hisham Ali

**Email:** s2hialii@uni-trier.de
