import re
from typing import Tuple

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

month_names = [
    "[Jj]an(?:uary)?", 
    "[Ff]eb(?:ruary)?", 
    "[Mm]ar(?:ch)", 
    "[Aa]pr(?:il)", 
    "[Mm]ay", 
    "[Jj]une",
    "[Jj]uly",
    "[Aa]ug(?:ust)", 
    "[Ss]ep(?:tember)", 
    "[Oo]ct(?:ober)", 
    "[Nn]ov(?:ember)", 
    "[Dd]ec(?:ember)", 
]

def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day

    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    year = r"\b(?:1\d\d\d|20[0-2]\d)\b"
    month = rf"(?:\b0\d|1[0-2]|%s\b)" % '|'.join(month_names)
    day = r"(?:\b3[01]|[12]\d|0?\d\b)"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """

    for i in range(len(month_names)):
        if re.search(month_names[i], s):
            month_number = str(i + 1) 

    if len(month_number) == 1:
        month_number = zero_pad(month_number)

    return month_number  


def zero_pad(n: str):
    """zero-pad a number string.

    E.g turns '2' into '02'

    Args:
        - n (str) : number to zero pad
    """

    return '0' + n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """

    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}-{month}-{day}"
    ISO_pattern = re.compile(ISO)

    # Date on format DD/MM/YYYY
    DMY = rf"{day} {month} {year}"
    DMY_pattern = re.compile(DMY)

    # Date on format MM/DD/YYYY
    MDY = rf"{month} {day}, {year}"
    MDY_pattern = re.compile(MDY)

    # Date on text format YYYY/MM/DD
    YMD = rf"{year} {month} {day}"
    YMD_pattern = re.compile(YMD)

    all_formats = rf"(?:{ISO}|{DMY}|{MDY}|{YMD})"

    dates = []
    dates = re.findall(all_formats, text)

    new_dates = []
    for date in dates:
        ISO_match = ISO_pattern.search(date)
        DMY_match = DMY_pattern.search(date)
        MDY_match = MDY_pattern.search(date)
        YMD_match = YMD_pattern.search(date)
        
        if ISO_match:
            date_element = re.sub("-", "/", date)
        if DMY_match:
            date_element = re.sub(rf"({day}) ({month}) ({year})", r"\3/\2/\1", date)
        if MDY_match:
            date_element = re.sub(rf"({month}) ({day}), ({year})", r"\3/\1/\2", date)
        if YMD_match:
            date_element = re.sub(rf"({year}) ({month}) ({day})", r"\1/\2/\3", date)
            
        new_dates.append(date_element)

    for n_date in new_dates:
        if not n_date[5].isdigit():
            month = re.findall(rf'([a-zA-Z])', n_date)
            month = ''.join(month)
            new_dates[new_dates.index(n_date)] = n_date.replace(month, str(convert_month(month)))

    for date in new_dates:
        if not date[-2].isdigit():
            new_dates[new_dates.index(date)] = new_dates[new_dates.index(date)][:-1] +  zero_pad(date[-1])

    dates = new_dates

    if output:
        print(f"Write file to {output}")
        file = open(output, "w")
        for d in dates:
            file.write(f"{d}\n")
        file.close()

    return dates