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

    # Open up the file
    fname = os.path.join("output", "booth_course_planner.xlsx")
    if os.path.exists(fname):
        os.remove(fname)
    writer = pd.ExcelWriter(fname, engine="xlsxwriter")

    # Read the course schedule
    df = booth_schedule.main()

    # Create the degree/conc requirements and merge
    courses = df["Course"].unique()
    reqs = requirements.main(courses)
    reqs.to_excel(writer, sheet_name="Requirements", index=False)
    df = df.merge(reqs, on="Course")

    # Read the price history, summarize, and merge
    prices = price_history.main()
    prices.to_excel(writer, sheet_name="Price History", index=False)
    prices_group_vars = ["Course", "Program", "Last Name"]
    prices = helper.summarize(prices, prices_group_vars)
    df = df.merge(prices, on=prices_group_vars, how="left")

    # Read the course evaluations, summarize, merge
    evals = course_evals.main()
    evals.to_excel(writer, sheet_name="Course Evaluations", index=False)
    evals_group_vars = ["Course", "Program", "Last Name"]
    evals = helper.summarize(evals, evals_group_vars)
    df = df.merge(evals, on=evals_group_vars, how="left")

    # Save the full df to the excel file
    df.to_excel(writer, sheet_name="Planner", index=False)
    writer.save()
    print(f"Saved course planner to {fname}")
    return df


if __name__ == "__main__":

    df = main()

