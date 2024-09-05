from dataclasses import dataclass
@dataclass
class csvRow:
    card: str
    date: str
    description:str
    parsed: str
    cost: float
    def __str__(self):
        return f"card:{self.card}, date:{self.date}, description:{self.description}, parsed:{self.parsed}, cost:{self.cost}\n"
    