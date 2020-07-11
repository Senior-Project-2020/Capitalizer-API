
def stock_suggestions(prices, prices_before, sellThreshold = -0.05, buyThreshold = 0.05):
    """
    Objects in the list prices and prices_before should be related by index.
    Calulates the percent price change from prices_before's actual_closing_price and prices' predicted_closing_price. 
    Suggests to either 'buy', 'sell', or 'hold' each stock in 'prices' based on the percent price change.
    If the change is less than sellThreshold, then the suggestion is 'sell'.
    If the change is greater than buyThreshold, then the suggestion is 'buy'.
    If the change is between the sell and buy thresholds, then the suggestion is 'hold'.
    If there is no predicted_closing_price for the given price object, then the suggestion is 'unknown'.
    
    prices - Either a Django QuerySet or a python list of api.models.StockPrice objects
    prices_before - Either a Django QuerySet or a python list of api.models.StockPrice objects
    sellThreshold - A percent value as a decimal.
    buyThreshold - A percent value as a decimal.
    """
    suggestions = []
    if (len(prices) != len(prices_before)):
        return None

    for i in range(len(prices)):
        stockSymbol = prices[i].stock.symbol

        # Make sure there is data in both fields
        if prices[i].predicted_closing_price == None or prices_before[i].actual_closing_price == None:
            suggestions.append({'stock': stockSymbol, 'action': 'unknown', 'percent_change': None})
            continue

        # Calculate percent change between previous day's actual closing and today's predicted
        before_closing = prices_before[i].actual_closing_price
        predicted_closing = prices[i].predicted_closing_price
        percentchange = (predicted_closing - before_closing) / before_closing

        if percentchange > buyThreshold:
            action = 'buy'
        elif percentchange < sellThreshold:
            action = 'sell'
        else:
            action = 'hold'

        suggestions.append({'stock': stockSymbol, 'action': action, 'percent_change': percentchange})
    return suggestions
