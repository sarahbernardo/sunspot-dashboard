"""
Sarah Bernardo
Prof.  Rachlin | DS 3500
10 Feb 2023
Homework 2

This file constructs the dashboard app using Dash. The dashboard contains a monthly total
sunspot double-line time-series graph, a cycle variability scatter plot, and three real
time images of the sun. It allows for the user to select time periods and parameters for the graphs.
It contains the function to create the cycle variability scatter plot and incorporates functions from
monthly_sunspot_graph.py.
"""

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from monthly_sunspot_graph import narrow_df, smooth_data, double_line_graph


def create_df(infile):
    """
    Reads CSV file and turns it into two dataframes
    :param infile: name of CSV file
    :return: data: dataframe
             smooth_dataframe: a duplicate dataframe of "data" to set up for data smoothing in first graph
    """
    # read csv
    data = pd.read_csv(infile,
                       delimiter=";",
                       names=["Year", "Month", "Date Fraction", "Mon_Total", "Mean SD", "Num Obs", "Marker"])

    # create dataframe for smoothing
    smooth_dataframe = data.copy()
    smooth_dataframe["Smooth Val"] = None
    smooth_dataframe["Smooth Val"] = data.Month.rolling(window=1, axis=0, center=True).mean()

    return data, smooth_dataframe


# create universal dfs from csv
df, smooth_df = create_df('monthly_sunspot.csv')


def main():
    app = Dash(__name__)

    # define the layout
    app.layout = html.Div([

        html.Div([
            # page title
            html.H1("Sunspot Dashboard",
                    style={'color': 'purple', 'text-align': 'center'}),

            # monthly averages graph
            html.H2("How Have Monthly Sunspot Totals Looked in the Past?",
                    style={'color': 'purple', 'text-align': 'center'}),
            # display monthly sunspot average graph
            dcc.Graph(id="time-series-chart"),

            # range slider for time period
            html.H3("Adjust Desired Time Period: ",
                    style={'color': 'blue'}),
            dcc.RangeSlider(id="time",
                            min=df["Year"].min(),
                            max=df["Year"].max(),
                            step=1,
                            marks={1750: '1750', 1800: '1800', 1850: '1850',
                                   1900: '1900', 1950: '1950', 2000: '2000', 2023: '2023'},
                            value=[1750, 2023],
                            tooltip={"placement": "bottom", "always_visible": True}),

            # slider for smoothing data
            html.H3("Adjust Desired Number of Months to Smooth: ",
                    style={'color': 'red'}),
            dcc.Slider(id='smoothing',
                       min=1,
                       max=24,
                       step=1,
                       marks={1: '1', 6: '6', 12: '12', 18: '18', 24: '24'},
                       value=12,
                       tooltip={"placement": "bottom", "always_visible": True},
                       included=False),

            # cycle variability graph
            html.H2("What is the Variability of the Sunspot Cycle?",
                    style={'color': 'purple', 'text-align': 'center'}),
            # display graph
            dcc.Graph(id="cycle_var_graph"),

            # slider for tuning cycle length
            html.H3("Adjust Desired Number of Years for Cycle Period: ",
                    style={'color': 'green'}),
            dcc.Slider(id='cycle_tuner',
                       min=1,
                       max=14,
                       marks={1: '1', 7: '7', 14: '14'},
                       value=11,
                       tooltip={"placement": "bottom", "always_visible": True},
                       included=False),

            # first real time image of sun
            html.H2("Real Time Sun Images",
                    style={'color': 'purple', 'text-align': 'center'}),
            html.H3("Hover over each image to see title.",
                    style={'color': 'purple', 'text-align': 'center'}),
            html.Img(
                src="https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg",
                height=400, width=400,
                title="Real Time SDO/HMI Continuum Image",
                style={'display': 'inline-block', 'float': 'left'}
            ),

            # second real time image of sun
            html.Img(
                src="https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg",
                height=400, width=400,
                title="Real Time EIT 171  Image",
                style={'display': 'inline-block', 'float': 'center'}
            ),

            # third real time image of sun
            html.Img(
                src="https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg",
                height=400, width=400,
                title="Real Time SDO HMI Magnetogram Image Image",
                style={'display': 'inline-block', 'float': 'right'}
            ),
        ])
    ])

    @app.callback(
        Output("time-series-chart", "figure"),
        Input("time", "value"),
        Input("smoothing", "value")
    )
    def monthly_avg_graph(time, smoothing):
        """
        Creates time-series chart of monthly average sunspot totals
        :param time: list of years whose data user wants to observe
        :param smoothing: smoothing window (int)
        :return: fig: time-series chart with the one smoothed line, one unsmoothed line
        """
        # calculate start and end rows for desired time period
        start_yr = time[0]
        end_yr = time[-1]

        # construct figures
        narrowed = narrow_df(df, start_yr, end_yr)
        smooth = smooth_data(narrowed, smooth_df, smoothing)
        fig = double_line_graph(narrowed, smooth)

        return fig

    @app.callback(
        Output("cycle_var_graph", "figure"),
        Input("cycle_tuner", "value"),
        Input("time", "value"),
    )
    def cycle_var_graph(cycle_tuner, time):
        """
        Creates scatter plot of the number of sunspots at certain times in a multi-year cycle
        :param cycle_tuner: length of cycle period (float)
        :param time: list of years whose data user wants to observe
        :return: fig: a scatter plot
        """
        # calculate start and end rows for desired time period
        start_yr = time[0]
        end_yr = time[-1]

        # calculate modulo of all decimal dates
        mod_df = df[start_yr:end_yr].copy()
        mod_df["Mod Res"] = mod_df["Date Fraction"] % cycle_tuner

        # construct scatter plot
        fig = px.scatter(x=mod_df["Mod Res"], y=mod_df["Mon_Total"], color_discrete_sequence=['green'])
        fig.update_layout(xaxis_title="Time (Years)",
                          yaxis_title="Number of Sunspots",
                          title="Cycle Variability")

        return fig

    app.run_server(debug=True)


main()
