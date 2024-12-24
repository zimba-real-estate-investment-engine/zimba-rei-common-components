from app.schemas.MortgageSchema import MortgageSchema


class Mortgage(MortgageSchema):

    def calculate_amortization_schedule(self):
        self.am
