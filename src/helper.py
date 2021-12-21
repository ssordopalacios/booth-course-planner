import copy
from operator import itemgetter
import pandas as pd


def section_to_program(section):
    """Transform a section number into program

    Args:
        section (int): The number of the section

    Returns:
        str: The name of the program
    """

    if section in range(1, 10):
        return "Full-Time"
    elif section in range(81, 85):
        return "Evening"
    elif section in range(85, 87):
        return "Weekend"
    elif section in range(87, 94):
        return "EMBA"
    elif section == 50 or section == 60:
        return "PhD"
    else:
        return "NA"


def qtr_to_quarter(qtr):
    """Transform a quarter into the standard form

    Args:
        qtr (str): The initial quarter

    Returns:
        str: The standardized quarter
    """

    qtr_dict = {
        1: (1, "Autumn"),
        "AUT": (1, "Autumn"),
        "Autumn": (1, "Autumn"),
        2: (2, "Winter"),
        "WIN": (2, "Winter"),
        "Winter": (2, "Winter"),
        3: (3, "Spring"),
        "SPR": (3, "Spring"),
        "Spring": (3, "Spring"),
        0: (4, "Summer"),
        "SUM": (4, "Summer"),
        "Summer": (4, "Summer"),
    }
    return qtr_dict[qtr]


def yq_to_year_quarter(yq):

    year = int(yq // 1)
    quarter = qtr_to_quarter(int(4 * (yq % 1)))
    return (year, quarter)


def modality(note):
    """Extract modality from note in booth schedule

    Args:
        note (str): The note description

    Returns:
        str: The modality of the course
    """

    modality_dict = {
        "In-Person Only": "IP",
        "Remote-Only": "R",
        "Dual Modality": "D",
        "Faculty In-Person, Dual Modality": "D-FIP",
        "Faculty Remote, Dual Modality": "D-FR",
    }
    if note in modality_dict:
        return modality_dict[note]
    else:
        return ""


def summarize(df, group_vars):
    """Summarized a df a group of variables

    Args:
        df (DataFrame): The df to group
        group_vars (list): The names of variables to group by

    Returns:
        DataFrame: The grouped dataframe
    """

    # Create a numerical representation of the last time the course was offered
    df["Q"] = pd.Series(map(itemgetter(0), df["Quarter"])) / 4
    df["YQ"] = df["Year"] + df["Q"]
    df = df.drop(columns=["Q"])

    # Create a copy fo the dataframe and subset variables to find maximum of
    df_last = copy.deepcopy(df)
    sub_vars = copy.deepcopy(group_vars)
    sub_vars.extend(["YQ"])
    df_last = df_last[sub_vars]

    # Find the maximum YQ on which the quarter was offered
    # This represents the last time that this course was offered
    df_last = df_last.groupby(group_vars, as_index=False).max()

    # Merge df and df_last, keeping only unique observations
    df_merge = pd.merge(df, df_last, how="inner", on=sub_vars)

    # Then for cases that are still not unique, find the median
    df_merge = df_merge.groupby(group_vars, as_index=False).median()
    df_merge = df_merge.drop(columns=["YQ"])

    # Identify columns to drop
    drop_columns = [
        c for c in base if c in df_merge.columns and c not in group_vars
    ]
    df_merge = df_merge.drop(columns=drop_columns)

    return df_merge


def remove_ascii(string):
    """Removes non-ASCII characters

    Args:
        string (str): Original string

    Returns:
        str: New string
    """
    if pd.isnull(string):
        return ""
    else:
        encoded_string = string.encode("ascii", "ignore")
        return encoded_string.decode()


# Store a base column ordering that all files should follow
base = [
    "Course",
    "Title",
    "Year",
    "Quarter",
    "Program",
    "Section",
    "Last Name",
    "First Name",
    "Day",
    "Time",
]


def column_ordering(df_columns, additional=[]):
    """Create a column ordering

    Args:
        df_columns (Index): The name of the columns
        additional (list, optional): Additional columns. Defaults to [].

    Returns:
        list: The ordered columns
    """

    # Remove columns from base that does not exist
    # For example, "Section" is not included in some files
    selected = [c for c in base if c in df_columns]

    # Extend by any additional columns selected
    selected.extend(additional)

    # Then find the other columns in the dataframe and include in order
    remaining = [c for c in df_columns if c not in selected]

    # Extend selected by remaining and return
    selected.extend(remaining)
    return selected


def column_sorting(df_columns):
    """Creates a column sorting

    Args:
        df_columns (Index): the name of the columns

    Returns:
        list: The sorting columns
    """

    # Select the columns to sort on
    selected = [c for c in base if c in df_columns]
    return selected
