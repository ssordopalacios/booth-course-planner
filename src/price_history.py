import os
import re
import numpy as np
import pandas as pd
from . import helper


def rename_columns(string):
    """Renames the columns for simplicity

    Args:
        string (str): The string to transform

    Returns:
        str: The transformed string
    """

    # Clean up the column names
    # TODO: Complete this with a simpler regex statement
    replacements = [
        ["Phase ", "P"],
        ["Price", "Price for"],
        ["Total Enrollment after", "Taken after"],
        ["Seats Available after", "Available after"],
        ["New Students", "NS"],
        [" +", " "],
        [r"(.*) (Price for)", r"\2 \1"],
        [r"(.*) (NS) (P\d)", r"\1 \3 \2"],
    ]
    for pattern, repl in replacements:
        string = re.sub(pattern, repl, string)
    return string


def read_sheet(xls, name):
    """Read a sheet of the prices

    Args:
        xls (XlsFile): The Excel file
        name (str): The name of the sheet

    Returns:
        DataFrame: The cleaned dataframe
    """

    # Starting at the second row
    df = pd.read_excel(xls, name, skiprows=1)

    # Split the instructor names
    # TODO: Do this in a simpler regex statement
    df["Instructor"] = df["Instructor"].str.replace(
        r"\(Katja\)", "", regex=True
    )
    df["Instructor"] = df["Instructor"].str.replace(
        r"(\S+, \S+) ?\;(.+, .+)", r"\1", regex=True
    )
    df[["Last Name", "First Name"]] = df["Instructor"].str.split(
        ", ", expand=True
    )

    # Get the new quarter numbers
    df["Quarter"] = df["Quarter"].map(helper.qtr_to_quarter)

    # Create a course number and section from the original
    df[["Course", "Section"]] = df.Course.str.split("-", expand=True)
    df["Course"] = df["Course"].astype(int)
    df["Section"] = df["Section"].astype(int)
    df["Program"] = df["Section"].map(helper.section_to_program)

    # Drop certain columns
    # TODO: Can probably extract day and time from this
    df = df.drop(columns=["Instructor", "Day and Time"])

    # Cleanup the column names
    # The originals are too long to be readable
    columns_dict = {c: rename_columns(c) for c in list(df.columns)}
    df = df.rename(columns_dict, axis=1)

    # Replace CLO with 0 and convert types to numeric
    df = df.replace("CLO", "0")
    df = df.convert_dtypes()
    cols_obj = list(df.select_dtypes(include=[object]).columns)
    df[cols_obj] = df[cols_obj].apply(pd.to_numeric)
    # TODO: Should we really fillna here?
    df = df.fillna(0)
    df["Total Seats"] = df["Taken after P1"] + df["Available after P1"]

    return df


def main():
    """Reads the price history

    Returns:
        DataFrame: The cleaned price history
    """

    # Load the ExcelFile
    fname = os.path.join("data", "course price history.xls")
    print(f"Reading Price History from {fname}")
    xls = pd.ExcelFile(fname)

    # Read in each sheet of the file
    df = pd.concat([read_sheet(xls, name) for name in xls.sheet_names])

    # Replace missing values that appeared after concatenation
    df = df.fillna(np.nan)

    # Order columns
    column_ordering = helper.column_ordering(df.columns, ["Total Seats"])
    df = df[column_ordering]

    # Sort columns
    column_sorting = helper.column_sorting(df.columns)
    df = df.sort_values(column_sorting)

    return df

