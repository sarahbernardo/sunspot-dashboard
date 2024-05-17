"""
Sarah Bernardo
Prof.  Rachlin | DS 3500
10 Feb 2023
Homework 2

This file contains the functions needed to create a double line graph with a smoothed
line chart (made from a rolling average) overlayed over a standard line graph of the dataframe
"""

import plotly.graph_objects as go

def narrow_df(orig_df, start_yr, end_yr):
    """
    Narrows down df of entire CSV to df of information about user-requested time period
    :param orig_df: full dataframe from CSV
    :param start_yr: first year of user-requested interval (int)
    :param end_yr: last year of user-requested interval (int)
    :return: narrowed_df: dataframe for user-requested time period
    """
    # locate row of beginning yr
    beg_yr = orig_df.index[orig_df['Year'] == start_yr].tolist()
    beg_idx = beg_yr[0]

    # locate row of ending yr
    end_yr = orig_df.index[orig_df['Year'] == end_yr].tolist()
    end_idx = end_yr[-1]

    # create narrowed down df
    narrowed_df = orig_df.loc[beg_idx:end_idx]
    return narrowed_df


def smooth_data(narrowed_df, smoothed_df, smooth_val):
    """
    Creates smoothed data with windows of a user-requested integer
    :param narrowed_df: dataframe for user-requested time period
    :param smoothed_df: copy of original dataframe from full CSV file
    :param smooth_val: user-requested value for smoothing window (int)
    :return: smoothed_df: dataframe for user-requested time period with column of rolling means
    """

    # smooth out values
    smoothed_df["Smooth Val"] = narrowed_df.Mon_Total.rolling(window=smooth_val, axis=0, center=True).mean()
    smoothed_df = smoothed_df.dropna().reset_index()

    return smoothed_df


def double_line_graph(narrowed_df, smoothed_df):
    """
    creates a time-series line graph with an overlay of a similar time-series line graph with smoothed data
    :param narrowed_df: dataframe for user-requested time period
    :param smoothed_df: dataframe for user-requested time period with column of rolling means
    :return: fig: figure of double line graph
    """
    # add normal graph
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=narrowed_df["Date Fraction"], y=narrowed_df["Mon_Total"], mode="lines", name="Monthly Total"))

    # add smoothed graph
    fig.add_trace(
        go.Scatter(x=smoothed_df["Date Fraction"], y=smoothed_df["Smooth Val"], mode="lines", name="Smoothed Total"))

    # add labels
    fig.update_layout(xaxis_title="Time (Years)",
                      yaxis_title="Sunspots (Monthly Total)",
                      title="Monthly Sunspot Totals")

    return fig