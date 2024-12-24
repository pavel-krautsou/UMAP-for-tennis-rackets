import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from helper_functions import customFormat



#
cols = ['HeadSize',
        'UnStrungWeight',
        'SwingWeight',
        'Balance',
        'Stiffness',
        'BeamWidth1',
        'BeamWidth2',
        'BeamWidth3',
    	'MinStringTension',
        'MaxStringTension',
        'StringOpenness'
       ]

# Load data and set up the scatter plot data
path = '../data/enchanced_data.csv'
df = pd.read_csv(path)
df = df.rename(columns={'StringDensity':'StringOpenness'})
df = df.set_index('Model')
values_df = df[cols]

# Load standardized data
path = '../data/standardized_data.csv'
sd = pd.read_csv(path)
sd = sd.rename(columns={'StringDensity':'StringOpenness'})
sd = sd.set_index(df.index)
sd = sd[cols]

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='brand-dropdown',
            options=[{'label': brand, 'value': brand} for brand in df['Brand'].unique()],
            value=None,
            placeholder="Select a Brand",
            clearable=True,
            style={'width': '45%', 'display': 'inline-block', 'margin-right': '10px'}
        ),
        dcc.Dropdown(
            id='model-dropdown',
            options=[],
            value=None,
            placeholder="Select a Model",
            clearable=True,
            style={'width': '45%', 'display': 'inline-block'}
        )
    ]),
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(df, x="Dim1", y="Dim2", hover_data={'Model': df.index}),

    ),
    dcc.Graph(
        id='heatmap'
    )
])


@app.callback(
    Output('model-dropdown', 'options'),
    Input('brand-dropdown', 'value')
)
def update_model_dropdown(selected_brand):
    if selected_brand is None:
        return [{'label': model, 'value': model} for model in df.index]
    else:
        filtered_models = df[df['Brand'] == selected_brand].index
        return [{'label': model, 'value': model} for model in filtered_models]


# Callback to update the scatter plot based on selected brand and model
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('brand-dropdown', 'value'),
    Input('model-dropdown', 'value')
)
def update_scatter_plot(selected_brand, selected_model):
    if selected_brand:
        df['ChosenBrand'] = (df['Brand'] == selected_brand)
    else:
        df['ChosenBrand'] = False

    # Highlight the selected model if specified
    if selected_model:
        df['ChosenModel'] = (df.index == selected_model).astype(int) + .1
        fig = px.scatter(
            df,
            x="Dim1",
            y="Dim2",
            color='ChosenBrand',
            symbol='ChosenModel',
            size='ChosenModel',
            color_discrete_map={True: 'red', False: 'blue'},
            hover_data={'Model': df.index},
        )
        fig.update_traces(showlegend=False)

    else:
        fig = px.scatter(
            df,
            x="Dim1",
            y="Dim2",
            color='ChosenBrand',
            hover_data={'Model': df.index},
            color_discrete_map={True: 'red', False: 'blue'},
        )
        fig.update_traces(showlegend=False)

    fig.update_layout()
    return fig


# Callback to update the heatmap based on the selected points in the scatterplot
@app.callback(
    Output('heatmap', 'figure'),
    [Input('scatter-plot', 'selectedData')]
)
def update_heatmap(selectedData):
    if selectedData is None or 'points' not in selectedData or len(selectedData['points']) == 0:
        # If no points are selected, show an empty fugure
        return {}
    else:
        # Retrieve the indices of the selected points
        selected_raquets = [point['customdata'][0] for point in selectedData['points']]
        selected_rows = sd.loc[selected_raquets, :]
        text = values_df.loc[selected_raquets, :]
        text = text.map(customFormat)

        # Construct the heatmap
        fig = ff.create_annotated_heatmap(selected_rows.values,
                                          x=list(selected_rows.columns.values),
                                          y=list(selected_rows.index.values),
                                          annotation_text=text.values,
                                          colorscale='Viridis',
                                          showscale=True
                                          )

    return fig


# Run the app
if __name__ == '__main__':

    # Run the app
    app.run_server(debug=False)