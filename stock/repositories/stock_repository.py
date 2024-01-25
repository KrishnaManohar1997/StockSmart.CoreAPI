from django.db.models import Q
from stock.models import Stock


class StockRepository:
    def get_stocks_by_name_or_symbol_search(self, stock_name: str):
        stock_name = stock_name.upper()
        company_name = stock_name.title()
        return Stock.objects.filter(
            Q(name__contains=company_name) | Q(symbol__contains=stock_name)
        )

    def get_stock_by_symbol(self, stock_symbol: str):
        return Stock.objects.get(symbol=stock_symbol)

    def get_stock_by_id(self, stock_id: str):
        return Stock.objects.get(id=stock_id)

    def get_stock_mention_posts(self, stock, blocked_by_user_ids: list):
        return (
            stock.post_mentions.exclude(created_by_user_id__in=blocked_by_user_ids)
            .prefetch_related("post", "post__created_by_user")
            .order_by("-created_at")
        )

    def get_stocks_by_symbols(self, stock_symbols: list):
        return Stock.objects.filter(symbol__in=stock_symbols)

    def get_stocks_by_ids(self, stock_ids: list):
        return Stock.objects.filter(id__in=stock_ids)

    def get_all_stocks(self):
        return Stock.objects.all()
