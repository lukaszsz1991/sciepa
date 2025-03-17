class Person:
    def __init__(self, name: str):
        self.name = name
        self.expenses = 0
        self.balance = 0
        self.debt = 0

    def __str__(self):
        return f"\n{self.name} zapłacił(a) {self.expenses:.2f} zł.\nPowininien zapłacić: {self.debt:.2f} zł.\nSaldo: {self.balance:.2f} zł."