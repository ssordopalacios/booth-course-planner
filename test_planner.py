from src.planner import AreaOfStudy

# Create an instance of the econometrics concentration
metrics = AreaOfStudy(
    "Econometrics",
    3,
    [
        41000,
        41100,
        41201,
        41202,
        41203,
        41204,
        41301,
        41901,
        41902,
        41903,
        41910,
        41911,
        41912,
        41913,
        41914,
    ],
)

print(metrics)
metrics.take(23)
print(metrics)
metrics.take(41901)
print(metrics)
metrics.take(41902)
print(metrics)
metrics.take(41903)

# Create an instance of the accounting requirement from the file
accounting = AreaOfStudy.degree("Financial Accounting")
print(accounting)
accounting.take(30000)
print(accounting)
