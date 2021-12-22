from abc import ABC, abstractmethod


class AreaOfStudy(ABC):
    def __init__(self, name, offerings):
        self.name = name
        self.offerings = {k: False for k in offerings}

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

    def satisfies(self, course):
        if course in self.offerings:
            return True
        else:
            return False

    def take(self, course):
        if course in self.offerings:
            if self.offerings[course] is True:
                raise ValueError(
                    f"Cannot retake {course} for {self.name} requirement"
                )
            else:
                self.offerings[course] = True
                return True
        else:
            return False


class DegreeRequirement(AreaOfStudy, ABC):
    def __init__(self, name, offerings):
        super().__init__(name, offerings)

    @property
    def completed(self):
        return any(self.offerings.values())


class FinancialAccounting(DegreeRequirement):
    def __init__(self):
        offerings = [
            30000,
            30116,
            30117,
            30120,
            30130,
            30131,
        ]
        super().__init__("Financial Accounting", offerings)


class Microeconomics(DegreeRequirement):
    def __init__(self):
        offerings = [
            33001,
            33002,
            33101,
            30100,
            30200,
        ]
        super().__init__("Microeconomics", offerings)


class InternationalBusiness(AreaOfStudy):
    def __init__(self):
        offerings = [
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
        super().__init__("International Business", offerings)

    @property
    def completed(self):
        # At least one must be 33501 or 33502.
        return any([self.offerings[33501], self.offerings[33502]]) and (
            sum(self.offerings.values()) >= 3
        )


if __name__ == "__main__":

    fa = FinancialAccounting()
    print(fa)
    fa.take(30000)
    print(fa)

    ib = InternationalBusiness()
    ib.take(30131)
    ib.take(33520)
    ib.take(35213)
    print(ib)
    ib.take(33502)
    print(ib)
