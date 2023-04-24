from stock.models import StockStatistics


def get_stock_statistics_map(date_min, date_max):
    stock_statistics = StockStatistics.objects.filter(createdAt__lt=date_max, createdAt__gt=date_min).all()
    ss_map = {}
    for ss in stock_statistics:
        ss_map[ss.code] = ss

    return ss_map
