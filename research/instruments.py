"""Contract specs for the instruments in scope.

Point value = $ per 1.0 price point. Tick size = minimum price increment.
Verify against the exchange/broker spec before any dollar-based result is trusted.
"""

INSTRUMENTS = {
    "NQ":  {"name": "E-mini Nasdaq-100",   "tick_size": 0.25, "point_value": 20.0},
    "MNQ": {"name": "Micro E-mini Nasdaq", "tick_size": 0.25, "point_value": 2.0},
    "ES":  {"name": "E-mini S&P 500",      "tick_size": 0.25, "point_value": 50.0},
    "MES": {"name": "Micro E-mini S&P",    "tick_size": 0.25, "point_value": 5.0},
    "GC":  {"name": "Gold (100 oz)",       "tick_size": 0.10, "point_value": 100.0},
    "MGC": {"name": "Micro Gold (10 oz)",  "tick_size": 0.10, "point_value": 10.0},
}
