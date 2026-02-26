# Project Documentation — LaTeX Table Generator

**Project:** UniTrier Quality Management Documents Production
**Author:** Hisham Ali (s2hialii@uni-trier.de)
**License:** MIT (2024)
**Current Version:** 2.5.4

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Directory Structure](#2-directory-structure)
3. [Installation & Setup](#3-installation--setup)
4. [How to Run](#4-how-to-run)
5. [Architecture & Data Flow](#5-architecture--data-flow)
6. [Module-by-Module Reference](#6-module-by-module-reference)
   - 6.1 [Entry Point — `main.py`](#61-entry-point--mainpy)
   - 6.2 [GUI — `GUI/UI_tk.py`](#62-gui--guiui_tkpy)
   - 6.3 [Generator — `Generator/table_generator.py`](#63-generator--generatortable_generatorpy)
   - 6.4 [Preprocessing — `preprocessing/base.py`](#64-preprocessing--preprocessingbasepy)
   - 6.5 [Column Processing — `preprocessing/process_columns.py`](#65-column-processing--preprocessingprocess_columnspy)
   - 6.6 [Row Processing — `preprocessing/process_rows.py`](#66-row-processing--preprocessingprocess_rowspy)
   - 6.7 [Censoring — `preprocessing/censored.py`](#67-censoring--preprocessingcensoredpy)
   - 6.8 [Preview Generator — `preprocessing/preview_tex_files.py`](#68-preview-generator--preprocessingpreview_tex_filespy)
   - 6.9 [Utilities — `utils/utils.py`](#69-utilities--utilsutilspy)
7. [Input File Format](#7-input-file-format)
8. [Output File Format](#8-output-file-format)
9. [Column Layout Types](#9-column-layout-types)
10. [Number Format Styles](#10-number-format-styles)
11. [Censoring Modes](#11-censoring-modes)
12. [Style Files (External Configuration)](#12-style-files-external-configuration)
13. [Building a Desktop Application](#13-building-a-desktop-application)
14. [LaTeX Compilation](#14-latex-compilation)
15. [Git Workflow & Branching](#15-git-workflow--branching)
16. [Known Considerations & Gotchas](#16-known-considerations--gotchas)

---

## 1. Project Overview

This project is a **CSV/Excel-to-LaTeX table converter** built for the Quality and Management (QM) department at the University of Trier. It reads tabular data from `.csv`, `.xlsx`, or `.xls` files and generates professionally formatted LaTeX table files (`.tex`) that conform to the department's specific styling requirements.

Key capabilities:
- Batch-converts all CSV/Excel files in a selected directory
- Supports 7 different number formatting styles (integers, decimals, percentages, rounding)
- Provides column layout types (A–Z) for controlling widths, alignment, and coloring
- Three censoring modes (column, cell, row) to mask sensitive data
- Multi-column header merging and multi-row spanning
- Header styling options (bold, italic, 90-degree rotation)
- Generates a `main.tex` preview document that compiles all tables into one PDF
- External style configuration via CSV/Excel files
- Tkinter-based GUI for user interaction

---

## 2. Directory Structure

```
Latex_project/
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
├── README.md                       # Original README with column type tables
├── DOCUMENTATION.md                # This file
├── WorkDocumentation.md            # Development journal (March–November 2024)
├── requirements.txt                # Python dependencies
└── Project_delta/                  # Main Python package
    ├── __init__.py                 # Exports: Processing
    ├── main.py                     # Application entry point
    ├── GUI/
    │   ├── __init__.py
    │   └── UI_tk.py                # Tkinter GUI (v2.5.4)
    ├── Generator/
    │   ├── __init__.py
    │   └── table_generator.py      # Orchestrates the conversion pipeline
    ├── preprocessing/
    │   ├── __init__.py             # Exports: Processing, ProcessColumns, ProcessRows
    │   ├── base.py                 # Core file parsing and LaTeX assembly
    │   ├── process_columns.py      # Column definition and header formatting
    │   ├── process_rows.py         # Row formatting and body generation
    │   ├── censored.py             # Three censoring functions
    │   └── preview_tex_files.py    # Generates main.tex for PDF preview
    └── utils/
        ├── __init__.py
        └── utils.py                # Locale, number formatting, multirow helper
```

---

## 3. Installation & Setup

### Prerequisites
- **Python 3.8+**
- A LaTeX distribution with **LuaLaTeX** (recommended) or **PDFLaTeX**
- The QM department's LaTeX style files (`pageSetup`, `customCommands`, `styles`) placed in a `setup/` directory

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**

| Package       | Version | Purpose                        |
|---------------|---------|--------------------------------|
| pandas        | 2.2.1   | CSV/Excel reading, DataFrames  |
| numpy         | 1.26.4  | Numeric operations             |
| openpyxl      | 3.1.5   | Excel (.xlsx) file support     |
| pyinstaller   | 6.10.0  | Desktop app packaging          |

> **Note:** The `requirements.txt` file has a UTF-16 encoding issue (extra spacing). If `pip install` fails, re-create it as a plain UTF-8 file with these essential packages:
> ```
> pandas==2.2.1
> numpy==1.26.4
> openpyxl==3.1.5
> ```

### Locale Configuration

The application uses German locale for number formatting (thousand separators, decimal commas). The locale is set automatically at import time in `utils/utils.py`:
- **Windows:** `German_Germany.1252`
- **Linux/macOS:** `de_DE.UTF-8` (currently commented out — uncomment line 11 and comment line 10 in `utils/utils.py` if running on Linux/macOS)

---

## 4. How to Run

### From the command line:
```bash
cd Latex_project
python -m Project_delta.main
```

This opens the Tkinter GUI window.

### Basic usage workflow:
1. **(Optional)** Click **"Load Table Styles"** to load a pre-configured style file (CSV/Excel)
2. Select a style from the dropdown, which auto-fills all settings
3. Click **"Select Directory"** to choose the folder containing your CSV/Excel data files
4. Adjust settings manually if needed (layout, format, censoring, etc.)
5. Click **"Generate LaTeX Tables"**
6. Output `.tex` files are written alongside the source files, and a `preview/main.tex` is generated

---

## 5. Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         User (GUI)                              │
│                      UI_tk.py (v2.5.4)                          │
│  Collects: directory path, layout, format, censoring, options   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               LaTeXTableGenerator                               │
│              table_generator.py                                  │
│  Iterates over all .csv/.xlsx/.xls files in the directory       │
│  Creates a Processing instance for each file                    │
│  Then calls PreviewTexFiles to generate main.tex                │
└──────────────────────────┬──────────────────────────────────────┘
                           │  (for each file)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing                                    │
│                    base.py                                        │
│                                                                  │
│  1. Read CSV/Excel file → pandas DataFrame                       │
│  2. Extract header_title (col 0) and caption (last col)          │
│  3. ProcessColumns.normal_columns() → column defs + header cmds  │
│  4. Apply format style (column-wise or row-wise)                 │
│  5. Apply censoring if enabled                                   │
│  6. ProcessRows.rows() → body commands                           │
│  7. Assemble full LaTeX table string                             │
│  8. Write to .tex file                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Module-by-Module Reference

### 6.1 Entry Point — `main.py`

**File:** `Project_delta/main.py`
**Lines:** 8

Creates a Tkinter root window, instantiates `LaTeXTableGeneratorUI`, and starts the main loop. This is the only file you need to run.

---

### 6.2 GUI — `GUI/UI_tk.py`

**File:** `Project_delta/GUI/UI_tk.py`
**Lines:** 433
**Class:** `LaTeXTableGeneratorUI`

The GUI is organized into sections:

| Section | UI Elements | Purpose |
|---------|-------------|---------|
| **Table Style Selection** | Button, Label, Combobox | Load and select pre-defined styles from CSV/Excel |
| **Directory Selection** | Button, Label | Choose input directory containing data files |
| **Style Options** | Entry (Layout), Entry (Format), Radio (Orientation) | Define layout letters, format digits, column/row orientation |
| **Censoring Options** | Checkbox, Radio (Column/Cell/Row), Entry fields | Configure data masking |
| **Additional Options** | Checkboxes | Italic, bold, 90-degree rotation, hline removal, caption/headline removal, column-name removal, multirow |
| **Generate Button** | Button | Triggers `process_directory()` |

**Key methods:**

| Method | Purpose |
|--------|---------|
| `select_directory()` | Opens folder dialog, stores path, enables Generate button |
| `load_style()` | Opens file dialog for style CSV/Excel, parses it into `self.styles_data` |
| `read_styles_file_column(csv_path)` | Static method — reads a style configuration file into a dict of dicts |
| `on_style_name_selected(event)` | Called when user picks a style from the dropdown |
| `apply_style_settings(settings)` | Maps style dict keys to UI variables using the `mapping` dictionary |
| `toggle_censored_entries()` | Shows/hides censoring-related UI fields based on checkbox and radio state |
| `process_directory()` | Gathers all UI values, creates a `LaTeXTableGenerator`, calls `generate_full_tabular` |

**Width detection logic** (in `apply_style_settings`):

| Layout starts with | Width (mm) |
|--------------------|-----------|
| A | 20 |
| B | 30 |
| C | 40 |
| D | 50 |
| E | 70 |
| F | 110 |

This width is passed to the multirow function for `\multirow{n}{<width>mm}{...}`.

---

### 6.3 Generator — `Generator/table_generator.py`

**File:** `Project_delta/Generator/table_generator.py`
**Lines:** 77
**Class:** `LaTeXTableGenerator`

Accepts 24 parameters from the GUI and stores them as instance attributes. The core logic is in the `generate_full_tabular` property:

1. Lists all files in `self.dir_path`
2. For each `.csv`, `.xlsx`, or `.xls` file: creates a `Processing(file_name, self)` instance
3. After all files are processed: calls `PreviewTexFiles(base_directory, self.style_dir_path)` to generate `preview/main.tex`
4. Returns `'-----------DONE-----------'` on success or an error message on failure

**Important:** The `generator` object itself is passed to `Processing`, which reads all configuration from `self.generator.<attribute>`.

---

### 6.4 Preprocessing — `preprocessing/base.py`

**File:** `Project_delta/preprocessing/base.py`
**Lines:** 174
**Class:** `Processing`

This is the **core of the application**. Each instance processes one input file end-to-end.

**Constructor flow (`__init__` → `process_file`):**

1. **Read file:**
   - Excel: `pd.read_excel(file_path, sheet_name=0)`
   - CSV: `pd.read_csv(file_path, delimiter=r'[\t]*;[\t]*', engine='python', encoding='utf-8')`
     - Delimiter is a regex matching semicolons with optional surrounding tabs

2. **Extract metadata:**
   - `header_title` = first column name (used as table headline)
   - `caption` = last column name (used as table caption)
   - `main_data` = DataFrame with first and last columns dropped
   - Columns named `"Unnamed: ..."` (pandas default for empty headers) are treated as empty

3. **Handle "no column names" mode** (`self.generator.column_names == True`):
   - Column names become the first data row
   - Actual column headers are replaced with integer indices
   - `header_commands` is set to empty strings

4. **Generate column definitions and headers:**
   - `ProcessColumns.normal_columns(...)` → returns `(column_definitions, header_commands)`

5. **Apply number formatting** (column-wise or row-wise based on `choose_which`):
   - Column-wise: `ProcessColumns.format_style(data, format_string)`
   - Row-wise: `ProcessRows.format_style(data, format_string)`

6. **Apply censoring** if enabled (column, cell, or row mode)

7. **Generate body rows:**
   - `ProcessRows.rows(row_values, multirow, width)` → list of LaTeX row strings

8. **Assemble full LaTeX table** based on flags:
   - 4 variants depending on `remove_table_caption` and `remove_table_headline` combinations
   - 2 variants for `horizontal_line` (with/without `\hline` after header)

9. **Write output** to `<filename>.tex` in the same directory as the input file

---

### 6.5 Column Processing — `preprocessing/process_columns.py`

**File:** `Project_delta/preprocessing/process_columns.py`
**Lines:** 120
**Class:** `ProcessColumns`

#### `normal_columns(column_names, columns_number, column_styles, first_row_italic, first_row_bold, first_row_90_degree)`

Returns `(column_definitions: list, header_commands: list[str])`.

- **`column_definitions`**: A list of single-letter layout codes (e.g., `['A', 'R', 'R', 'R']`), truncated or padded with `'X'` to match the actual number of data columns.
- **`header_commands`**: LaTeX commands for each header cell, handling:
  - Multi-column merging: consecutive `"Unnamed"` columns after a named column are merged into one `\multicolumn{n}{c}{...}`
  - Alternating green background: even-indexed real columns get `\cellcolor{green40}`
  - Styling: `\textit{}`, `\textbf{}`, `\rotatebox{90}{}`

**Validation:** Raises `ValueError` if `column_styles` contains non-alphabetic characters or is empty.

#### `format_style(data, format_string)`

Applies `apply_format(value, style_digit)` column-by-column. Each digit in `format_string` maps to a column index. If there are more columns than digits, extra columns are left unformatted.

**Validation:** Raises `ValueError` if `format_string` contains non-digit characters or is empty.

---

### 6.6 Row Processing — `preprocessing/process_rows.py`

**File:** `Project_delta/preprocessing/process_rows.py`
**Lines:** 62
**Class:** `ProcessRows`

#### `rows(row_values, multirow, width)`

Converts a list of lists into LaTeX row strings:
- `NaN` values → `'-'`
- Cells joined with ` & `
- Each row terminated with ` \\ \hline` (except the last row: just ` \\ `)
- If `multirow is True`, passes through `multi_row()` to handle row spanning

#### `format_style(data, format_string)`

Applies `apply_format()` row-by-row. The format string digit is selected by cycling: `format_string[row_index % len(format_string)]`. This means the same format digit applies to **every cell in a given row**.

---

### 6.7 Censoring — `preprocessing/censored.py`

**File:** `Project_delta/preprocessing/censored.py`
**Lines:** 59

Three standalone functions that modify a DataFrame in-place and return it:

#### `column_censoring(data, trigger_number, trigger_column, affected_columns)`
- For each row: if the value in `trigger_column` < `trigger_number`, replace values in all `affected_columns` with `'XXX'`
- Column indices are **1-based** (user-facing)
- `affected_columns` is a comma-separated string (e.g., `"1,2,5"`)

#### `cell_censoring(data, trigger_number, affected_cells)`
- Scans every column independently
- When a cell value < `trigger_number`, the next N cells (`affected_cells`) in the same column are replaced with `'XXX'`
- Skips forward by `affected_cells` after each trigger

#### `row_censoring(data, trigger_number, trigger_row, affected_rows)`
- Checks each cell in `trigger_row`
- If a cell value < `trigger_number`, the same column position in all `affected_rows` is replaced with `'XXX'`
- Row indices are **1-based**
- `affected_rows` is a comma-separated string

---

### 6.8 Preview Generator — `preprocessing/preview_tex_files.py`

**File:** `Project_delta/preprocessing/preview_tex_files.py`
**Lines:** 79
**Class:** `PreviewTexFiles`

Generates a `preview/main.tex` file that compiles all generated tables into a single document.

**Constructor:**
- `base_directory`: the directory containing the generated `.tex` files
- `styles_absolute_path`: absolute path to the directory containing `setup/` with LaTeX style files
- `output_file_name`: defaults to `'main.tex'`

**Logic:**
1. Writes LaTeX preamble with `\input` statements for `pageSetup`, `customCommands`, and `styles`
2. Collects all `.tex` files that have a matching source file (`.csv`, `.xlsx`, etc.)
3. Sorts files using natural sort (so `table2a.tex` comes before `table10.tex`)
4. Generates `\input{../relative/path/to/table.tex}` for each
5. Creates `preview/` subdirectory if it doesn't exist
6. Writes the file

**Generated structure:**
```latex
\input{/absolute/path/to/setup/pageSetup}
\input{/absolute/path/to/setup/customCommands}
\input{/absolute/path/to/setup/styles}

\begin{document}
    \section*{Vorschau der Tabellen}
\input{../table1.tex}
\input{../table2.tex}
\end{document}
```

---

### 6.9 Utilities — `utils/utils.py`

**File:** `Project_delta/utils/utils.py`
**Lines:** 93

#### `set_locale()`
Sets the process locale to German. Called at module import time (line 93). Required for `locale.format_string()` to use German number formatting (e.g., `1.234,56`).

#### `remove_dots(value)`
Cleans raw number strings:
1. Strips `%`
2. Replaces `,` with `.`
3. If multiple dots exist (e.g., `1.234.567.89`), keeps only the last one as decimal separator

#### `apply_format(value, style)`
The central number formatting function. Takes a raw value and a single-digit style character:

| Style | Output | Example |
|-------|--------|---------|
| `'1'` | Plain text, NaN → empty string | `"Hello"` → `"Hello"` |
| `'2'` | Integer with thousand grouping | `1234` → `"1.234"` |
| `'3'` | Integer percent (no decimals) | `45` → `"45\%"` |
| `'4'` | 1 decimal place | `3.14159` → `"3,1"` |
| `'5'` | 2 decimal places | `3.14159` → `"3,14"` |
| `'6'` | Percent with 2 decimals | `45.678` → `"45,68\%"` |
| `'7'` | Rounded to nearest 100 | `1234` → `"1.200"` |

All numeric styles return `'-'` for NaN/empty values. On parse failure (ValueError, TypeError, OverflowError), returns the value as-is.

#### `multi_row(rows_full, width)`
Post-processes body row strings to add `\multirow` commands:
1. Scans the first cell of each row
2. When a non-empty first cell is found, counts consecutive empty/NaN first cells below it
3. Wraps the first cell in `\multirow{<count>}{<width>mm}{<text>}`
4. Replaces first cells of spanned rows with empty string
5. Removes `\hline` between spanned rows

---

## 7. Input File Format

### CSV Files
- **Delimiter:** Semicolon (`;`), optionally surrounded by tabs
- **Encoding:** UTF-8
- **Structure:**

| Column 0 (Header Title) | Data Column 1 | Data Column 2 | ... | Last Column (Caption) |
|--------------------------|---------------|---------------|-----|----------------------|
| row 1 data               | value         | value         | ... | row 1 data           |
| row 2 data               | value         | value         | ... | row 2 data           |

- The **first column name** becomes the table headline
- The **last column name** becomes the table caption
- Both are dropped from the actual table data
- Column names starting with `"Unnamed"` are treated as part of a multi-column header

### Excel Files
- First sheet is read (`sheet_name=0`)
- Same structure as CSV (first column = headline, last column = caption)

---

## 8. Output File Format

For each input file `example.csv`, the output is `example.tex` in the same directory.

**Generated LaTeX structure (with headline and caption, with hline):**
```latex
\begin{table}[H]
\tblheadline{Header Title Text}
\tblfont
\begin{tabularx}{\textwidth}{ARSRS}
\multicolumn{1}{c}{Col1} & \multicolumn{1}{c}{\cellcolor{green40}Col2} & ... \\ \hline
data1 & data2 & ... \\ \hline
data3 & data4 & ... \\
\end{tabularx}
\tblcaption{Caption Text}
\end{table}
\normalspacing
\vspace{0.5cm}
```

**Custom LaTeX commands used** (defined in the QM department's style files):
- `\tblheadline{...}` — table headline above the tabular
- `\tblfont` — sets the font/size for the table
- `\tblcaption{...}` — table caption below the tabular
- `\normalspacing` — restores normal line spacing after the table

---

## 9. Column Layout Types

### Version 2026 (Current)

| Letter | Category | Description |
|--------|----------|-------------|
| **A** | First column | Left-aligned, fixed width 20 mm |
| **B** | First column | Left-aligned, fixed width 30 mm |
| **C** | First column | Left-aligned, fixed width 40 mm |
| **D** | First column | Left-aligned, fixed width 50 mm |
| **E** | First column | Left-aligned, fixed width 70 mm |
| **F** | First column | Left-aligned, fixed width 110 mm |
| **R** | Data column | Left-aligned, flexible width, green background |
| **S** | Data column | Left-aligned, flexible width |
| **T** | Data column | Centered, flexible width, green background |
| **U** | Data column | Centered, flexible width |
| **V** | Data column | Right-aligned, flexible width, green background |
| **W** | Data column | Right-aligned, flexible width |

### Version 2025 (Legacy)

| Letter | Description |
|--------|-------------|
| A | Centered, flexible width |
| B | Centered, flexible width, green background |
| C | Left-aligned, flexible width |
| D | Left-aligned, flexible width, green background |
| E | Right-aligned, flexible width |
| F | Right-aligned, flexible width, green background |
| G | Left-aligned, fixed 2 cm |
| H | Left-aligned, fixed 2 cm, green background |
| I | Left-aligned, fixed 5 cm |
| J | Left-aligned, fixed 5 cm, green background |
| K | Left-aligned, fixed 12 cm |
| L | Left-aligned, fixed 12 cm, green background |
| R | Left-aligned, fixed 7 cm |
| S | Centered, fixed 0.5 cm, green background |
| T | Centered, fixed 0.5 cm |
| U | Left-aligned, fixed 10.5 cm |
| V | Left-aligned, fixed 2.5 cm |
| Y | Left-aligned, fixed 3.5 cm |
| Z | Left-aligned, fixed 4 cm |

> These column types are defined in the QM department's LaTeX `.sty` style files (not in this Python project). The Python code simply writes the letter into the `\begin{tabularx}` column specification.

### How the Layout String Works

The layout string is a sequence of letters, one per column. For example, with 4 data columns:

- `ARSR` → first column 20mm fixed, second left-aligned green, third left-aligned, fourth left-aligned green
- `CTTT` → first column 40mm fixed, remaining three centered green

If the layout string has fewer letters than columns, the remaining columns default to `X` (standard tabularx flexible width).

---

## 10. Number Format Styles

The format string is a sequence of digits, one per column (column-wise) or cycled per row (row-wise).

| Digit | Type | Decimal Places | Suffix | NaN Handling |
|-------|------|----------------|--------|-------------|
| **1** | Plain text | — | — | Empty string |
| **2** | Integer | 0 | — | `'-'` |
| **3** | Percent integer | 0 | `\%` | `'-'` |
| **4** | Decimal | 1 | — | `'-'` |
| **5** | Decimal | 2 | — | `'-'` |
| **6** | Percent decimal | 2 | `\%` | `'-'` |
| **7** | Rounded to 100s | 0 | — | `'-'` |

### Column-wise vs. Row-wise Orientation

- **Column-wise** (`choose_which == "column"`): digit at position `i` applies to column `i`. E.g., `"12345"` → col 0 is text, col 1 is integer, col 2 is percent, etc.
- **Row-wise** (`choose_which == "row"`): the format string cycles over rows. E.g., `"23"` → row 0 uses style 2, row 1 uses style 3, row 2 uses style 2, etc. The same style applies to every cell in that row.

---

## 11. Censoring Modes

Censoring replaces data values with `'XXX'` based on a trigger condition (`value < trigger_number`).

### Column Censoring
- **Trigger column:** a specific column number (1-based) whose values are checked
- **Trigger value:** if the trigger column's value < this number, censoring activates for that row
- **Affected columns:** comma-separated column numbers (1-based) whose values get replaced with `'XXX'`

**Example:** Trigger column = 3, trigger value = 5, affected columns = "4,5"
→ For any row where column 3 < 5, columns 4 and 5 are replaced with `'XXX'`.

### Cell Censoring
- **Trigger value:** threshold for individual cell values
- **Number of affected cells:** N cells below the trigger cell (in the same column) are censored

This scans every column independently. When a cell < trigger value, the next N cells below it become `'XXX'`.

### Row Censoring
- **Trigger row:** a specific row number (1-based) whose cell values are checked
- **Trigger value:** threshold for each cell in the trigger row
- **Affected rows:** comma-separated row numbers (1-based) whose cells get replaced

For each column: if the trigger row's cell < trigger value, the same column position in all affected rows becomes `'XXX'`.

---

## 12. Style Files (External Configuration)

Pre-defined table styles can be loaded from a CSV or Excel file. The file format:

| (Variable Name) | Style1 | Style2 | Style3 |
|------------------|--------|--------|--------|
| Layout           | ARSRS  | CTTTT  | BRSRS  |
| Format           | 12222  | 15555  | 13333  |
| Orientation      | column | row    | column |
| Censoring        | 0      | 1      | 0      |
| censoringMode    | column | cell   | column |
| TriggerColumnValue | 5    | 3      | 5      |
| TriggerColumn    | 2      |        | 3      |
| AffectedColumns  | 3,4    |        | 4,5    |
| TriggerRowValue  |        |        |        |
| TriggerRow       |        |        |        |
| AffectedRows     |        |        |        |
| CellTriggerValue |        | 10     |        |
| NumberOfCells    |        | 2      |        |
| FirstRowItalics  | 0      | 0      | 1      |
| FirstRow90       | 0      | 1      | 0      |
| FirstRowBold     | 1      | 0      | 0      |
| RemoveHline      | 0      | 1      | 0      |
| RemoveCaption    | 0      | 0      | 1      |
| RemoveHeadline   | 0      | 0      | 0      |
| RemoveColumnNames| 0      | 0      | 0      |
| MultiRow         | 0      | 0      | 1      |

- First column = variable names (keys)
- Subsequent columns = style values (one column per named style)
- Boolean fields: `"1"` = true, `"0"` or empty = false
- The style file must be located alongside the `setup/` directory (its parent directory path is used as `styles_absolute_path` for LaTeX compilation)

---

## 13. Building a Desktop Application

Use PyInstaller to package the application as a standalone executable:

```bash
pyinstaller --onefile --name QM_TableGenerator --icon /path/to/icon.ico --windowed Project_delta/main.py
```

The executable will be in the `dist/` directory. Note that:
- The `--windowed` flag hides the console window (GUI-only)
- `--onefile` bundles everything into a single `.exe`
- Windows-specific dependencies (`pywin32-ctypes`, `pefile`) are only needed for Windows builds

---

## 14. LaTeX Compilation

The generated `preview/main.tex` requires the QM department's style files. To compile:

```bash
cd /path/to/output/preview/
lualatex main.tex
```

Or with PDFLaTeX:
```bash
pdflatex main.tex
```

**Required LaTeX packages** (typically included in the QM style files):
- `tabularx` — flexible-width tables
- `multirow` — row spanning
- `xcolor` — cell background colors (specifically `green40`)
- `float` — `[H]` placement specifier
- `graphicx` — `\rotatebox` command

---

## 15. Git Workflow & Branching

**Main branch:** `master`

**Branch naming convention:** `#<issue-number>-<feature-name>` for feature branches

**Recent merged features (by PR):**

| PR | Feature |
|----|---------|
| #62 | Row censoring |
| #60 | Excel file support (.xlsx, .xls) |
| #58 | Multirow handling |
| #52 | Main.tex compilation / preview |
| #50 | UI redesign |
| #48 | Style file loading |
| #46 | Display selected path in UI |
| #45 | Censoring trigger value UI |
| #44 | Headline checkbox |
| #41 | German decimal format |

---

## 16. Known Considerations & Gotchas

1. **Locale dependency:** The application sets the locale globally at import time. If the German locale is not installed on the system, number formatting will fall back to default behavior. On Linux, ensure `de_DE.UTF-8` is available (`sudo locale-gen de_DE.UTF-8`), and switch the active locale line in `utils/utils.py`.

2. **CSV delimiter:** The CSV parser uses a regex delimiter `[\t]*;[\t]*` which matches semicolons with optional tabs. Standard comma-delimited CSVs will **not** work — files must use semicolons.

3. **UTF-8 BOM:** The code strips `\ufeff` (Byte Order Mark) from column names. If you encounter encoding issues, ensure files are saved as UTF-8 without BOM.

4. **requirements.txt encoding:** The file has a UTF-16 encoding issue with extra null bytes between characters. If you need to regenerate it, save as plain UTF-8.

5. **Single-threaded GUI:** The application runs on Tkinter's main thread. Large batch operations will freeze the UI until processing completes. There is no progress bar or background thread.

6. **No automated tests:** The project does not have a test suite. `process_rows.py` has a `__main__` block with example code that can serve as a manual test.

7. **Style files are external:** The LaTeX `.sty` files that define column types (A–Z) and custom commands (`\tblheadline`, `\tblfont`, etc.) are maintained separately by the QM department. This Python project only generates references to them.

8. **Censoring is destructive to the DataFrame:** Censoring functions modify the pandas DataFrame in-place. This doesn't cause issues in normal use since each file gets a fresh DataFrame, but be aware if reusing `Processing` objects.

9. **Column count mismatch:** If the layout string has fewer letters than data columns, remaining columns get `'X'` (standard tabularx). If the format string has fewer digits than columns (in column-wise mode), remaining columns are left unformatted.

10. **The "Remove Horizontal Line" checkbox** is counterintuitively named: when checked (`True`), it removes the `\hline` after the header row. The body rows' `\hline` separators remain regardless.
