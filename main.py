import os
import pandas as pd
from src import (
    helper,
    booth_schedule,
    requirements,
    price_history,
    course_evals,
)


def main():
    """Create a course overview

    Returns:
        DataFrame: The merged course overview information
    """

    # Store the grouping variable
    group_vars = ["Course", "Program", "Last Name"]

    # Set up the file to write to
    fname = os.path.join("output", "booth_course_planner.xlsx")
    if os.path.exists(fname):
        os.remove(fname)
    xls = pd.ExcelWriter(fname)

    # Read the course schedule
    df = booth_schedule.main()

    # Create the degree/conc requirements and merge
    courses = df["Course"].unique()
    reqs = requirements.main(courses)
    reqs.to_excel(xls, "Requirements", index=False)
    df = df.merge(reqs, on="Course")

    # Read the price history, summarize, and merge
    prices = price_history.main()
    prices.to_excel(xls, "Price History", index=False)
    prices = helper.summarize(prices, group_vars)
    df = df.merge(prices, on=group_vars, how="left")

    # Read the course evaluations, summarize, merge
    evals = course_evals.main()
    evals.to_excel(xls, "Course Evaluations", index=False)
    evals = helper.summarize(evals, group_vars)
    df = df.merge(evals, on=group_vars, how="left")

    # Export the file
    df.to_excel(xls, "Planner", index=False)
    xls.close()
    print(f"Saved course planner to {fname}")

    return df


if __name__ == "__main__":

    main()
