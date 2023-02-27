from typing import Dict, Optional
import requests

## -- Task 1 -- ##

def get_html(url: str, params: Optional[Dict] = None, output: Optional[str] = None):
    """Gets an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """

    response = requests.get(url, params=params)
    html_str = response.text

    if output:
        f = open(output, "w")
        f.write(url + "\n" + html_str)
        f.close()

    return html_str
