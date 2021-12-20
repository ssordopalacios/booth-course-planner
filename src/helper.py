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


def qtr_to_quarter(qtr):
    """Transform a quarter into the standard form

    Args:
        qtr (str): The initial quarter

    Returns:
        str: The standardized quarter
    """

    qtr_dict = {
        "AUT": "1-Autumn",
        "Autumn": "1-Autumn",
        "WIN": "2-Winter",
        "Winter": "2-Winter",
        "SPR": "3-Spring",
        "Spring": "3-Spring",
        "SUM": "4-Summer",
        "Summer": "4-Summer",
    }
    return qtr_dict[qtr]


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

    # Identify columns to drop
    drop_columns = [c for c in base if c in df.columns and c not in group_vars]
    df = df.drop(columns=drop_columns)

    # Group by the specified values
    df = df.groupby(group_vars, as_index=False).median()
    return df


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
