import os
import numpy as np
import pandas as pd


def read(fname):
    """Read a requirements file

    Args:
        fname (str): The name of the file

    Returns:
        dict: The requirements dictionary
    """

    # Load the file
    print(f"Reading Requirements from {fname}")
    dictionary = {}
    with open(fname, "r") as f:
        # Each line contains Area: CourseNum, CourseNum
        # Put this into a dictionary
        for line in f:
            line = line.strip().split(":")
            area = line[0]
            course = [int(x) for x in line[1].split(",")]
            dictionary[area] = course
    return dictionary


def lookup(course, dictionary):
    """Look for a course in the dictionary file

    Args:
        course (int): The course number
        dictionary (dict): The requirements dictionary

    Returns:
        DataFrame: A mapping of which requirements meet it
    """

    # Create a dictionary
    df = {}
    df["Course"] = [course]

    # For each area, see if the course is an option then add to dictionary
    matches = {
        area: [course in offering] for area, offering in dictionary.items()
    }
    df.update(matches)

    # Create a dataframe from dictionary
    df = pd.DataFrame.from_dict(data=df)
    return df


def fill(courses, dictionary):
    """Fill a DataFrame for all the courses

    Args:
        courses (list): The list of courses
        dictionary (dict): The requirements dictionary

    Returns:
        DataFrame: The dataframe for the courses
    """

    # Add the requirements matching
    df = pd.concat([lookup(c, dictionary) for c in courses])

    # Replace with 1 and NaN for nicer viewing in Excel
    df = df.replace(True, 1)
    df = df.replace(False, np.nan)
    return df


def main(courses):
    """Load the requirements file

    Args:
        courses (list): The list of courses

    Returns:
        DataFrame: The dataframe for the courses
    """

    # Read the degree requirements
    fname_degree = os.path.join("data", "degree_requirements.txt")
    dictionary = read(fname_degree)

    # Read the concentration requirements
    fname_conc = os.path.join("data", "concentration_requirements.txt")
    dictionary.update(read(fname_conc))

    # Fill the courses as a dataframe
    df = fill(courses, dictionary)
    return df
