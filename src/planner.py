import os
from . import requirements


class AreaOfStudy:
    def __init__(self, name, n_required, offerings):
        self.name = name
        self.offerings = offerings
        self.n_required = n_required
        self._taken = []

    @classmethod
    def degree(cls, name):
        fname = os.path.join("data", "degree_requirements.txt")
        req_dict = requirements.read(fname)
        if name not in req_dict:
            raise KeyError(f"{name} is not a degree requirement")
        else:
            return cls(name, 1, req_dict[name])

    def __str__(self):
        return f"{self.name}: {len(self)}/{self.n_required} completed"

    def __len__(self):
        return len(self._taken)

    def __contains__(self, key):
        return key in self._taken

    @property
    def completed(self):
        return len(self) == self.n_required

    def satisfies(self, cid):
        if cid in self.offerings:
            return True
        else:
            return False

    def take(self, cid):
        if cid in self:
            raise ValueError(f"Cannot retake {cid} for {self.name} requirement")
        if self.completed:
            return False
        if self.satisfies(cid):
            self._taken.append(cid)
            return True
        else:
            return False
