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

## Column Types with Formatting Styles Documentation

This table provides a description of the custom LaTeX column types, along with their corresponding format styles.

| Layout Style | Description                                     | Format Style | Format Description                              |
|--------------|-------------------------------------------------|--------------|-------------------------------------------------|
| A            | Centered column with flexible width             | 1            | Normal Text                                     |
| B            | Centered column with flexible width and green background | 2            | Normal Numbers with no decimal places (integers) |
| C            | Left-aligned column with flexible width         | 3            | Percent numbers with no decimal places          |
| D            | Left-aligned column with flexible width and green background | 4            | Decimal numbers with 1 decimal place            |
| E            | Right-aligned column with flexible width        | 5            | Decimal numbers with 2 decimal places           |
| F            | Right-aligned column with flexible width and green background | 6            | Percent numbers with 2 decimal places        |
| G            | Left-aligned column with fixed width of 2cm     |              |                                                 |
| H            | Left-aligned column with fixed width of 2cm and green background |              |                                                 |
| I            | Left-aligned column with fixed width of 5cm     |              |                                                 |
| J            | Left-aligned column with fixed width of 5cm and green background |              |                                                 |

## Author:

**Name:** Hisham Ali

**Email:** s2hialii@uni-trier.de
