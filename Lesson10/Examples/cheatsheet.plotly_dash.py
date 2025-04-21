"""
Plotly Dash Cheatsheet for Interactive Web Dashboards
====================================================

This cheatsheet provides patterns for creating interactive web dashboards
using Plotly Dash with Python and Flask integration.
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from flask import Flask

# Basic Dash App Setup
def basic_dash_app():
    """Basic Dash app setup."""
    # Create a Dash app
    app = dash.Dash(__name__)
    
    # Define the layout
    app.layout = html.Div([
        html.H1("My Dashboard"),
        html.Div("This is a simple Dash app"),
        dcc.Graph(
            id='example-graph',
            figure=px.bar(
                x=["A", "B", "C"],
                y=[1, 3, 2]
            )
        )
    ])
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Dash with Flask Integration
def dash_with_flask():
    """Dash app with Flask integration."""
    # Create a Flask server
    server = Flask(__name__)
    
    # Create a Dash app using the Flask server
    app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')
    
    # Define the Dash layout
    app.layout = html.Div([
        html.H1("Dashboard with Flask Integration"),
        dcc.Graph(
            id='example-graph',
            figure=px.line(
                x=[0, 1, 2, 3, 4],
                y=[0, 1, 4, 9, 16]
            )
        )
    ])
    
    # Define a Flask route
    @server.route('/')
    def index():
        return 'This is the Flask app. Go to <a href="/dashboard/">dashboard</a> to see the Dash app.'
    
    # Run the Flask app
    if __name__ == '__main__':
        server.run(debug=True)
    
    return app, server

# Interactive Components
def interactive_components():
    """Examples of interactive Dash components."""
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        # Dropdown
        html.Label("Dropdown"),
        dcc.Dropdown(
            id='dropdown-example',
            options=[
                {'label': 'Option 1', 'value': 'opt1'},
                {'label': 'Option 2', 'value': 'opt2'},
                {'label': 'Option 3', 'value': 'opt3'}
            ],
            value='opt1'
        ),
        
        # Multi-select Dropdown
        html.Label("Multi-Select Dropdown"),
        dcc.Dropdown(
            id='multi-dropdown',
            options=[
                {'label': 'Option 1', 'value': 'opt1'},
                {'label': 'Option 2', 'value': 'opt2'},
                {'label': 'Option 3', 'value': 'opt3'}
            ],
            multi=True,
            value=['opt1', 'opt2']
        ),
        
        # Radio Items
        html.Label("Radio Items"),
        dcc.RadioItems(
            id='radio-example',
            options=[
                {'label': 'Option 1', 'value': 'opt1'},
                {'label': 'Option 2', 'value': 'opt2'},
                {'label': 'Option 3', 'value': 'opt3'}
            ],
            value='opt1'
        ),
        
        # Checklist
        html.Label("Checklist"),
        dcc.Checklist(
            id='checklist-example',
            options=[
                {'label': 'Option 1', 'value': 'opt1'},
                {'label': 'Option 2', 'value': 'opt2'},
                {'label': 'Option 3', 'value': 'opt3'}
            ],
            value=['opt1', 'opt3']
        ),
        
        # Slider
        html.Label("Slider"),
        dcc.Slider(
            id='slider-example',
            min=0,
            max=10,
            step=1,
            value=5,
            marks={i: str(i) for i in range(11)}
        ),
        
        # Range Slider
        html.Label("Range Slider"),
        dcc.RangeSlider(
            id='range-slider-example',
            min=0,
            max=10,
            step=1,
            value=[2, 7],
            marks={i: str(i) for i in range(11)}
        ),
        
        # Input
        html.Label("Input"),
        dcc.Input(
            id='input-example',
            type='text',
            value='Initial value'
        ),
        
        # Date Picker
        html.Label("Date Picker"),
        dcc.DatePickerSingle(
            id='date-picker-example',
            date=pd.Timestamp('2023-01-01').date()
        ),
        
        # Date Range Picker
        html.Label("Date Range Picker"),
        dcc.DatePickerRange(
            id='date-range-example',
            start_date=pd.Timestamp('2023-01-01').date(),
            end_date=pd.Timestamp('2023-01-31').date()
        ),
        
        # Tabs
        html.Label("Tabs"),
        dcc.Tabs(
            id='tabs-example',
            value='tab1',
            children=[
                dcc.Tab(label='Tab 1', value='tab1', children=[
                    html.Div("This is the content of Tab 1")
                ]),
                dcc.Tab(label='Tab 2', value='tab2', children=[
                    html.Div("This is the content of Tab 2")
                ])
            ]
        ),
        
        # Output area
        html.Div(id='output-area')
    ])
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Callbacks for Interactivity
def callbacks_example():
    """Examples of Dash callbacks for interactivity."""
    app = dash.Dash(__name__)
    
    # Sample data
    df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'A', 'B', 'C'],
        'Series1': [4, 1, 2, 3, 2, 5],
        'Series2': [2, 4, 5, 1, 3, 6]
    })
    
    app.layout = html.Div([
        html.H1("Interactive Dashboard"),
        
        # Controls
        html.Div([
            html.Label("Select Chart Type:"),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Scatter Plot', 'value': 'scatter'}
                ],
                value='bar'
            ),
            
            html.Label("Select Data Series:"),
            dcc.Dropdown(
                id='data-series',
                options=[
                    {'label': 'Series 1', 'value': 'Series1'},
                    {'label': 'Series 2', 'value': 'Series2'},
                    {'label': 'Both Series', 'value': 'both'}
                ],
                value='Series1'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        # Graph
        html.Div([
            dcc.Graph(id='interactive-graph')
        ], style={'width': '70%', 'display': 'inline-block'})
    ])
    
    # Define callback to update graph based on user input
    @app.callback(
        Output('interactive-graph', 'figure'),
        [Input('chart-type', 'value'),
         Input('data-series', 'value')]
    )
    def update_graph(chart_type, data_series):
        if data_series == 'both':
            if chart_type == 'bar':
                fig = px.bar(df, x='Category', y=['Series1', 'Series2'], barmode='group')
            elif chart_type == 'line':
                fig = px.line(df, x='Category', y=['Series1', 'Series2'])
            else:  # scatter
                fig = px.scatter(df, x='Series1', y='Series2', color='Category', size='Series1')
        else:
            if chart_type == 'bar':
                fig = px.bar(df, x='Category', y=data_series)
            elif chart_type == 'line':
                fig = px.line(df, x='Category', y=data_series)
            else:  # scatter
                fig = px.scatter(df, x='Category', y=data_series, size='Series1')
        
        return fig
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Multiple Inputs and Outputs
def multiple_io_example():
    """Example with multiple inputs and outputs."""
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.Div([
            html.Label("Input A:"),
            dcc.Input(id='input-a', type='number', value=5),
            
            html.Label("Input B:"),
            dcc.Input(id='input-b', type='number', value=10),
            
            html.Button('Calculate', id='calculate-button')
        ]),
        
        html.Div([
            html.Div(id='sum-output'),
            html.Div(id='product-output'),
            html.Div(id='difference-output')
        ])
    ])
    
    @app.callback(
        [Output('sum-output', 'children'),
         Output('product-output', 'children'),
         Output('difference-output', 'children')],
        [Input('calculate-button', 'n_clicks')],
        [State('input-a', 'value'),
         State('input-b', 'value')]
    )
    def update_outputs(n_clicks, a, b):
        if n_clicks is None:
            return "Sum: ", "Product: ", "Difference: "
        
        a = a or 0  # Handle None values
        b = b or 0
        
        return f"Sum: {a + b}", f"Product: {a * b}", f"Difference: {a - b}"
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Pattern Matching Callbacks
def pattern_matching_callbacks():
    """Example of pattern matching callbacks for dynamic content."""
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    
    app.layout = html.Div([
        html.Button("Add Chart", id="add-chart", n_clicks=0),
        html.Div(id="chart-container", children=[])
    ])
    
    @app.callback(
        Output("chart-container", "children"),
        [Input("add-chart", "n_clicks")],
        [State("chart-container", "children")]
    )
    def add_chart(n_clicks, children):
        if n_clicks > 0:
            new_child = html.Div([
                dcc.Graph(
                    id={"type": "dynamic-graph", "index": n_clicks},
                    figure=px.line(
                        x=np.arange(10),
                        y=np.random.randn(10).cumsum()
                    )
                ),
                html.Button(
                    "Remove",
                    id={"type": "remove-chart", "index": n_clicks}
                )
            ])
            children.append(new_child)
        return children
    
    @app.callback(
        Output({"type": "dynamic-graph", "index": dash.dependencies.MATCH}, "figure"),
        [Input({"type": "remove-chart", "index": dash.dependencies.MATCH}, "n_clicks")]
    )
    def update_chart(n_clicks):
        if n_clicks:
            # Return an empty figure to "remove" it
            return {}
        # This is needed to initialize the callback, but won't actually be used
        return px.line(x=np.arange(10), y=np.random.randn(10).cumsum())
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Real-time Data Updates
def real_time_updates():
    """Example of real-time data updates in Dash."""
    app = dash.Dash(__name__)
    
    # Initial data
    df = pd.DataFrame({
        'time': pd.date_range(start='2023-01-01', periods=10, freq='1min'),
        'value': np.random.randn(10).cumsum()
    })
    
    app.layout = html.Div([
        html.H1("Real-time Data Dashboard"),
        
        dcc.Graph(id='live-graph'),
        
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds (1 second)
            n_intervals=0
        )
    ])
    
    @app.callback(
        Output('live-graph', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_graph_live(n):
        # Add new data point
        new_time = df['time'].iloc[-1] + pd.Timedelta(minutes=1)
        new_value = df['value'].iloc[-1] + np.random.randn()
        
        # Append to dataframe
        new_row = pd.DataFrame({'time': [new_time], 'value': [new_value]})
        global df
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Keep only the last 20 data points
        if len(df) > 20:
            df = df.iloc[-20:]
        
        # Create the figure
        fig = px.line(df, x='time', y='value', title='Live Data Feed')
        
        # Update layout for a more real-time feel
        fig.update_layout(
            xaxis=dict(range=[df['time'].min(), df['time'].max()]),
            yaxis=dict(range=[df['value'].min() - 1, df['value'].max() + 1]),
            transition_duration=500
        )
        
        return fig
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Advanced Layout with Bootstrap
def bootstrap_layout():
    """Example of using Bootstrap components for layout."""
    # Need to install dash-bootstrap-components
    import dash_bootstrap_components as dbc
    
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    # Create a navbar
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Page 1", href="#"),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="My Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
    )
    
    # Create cards for dashboard
    card1 = dbc.Card(
        [
            dbc.CardHeader("Chart 1"),
            dbc.CardBody(
                [
                    dcc.Graph(
                        figure=px.bar(
                            x=["A", "B", "C"],
                            y=[3, 1, 2]
                        )
                    )
                ]
            ),
        ]
    )
    
    card2 = dbc.Card(
        [
            dbc.CardHeader("Chart 2"),
            dbc.CardBody(
                [
                    dcc.Graph(
                        figure=px.line(
                            x=[0, 1, 2, 3, 4],
                            y=[0, 1, 4, 9, 16]
                        )
                    )
                ]
            ),
        ]
    )
    
    # Layout with Bootstrap grid
    app.layout = html.Div([
        navbar,
        dbc.Container([
            html.H1("Dashboard with Bootstrap", className="mt-4"),
            html.Hr(),
            dbc.Row([
                dbc.Col(card1, width=6),
                dbc.Col(card2, width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3("Controls", className="mt-4"),
                    dbc.Form([
                        dbc.FormGroup([
                            dbc.Label("Select Option"),
                            dcc.Dropdown(
                                id="dropdown",
                                options=[
                                    {"label": "Option 1", "value": "1"},
                                    {"label": "Option 2", "value": "2"},
                                ],
                                value="1",
                            ),
                        ]),
                        dbc.FormGroup([
                            dbc.Label("Range"),
                            dcc.RangeSlider(
                                id="range-slider",
                                min=0,
                                max=10,
                                step=1,
                                value=[3, 7],
                                marks={i: str(i) for i in range(11)},
                            ),
                        ]),
                        dbc.Button("Submit", color="primary"),
                    ]),
                ], width=12),
            ]),
        ], fluid=True),
    ])
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Example of a Complete Dashboard
def complete_dashboard_example():
    """Example of a complete dashboard with multiple components."""
    app = dash.Dash(__name__)
    
    # Sample data
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=30, freq='D')
    df = pd.DataFrame({
        'date': dates,
        'sales': np.random.randint(100, 1000, size=30),
        'customers': np.random.randint(10, 100, size=30),
        'category': np.random.choice(['A', 'B', 'C'], size=30)
    })
    
    # Create layout
    app.layout = html.Div([
        # Header
        html.Div([
            html.H1("Sales Dashboard", style={'text-align': 'center'}),
            html.P("Interactive dashboard showing sales data", style={'text-align': 'center'})
        ]),
        
        # Filters
        html.Div([
            html.Div([
                html.Label("Date Range:"),
                dcc.DatePickerRange(
                    id='date-range',
                    start_date=df['date'].min(),
                    end_date=df['date'].max(),
                    display_format='YYYY-MM-DD'
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Category:"),
                dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
                    multi=True,
                    value=df['category'].unique()
                )
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'padding': '10px'}),
        
        # KPI Cards
        html.Div([
            html.Div([
                html.H4("Total Sales"),
                html.H2(id='total-sales')
            ], style={'width': '30%', 'display': 'inline-block', 'text-align': 'center', 
                      'box-shadow': '0px 0px 5px #ccc', 'padding': '10px', 'margin': '5px'}),
            
            html.Div([
                html.H4("Total Customers"),
                html.H2(id='total-customers')
            ], style={'width': '30%', 'display': 'inline-block', 'text-align': 'center', 
                      'box-shadow': '0px 0px 5px #ccc', 'padding': '10px', 'margin': '5px'}),
            
            html.Div([
                html.H4("Avg. Sale per Customer"),
                html.H2(id='avg-sale')
            ], style={'width': '30%', 'display': 'inline-block', 'text-align': 'center', 
                      'box-shadow': '0px 0px 5px #ccc', 'padding': '10px', 'margin': '5px'})
        ], style={'padding': '10px', 'display': 'flex', 'justify-content': 'space-between'}),
        
        # Charts
        html.Div([
            html.Div([
                dcc.Graph(id='sales-trend')
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='category-pie')
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='sales-vs-customers')
        ], style={'padding': '10px'}),
        
        # Data Table
        html.Div([
            html.H3("Data Table"),
            dash.dash_table.DataTable(
                id='data-table',
                columns=[
                    {'name': 'Date', 'id': 'date'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Sales', 'id': 'sales'},
                    {'name': 'Customers', 'id': 'customers'}
                ],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ], style={'padding': '10px'})
    ])
    
    # Define callbacks
    @app.callback(
        [Output('total-sales', 'children'),
         Output('total-customers', 'children'),
         Output('avg-sale', 'children'),
         Output('sales-trend', 'figure'),
         Output('category-pie', 'figure'),
         Output('sales-vs-customers', 'figure'),
         Output('data-table', 'data')],
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('category-filter', 'value')]
    )
    def update_dashboard(start_date, end_date, categories):
        # Filter data
        filtered_df = df[
            (df['date'] >= start_date) &
            (df['date'] <= end_date) &
            (df['category'].isin(categories))
        ]
        
        # Calculate KPIs
        total_sales = filtered_df['sales'].sum()
        total_customers = filtered_df['customers'].sum()
        avg_sale = total_sales / total_customers if total_customers > 0 else 0
        
        # Create charts
        sales_trend_fig = px.line(
            filtered_df, 
            x='date', 
            y='sales',
            title='Sales Trend',
            color='category'
        )
        
        category_pie_fig = px.pie(
            filtered_df.groupby('category').sum().reset_index(),
            values='sales',
            names='category',
            title='Sales by Category'
        )
        
        sales_vs_customers_fig = px.scatter(
            filtered_df,
            x='customers',
            y='sales',
            color='category',
            size='sales',
            title='Sales vs Customers',
            trendline='ols'
        )
        
        # Format data for table
        table_data = filtered_df.sort_values('date', ascending=False).to_dict('records')
        for record in table_data:
            record['date'] = record['date'].strftime('%Y-%m-%d')
        
        return (
            f"${total_sales:,.0f}",
            f"{total_customers:,.0f}",
            f"${avg_sale:.2f}",
            sales_trend_fig,
            category_pie_fig,
            sales_vs_customers_fig,
            table_data
        )
    
    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
    
    return app

# Example usage
if __name__ == "__main__":
    print("This is a cheatsheet for Plotly Dash. Import the functions to use them.")
