from dataclasses import dataclass

@dataclass
class csvRow:
    card: str
    date: str
    description:str
    parsed: str
    cost: float
    def __str__(self):
        return f"card:{self.card}, date:{self.date}, description:{self.description}, cost:{self.cost}\n"

@dataclass
class csvDebitRow:
    line: str
    date: str
    description:str
    parsed: str
    cost: float
    def __str__(self):
        return f"line:{self.line}, date:{self.date}, description:{self.description}, cost:{self.cost}\n"