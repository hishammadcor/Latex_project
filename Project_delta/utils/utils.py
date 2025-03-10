import locale
import pandas as pd


def set_locale():
    """
    Sets locale to German settings.
    """
    try:
        locale.setlocale(locale.LC_ALL, 'German_Germany.1252')  # this is locale windows settings
        # locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # I think this is linux/macOS locale settings # Adjust based on your system
    except locale.Error:
        print(
            "Locale not supported or settings are not correctly adjusted, return to class ProcessRows and ProcessColumns.")


def remove_dots(value):
    after_value = str(value).replace('%', '').replace(',', '.')
    if after_value.count('.') > 1:
        last_dot_index = after_value.rfind('.')
        end_value = after_value[:last_dot_index].replace('.', '') + after_value[
                                                                    last_dot_index:]  # Remove all dots in the substring except the last dot
        return end_value
    else:
        return after_value


def apply_format(value, style):
    try:
        if style == '1':
            value = str(value)
            if pd.isna(value) or value == 'nan':
                return ''
            return str(value)

        processed_value = remove_dots(value)
        # if float(processed_value) is True:
        float_value = float(processed_value)
        if pd.isna(value) or pd.isna(float_value):
            return '-'
        elif style == '2':
            return f'\\rightalignbox{{{locale.format_string("%d", round(float_value), grouping=True)}}}'
        elif style == '3':
            return f'\\rightalignbox{{{locale.format_string("%d", round(float_value), grouping=True)}\\%}}'
        elif style == '4':
            return f'\\rightalignbox{{{locale.format_string("%.1f", round(float_value, 1), grouping=True)}}}'
        elif style == '5':
            return f'\\rightalignbox{{{locale.format_string("%.2f", round(float_value, 2), grouping=True)}}}'
        elif style == '6':
            return f'\\rightalignbox{{{locale.format_string("%.2f", round(float_value, 2), grouping=True)}\\%}}'
        elif style == '7':
            return f'\\rightalignbox{{{locale.format_string("%d", round(float_value, -2), grouping=True)}}}'
        else:
            return str(value)
    except (ValueError, TypeError, OverflowError):
        return str(value)


def multi_row(rows_full):
    reference = None
    modified_rows = []

    for index, row in enumerate(rows_full):
        row = row.split(' & ')
        first_entry = row[0]
        if first_entry != '-' and not pd.isna(first_entry) and first_entry != 'nan' and first_entry != '':
            i = 1
            for next_row in rows_full[index + 1:]:
                next_row = next_row.split(' & ')
                if pd.isna(next_row[0]) or next_row[0] == '-' or next_row[0] == 'nan' or next_row[0] == '':
                    i += 1
                else:
                    break

            reference = f'\\multirow{{{i}}}{{*}}{{{first_entry}}}'
            row[0] = str(reference)
        else:
            if reference:
                row[0] = ""

        row_string = ' & '.join(row)
        if index < len(rows_full) - 1:
            next_first_entry = rows_full[index + 1].split(' & ')[0].strip()
            if next_first_entry == '-' or next_first_entry.lower() == 'nan' or pd.isna(next_first_entry) or next_first_entry == '':
                row_string = row_string.replace('\\hline', '')

        modified_rows.append(row_string)

    return modified_rows

set_locale()
