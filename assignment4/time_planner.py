import re
import bs4
import pandas as pd
from bs4 import BeautifulSoup

from copy import copy
from dataclasses import dataclass
from requesting_urls import get_html

## --- Task 5, 6, and 7 ---- ##

event_types = {
    "DH": "Downhill",
    "SL": "Slalom",
    "GS": "Giant Slalom",
    "SG": "Super Giant slalom",
    "AC": "Alpine Combined",
    "PG": "Parallel Giant Slalom",
}

def time_plan(url: str) -> str:
    """Parses table from html text and extract desired information
    and saves in betting slip markdown file

    arguments:
        url (str) : URL for page with calendar table
    return:
        markdown (str) : string containing the markdown schedule
    """

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    calendar = soup.find(id="Calendar")
    soup_table = calendar.find_next("table", {"class": "wikitable"})
    df = extract_events(soup_table)

    return render_schedule(df)


@dataclass
class TableEntry:
    """Data class representing a single entry in a table

    Records text content, rowspan, and colspan attributes
    """

    text: str
    rowspan: int
    colspan: int


def extract_events(table: bs4.element.Tag) -> pd.DataFrame:
    """Gets the events from the table

    arguments:
        table (bs4.element.Tag) : Table containing data
    return:
        df (DataFrame) : DataFrame containing filtered and parsed data
    """

    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]
    data = []

    rows = table.find_all("tr")
    rows = rows[1:]

    for tr in rows:
        cells = tr.find_all("td")
        row = []
        for cell in cells:
            colspan = 1 if cell.get('colspan') == None else int(cell.get('colspan'))
            rowspan = 1 if cell.get('rowspan') == None else int(cell.get('rowspan'))

            text = strip_text(cell.get_text(strip=True))
            row.append(
                TableEntry(
                    text=text,
                    rowspan=rowspan,
                    colspan=colspan,
                )
            )        
        data.append(row)

    all_data = expand_row_col_span(data)
    wanted = ["Date", "Venue", "Type"]
    filtered_data = filter_data(labels, all_data, wanted)
    df = pd.DataFrame(filtered_data, columns=wanted)

    return df


def render_schedule(data: pd.DataFrame) -> str:
    """Renders the schedule data to markdown

    arguments:
        data (DataFrame) : DataFrame containing table to write
    return:
        markdown (str): the rendered schedule as markdown
    """

    def expand_event_type(type_key):
        """Expands event type key (SL) to full name (Slalom)

        Args:
            type_key (str): 
                abbreviation from event types. 
        Returns:
            (str): 
                the full name of event type.
        """

        return event_types.get(type_key[:2], type_key)

    data['Type'] = data['Type'].apply(expand_event_type)
    
    return data.to_markdown()


def strip_text(text: str) -> str:
    """Gets rid of cruft from table cells, footnotes and setting limit to 20 chars

    arguments:
        text (str) : string to fix
    return:
        text (str) : the string fixed
    """

    text = text[:30]  
    text = re.sub(r"\[.*\]", "", text)

    return text


def filter_data(keys: list, data: list, wanted: list):
    """Filters away the columns not specified in wanted argument

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (list of lists) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """

    filtered_df = pd.DataFrame(data, columns=keys)

    return filtered_df[wanted] 

def expand_row_col_span(data):
    """Applies row/colspan to tabular data

    - Copies cells with colspan to columns to the right
    - Copies cells with rowspan to rows below
    - Returns raw data (removing TableEntry wrapper)

    arguments:
        data_table (list) : data with rows and cols
            Table of the form:

            [
                [ # row
                    TableEntry(text='text', rowspan=2, colspan=1),
                ]
            ]
    return:
        new_data_table (list): list of lists of strings
            [
                [
                    "text",
                    "text",
                    ...
                ]
            ]

            This should be a dense matrix (list of lists) of data,
            where all rows have the same length,
            and all values are `str`.
    """

    new_data = []
    for row in data:
        new_row = []
        new_data.append(new_row)
        for entry in row:
            for _ in range(entry.colspan):
                new_entry = copy(entry)
                new_entry.colspan = 1
                new_row.append(new_entry)

    for row_idx, row in enumerate(new_data):
        for col_idx, entry in enumerate(row):
            for offset in range(1, entry.rowspan):
                target_row = new_data[row_idx + offset]
                new_entry = copy(entry)
                new_entry.rowspan = 1
                target_row.insert(col_idx, new_entry)
            entry.rowspan = 1

    return [[entry.text for entry in row] for row in new_data]

if __name__ == "__main__":
    # test the script on the past few years by running it:
    for year in range(20, 23):
        url = (
            f"https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup"
        )
        
        print(url)
        md = time_plan(url)
        print(md)
