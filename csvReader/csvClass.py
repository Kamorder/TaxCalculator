from dataclasses import dataclass
@dataclass
class csvRow:
    card: str
    date: str
    description:str
    cost: float

    def __str__(self):
        return f"card:{self.card}, date:{self.date}, description:{self.description}, cost:{self.cost}\n"
    