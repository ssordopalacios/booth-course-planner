import os
import pandas as pd
from . import helper


def rename_last(names):
    """Renames last names that do not match

    Args:
        names (series): The professor names

    Returns:
        series: The cleaned professor names
    """

    # Store names not matching
    change_dict = {
        "Pagliari Jr.": "Pagliari",
        "Mcgowan": "McGowan",
        "Dube": "Dubé",
        "O'brien": "O'Brien",
    }

    # Replace names
    for k, v in change_dict.items():
        names = names.str.replace(k, v, regex=True)

    return names


def read_historical():
    """Read the historical course evaluations

    Returns:
        DataFrame: The cleaned historical course evaluations
    """

    # Read the historical evaluations
    fname = os.path.join("data", "course_evals.xlsx")
    print(f"Reading Historical Course Evaluations from {fname}")
    df = pd.read_excel(fname)

    # Store program instead of section
    df["Program"] = df["SECT"].map(helper.section_to_program)

    # Expand the name of the quarter
    df["Quarter"] = df["QTR"].map(helper.qtr_to_quarter)
    # Clean up the instructor's name
    # TODO: Do this in a cleaner regex statement
    df["Instructor"] = df["Instructor"].str.replace(
        r"(\S+, \S+) (\(.*\))", r"\1", regex=True
    )
    df[["Last Name", "First Name"]] = df["Instructor"].str.split(
        ", ", expand=True
    )
    # Clean up last names
    df["Last Name"] = rename_last(df["Last Name"])

    # Rename columns
    rename_dict = {
        "YR": "Year",
        "SECT": "Section",
        "ENRL": "Enrollment",
        r"% RESP": "Percent Responses",
        "Q. 1 HRS /WK": "Hours Per Week",
        "Q. 2 CONVEY CLEAR": "Convey Clearly",
        "Q. 3 CONVEY INTRST": "Convey Interesting",
        "Q. 4 USEFUL TOOLS": "Useful Tools",
        "Q. 5 OUT OF COURSE": "Out Of Course",
        "Q. 6 REC COURSE": "Recommend Course",
    }
    df = df.rename(rename_dict, axis=1)

    # Round percent responses
    df["Percent Responses"] = (100 * df["Percent Responses"]).round(0)

    # Remove unwanted columns
    df = df.drop(columns=["QTR", "Instructor"])

    # Order the columns
    column_ordering = helper.column_ordering(df.columns)
    df = df[column_ordering]

    # Sort the columns
    column_sorting = helper.column_sorting(df.columns)
    df = df.sort_values(column_sorting)

    return df


def read_new(fname):
    """Read the course evaluations from BLUE

    Returns:
        DataFrame: The cleaned BLUE evaluations
    """

    # Read the file
    print(f"Reading New Course Evaluations from {fname}")
    df = pd.read_csv(fname)

    # Get the course number
    df[["Department", "Course", "Section"]] = df["Course Title"].str.split(
        " ", expand=True
    )
    df = df[df["Department"] == "BUSN"]
    df["Course"] = df["Course"].astype(int)
    df["Section"] = df["Section"].astype(int)
    df["Program"] = df["Section"].map(helper.section_to_program)

    # Get the year and quarter
    df[["Quarter", "Year"]] = df["Quarter"].str.split(" ", expand=True)
    df["Year"] = df["Year"].astype(int)
    df["Quarter"] = df["Quarter"].map(helper.qtr_to_quarter)

    # Clean up last names
    df["Last Name"] = rename_last(df["Last Name"])

    # Order and rename the columns
    rename_dict = {
        "Courses - LONG_CLASS_TITLE": "Title",
        "Invites": "Enrollment",
        "Resp.": "Responses",
        r"%Resp": "Percent Responses",
        "Q1 Average Number of Hours Per Week Spent in Preparation": "Hours Per Week",
        "Q2 Info Clearly Conveyed": "Convey Clearly",
        "Q3 Info Conveyed In an Interesting Way": "Convey Interesting",
        "Q4 Acquired Useful Tools": "Useful Tools",
        "Q5 Amount Learned from Course": "Out Of Course",
        "Q6 Recommend Course to Others": "Recommend Course",
    }
    df = df.rename(rename_dict, axis=1)

    # Round percent responses
    df["Percent Responses"] = df["Percent Responses"].round(0)
    df[
        [
            "Hours Per Week",
            "Convey Clearly",
            "Convey Interesting",
            "Useful Tools",
            "Out Of Course",
            "Recommend Course",
        ]
    ] = df[
        [
            "Hours Per Week",
            "Convey Clearly",
            "Convey Interesting",
            "Useful Tools",
            "Out Of Course",
            "Recommend Course",
        ]
    ].round(
        1
    )

    # Remove unwanted columns
    df = df.drop(columns=["Course Title", "Department"])

    # Order the columns
    column_ordering = helper.column_ordering(df.columns)
    df = df[column_ordering]

    # Sort the columns
    column_sorting = helper.column_sorting(df.columns)
    df = df.sort_values(column_sorting)
    return df


def main():
    """Read and merge the course evaluations

    Returns:
        DataFrame: The cleaned course evaluations
    """

    # Read the historical files from 2015-2019
    df_historical = read_historical()

    # Read the new files from BLUE
    df_new_mba = read_new(os.path.join("data", "ExportReport_MBA.csv"))

    # Append the two and re-sort
    df = pd.concat([df_historical, df_new_mba])
    column_sorting = helper.column_sorting(df.columns)
    df = df.sort_values(column_sorting)
    return df
