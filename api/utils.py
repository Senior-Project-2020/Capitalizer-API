
def stock_suggestions(prices, sellThreshold = -0.1, buyThreshold = 0.1):
    """
    Suggests to either 'buy', 'sell', or 'hold' each stock in 'prices' based on the percent price change.
    If the change is less than sellThreshold, then the suggestion is 'sell'.
    If the change is greater than buyThreshold, then the suggestion is 'buy'.
    If the change is between the sell and buy thresholds, then the suggestion is 'hold'.
    If there is no predicted_closing_price for the given price object, then the suggestion is 'unknown'.
    
    prices - Either a Django QuerySet or a python list of api.models.StockPrice objects
    sellThreshold - A percent value as a decimal.
    buyThreshold - A percent value as a decimal.
    """
    suggestions = []
    for price in prices:
        stockId = price.stock.id

        if price.predicted_closing_price == None:
            suggestions.append({'stock': stockId, 'action': 'unknown', 'percent_change': None})
            continue

        opening = price.opening_price
        closing = price.predicted_closing_price
        percentchange = (closing - opening) / opening

        if percentchange > buyThreshold:
            action = 'buy'
        elif percentchange < sellThreshold:
            action = 'sell'
        else:
            action = 'hold'

        suggestions.append({'stock': stockId, 'action': action, 'percent_change': percentchange})
    return suggestions
