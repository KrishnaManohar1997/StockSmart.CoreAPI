from smallcase.models import Smallcase


class SmallcaseRepository:
    def get_smallcase_by_symbol(self, symbol):
        return Smallcase.objects.get(symbol=symbol)

    def get_smallcase_by_id(self, smallcase_id):
        return Smallcase.objects.get(id=smallcase_id)

    def get_all_smallcases(self):
        return Smallcase.objects.all()

    def get_smallcases_by_symbols(self, symbols: list):
        return Smallcase.objects.filter(symbol__in=symbols)
