def is_recent_trade(trade, time_expression):
    if trade.timestamp >= time_expression:
        return True
    return False


def find_recent_trades(trades, time_expression):
    return filter(lambda trade: is_recent_trade(trade, time_expression),
                  trades)


def convert_to_pounds(value):
    """
    This function converts a value to a
    :param value: numeric value - integer, float
    :return: string in '£nn.nn' format, e.g. "£30.44"
    """
    return f'£{value:.2f}'


def convert_to_percent(value):
    """
    This function converts a value to percentage
    :param value: float
    :return: string in 'nn.nn%' format
    """
    return f'{value*100}%'
