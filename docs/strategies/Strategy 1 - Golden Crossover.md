# Trading Strategies - Crossover

## Overview

The Golden Cross is a bullish phenomenon when the 50-day moving average crosses
above the 200-day moving average. When the market is in a long-term downtrend,
the 50-day moving average is below the 200-day moving average.However, no downtrend
lasts forever. So, when a new uptrend begins, the 50-day moving average must cross
above the 200-day moving average — and that’s known as the Golden Cross.

Because the concept is what matters (which is the short-term trend showing signs of
strength against the long-term downtrend). The moving average is only a tool to
define the trend.

## Indicators

1. 50-Day SMA (Simple Moving Average), represents the short-term trend.
2. 200-Day SMA (Simple Moving Average), represents the long-term trend.

## Buy Signal & Sell Signal

1. Buy Signal, the 50-Day Average Crosses **ABOVE** the 200-Day Moving Average,
   indicating that there may be a bull-market on the horizon.
2. Sell Signal, the 50-Day Average Crosses **BELOW** the 200-Day Moving Average,
   indicating that there may be a bear-market on the horizon.

When the 50-Day SMA crosses **ABOVE** the 200-Day SMA we call it a **Golden Crossover**,
and when the 50-Day SMA crosses **BELOW** the 200-Day SMA we call it a **Death Cross**.

## How to use the Golden Crossover

There are three stages to a golden cross.

- The **first stage** requires that a downtrend eventually bottoms out as selling is depleted.
- In the **second stage**, the shorter moving average forms a crossover up through the larger
  moving average to trigger a breakout and confirmation of trend reversal.
- The **last stage** is the continuing uptrend for the follow through to higher prices. The
  moving averages act as support levels on pullbacks, until they crossover back down at which
  point a death cross may form. The death cross is the opposite of the golden cross as the shorter
  moving average forms a crossover down through the longer moving average.

The most commonly used moving averages are the 50-period and the 200-period moving average. The period
represents a specific time increment. **Generally, larger time periods tend to form stronger lasting breakouts.**
For example, the daily 50-day moving average crossover up through the 200-day moving average on an index like
the S&P 500 is one of the most popular bullish market signals. With a bellwether index, the motto "A rising
tide lifts all boats" applies when a golden cross forms as the buying resonates throughout the index components
and sectors.

## Python Code

```python
# Create an indicator Object.
indicator_client = Indicators(price_data_frame=stock_frame)

# Add the 200-Day simple moving average.
indicator_client.sma(period=200)

# Add the 50-Day simple moving average.
indicator_client.sma(period=200)

# Add a signal to check for.
indicator_client.set_indicator_signal_compare(
    indicator_1='sma',
    indicator_2='sma',
    condition_buy=operator.ge,
    condition_sell=operator.le,
)
```
