import locale
import pandas as pd

def set_locale():
    """
    Sets locale to German settings.
    """
    try:
        locale.setlocale(locale.LC_ALL, 'German_Germany.1252') # this is locale windows settings
        # locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # I think this is linux/macOS locale settings # Adjust based on your system
    except locale.Error:
        print("Locale not supported or settings are not correctly adjusted, return to class ProcessRows and ProcessColumns.")


def apply_format(value, style):
    try:
        if style == '1':
            value = str(value)
            float_value = float(value)
            if pd.isna(value) or pd.isna(float_value):
                return ''
            return str(value)

        value = str(value).replace('%', '').replace(',', '.')
        if value.count('.') > 1:
            last_dot_index = value.rfind('.')
            value = value[:last_dot_index].replace('.', '') + value[last_dot_index:]  # Remove all dots in the substring except the last dot
        float_value = float(value)
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


set_locale()
