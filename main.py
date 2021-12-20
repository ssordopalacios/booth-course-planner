import os
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

    # Read the course schedule
    df = booth_schedule.main()

    # Create the degree/conc requirements and merge
    courses = df["Course"].unique()
    reqs = requirements.main(courses)
    df = df.merge(reqs, on="Course")

    # Read the price history, summarize, and merge
    prices = price_history.main()
    prices_group_vars = ["Course", "Quarter", "Program"]
    prices = helper.summarize(prices, prices_group_vars)
    df = df.merge(prices, on=prices_group_vars, how="left")

    # Read the course evaluations, summarize, merge
    evals = course_evals.main()
    evals_group_vars = ["Course", "Last Name"]
    evals = helper.summarize(evals, evals_group_vars)
    df = df.merge(evals, on=evals_group_vars, how="left")

    return df


if __name__ == "__main__":

    df = main()
    fname = os.path.join("output", "booth_course_planner.csv")
    print(f"Saved course planner to {fname}")
    df.to_csv(fname, index=False)
