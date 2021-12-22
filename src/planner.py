from abc import ABC, abstractmethod


class AreaOfStudy(ABC):
    def __init__(self, name, courses):
        self.name = name
        self.courses = {k: False for k in courses}

    def __str__(self):
        if self.completed:
            msg = "Complete"
        else:
            msg = "Incomplete"
        return f"{self.name}: {msg}"

    @property
    @abstractmethod
    def completed():
        pass


class FinancialAccounting(AreaOfStudy):
    def __init__(self):
        courses = [
            30000,
            30116,
            30117,
            30120,
            30130,
            30131,
        ]
        super().__init__("Financial Accounting", courses)

    @property
    def completed(self):
        return any(self.courses.values())


class InternationalBusiness(AreaOfStudy):
    def __init__(self):
        courses = [
            30131,
            33402,
            33501,
            33502,
            33503,
            33520,
            33521,
            35210,
            35213,
            35219,
        ]
        super().__init__("Financial Accounting", courses)

    @property
    def completed(self):
        any([self.courses[33501], self.courses[33501]]) and (
            sum(self.courses.values()) > 3
        )

        # At least one must be 33501 or 33502.


if __name__ == "__main__":

    fa = FinancialAccounting()
    print(fa.completed)
    print(fa)

    ib = InternationalBusiness()
    print(fa.completed)
    print(fa)
