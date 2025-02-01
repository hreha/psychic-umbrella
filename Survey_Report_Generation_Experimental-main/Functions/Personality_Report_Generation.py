# plot out the results
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def personality_report_generation(test_taker_df, name, item_number):
    """Code to generate the personality reports for each test taker. 

    Args:
        test_taker_df (list): dataframes for personality scores for each test taker.
        name (string): Full name of each test taker.
        item_number (numeric): Number of personality items (120 or 300).

    Returns:
        fig (figure): plotly figure for the generated report
    """
    #name = 'Jason Hreha'
    personality_score_total = 5 * item_number
    dimension_data_list = {}
    for dimension in test_taker_df['Dimension'].dropna().unique():
        dimension_data_dimension = test_taker_df[test_taker_df['Facet'].str.contains(dimension, na = False)]
        dimension_data_facet = test_taker_df[test_taker_df['Dimension'].str.contains(dimension, na = False)]
        dimension_data_list[dimension] = pd.concat([dimension_data_dimension, dimension_data_facet])

    fig = make_subplots(rows = 5, cols = 1, shared_xaxes = True, shared_yaxes = False, vertical_spacing = 0.02)
    # Openness
    fig.append_trace(go.Bar(
                x=dimension_data_list['Openness'].loc[:, name],
                y=['<b>Openness</b>'] + dimension_data_list['Openness'].reset_index().loc[1:, 'Facet'].tolist(),
                orientation='h', text = dimension_data_list['Openness'].loc[:, name], 
                textposition = 'outside', textfont_size = 9, 
                marker = dict(color = 'LightSkyBlue', 
                            opacity = [value/max(dimension_data_list['Openness'].loc[:, name]) for value in dimension_data_list['Openness'].loc[:, name]])
                ), 1, 1)
    # Conscientiousness
    fig.append_trace(go.Bar(
                x=dimension_data_list['Conscientiousness'].loc[:, name],
                y=['<b>Conscientiousness</b>'] + dimension_data_list['Conscientiousness'].reset_index().loc[1:, 'Facet'].tolist(),
                orientation='h', text = dimension_data_list['Conscientiousness'].loc[:, name], 
                textposition = 'outside', textfont_size = 9, 
                marker = dict(color = 'DarkOrange', 
                            opacity = [value/max(dimension_data_list['Conscientiousness'].loc[:, name]) for value in dimension_data_list['Conscientiousness'].loc[:, name]])
                ), 2, 1)
    # Extroversion
    fig.append_trace(go.Bar(
                x=dimension_data_list['Extroversion'].loc[:, name],
                y=['<b>Extroversion</b>'] + dimension_data_list['Extroversion'].loc[1:, 'Facet'].reset_index().loc[1:, 'Facet'].tolist(),
                orientation='h', text = dimension_data_list['Extroversion'].loc[:, name], 
                textposition = 'outside', textfont_size = 9, 
                marker = dict(color = 'IndianRed', 
                            opacity = [value/max(dimension_data_list['Extroversion'].loc[:, name]) for value in dimension_data_list['Extroversion'].loc[:, name]])
                ), 3, 1)
    # Agreeableness
    fig.append_trace(go.Bar(
                x=dimension_data_list['Agreeableness'].loc[:, name],
                y=['<b>Agreeableness</b>'] + dimension_data_list['Agreeableness'].loc[:, 'Facet'].reset_index().loc[1:, 'Facet'].tolist(),
                orientation='h', text = dimension_data_list['Agreeableness'].loc[:, name], 
                textposition = 'outside', textfont_size = 9, 
                marker = dict(color = 'lightseagreen', 
                            opacity = [value/max(dimension_data_list['Agreeableness'].loc[:, name]) for value in dimension_data_list['Agreeableness'].loc[:, name]])
                ), 4, 1)
    # Neuroticism
    fig.append_trace(go.Bar(
                x=dimension_data_list['Neuroticism'].loc[:, name],
                y=['<b>Neuroticism</b>'] + dimension_data_list['Neuroticism'].loc[:, 'Facet'].reset_index().loc[1:, 'Facet'].tolist(),
                orientation='h', text = dimension_data_list['Neuroticism'].loc[:, name], 
                textposition = 'outside', textfont_size = 9, 
                marker = dict(color = 'MediumPurple', 
                            opacity = [value/max(dimension_data_list['Neuroticism'].loc[:, name]) for value in dimension_data_list['Neuroticism'].loc[:, name]])
                ), 5, 1)

    # convert Facet column to row inde for easier reference
    individual_data = test_taker_df.set_index('Facet', inplace = False)
    fig.update_layout(
        autosize = True,
        height = 1200,  
        title = dict(
            text = f"Personality Report <br><sub><b>{name}</b></sub> <br><sub>{individual_data.loc['Email address'].iloc[0]}</sub>",
            y = 0.95,
            yanchor = 'top', 
            font = dict(size = 15)),  # title font size
        font = dict(size = 9), # yaxis font size
        yaxis = dict(autorange="reversed", showgrid = False, type = 'category'), 
        yaxis2 = dict(autorange="reversed", showgrid = False, type = 'category'), 
        yaxis3 = dict(autorange="reversed", showgrid = False, type = 'category'), 
        yaxis4 = dict(autorange="reversed", showgrid = False, type = 'category'), 
        yaxis5 = dict(autorange="reversed", showgrid = False, type = 'category'), 
        xaxis5 = dict(showgrid = False, visible = False),
        margin = dict(t = 200, l = 10, r = 20, b = 30), 
        plot_bgcolor = 'rgba(0, 0, 0, 0)', 
        showlegend = False
        ) 
    fig.add_annotation(
        text = f"DATE/TIME OF COMPLETION<br><b>{individual_data.loc['Completion Time'].iloc[0]}</b>" + 
                f"<br><br> TIME TO COMPLETION <br><b>{individual_data.loc['Response Time'].iloc[0]}</b>" +
                f"<br><br>PERSONALITY SCORE<br><b>{individual_data.loc['Personality Score'].iloc[0]} (Out of {personality_score_total} Total)</b>" + 
                f"<br><br>SOCIAL DESIRABILITY SCORE<br><b>{individual_data.loc['Social Desirability Score'].iloc[0]}</b>" +
                f"<br><br>VARIATION SCORE<br><b>{individual_data.loc['Response Variance'].iloc[0]}</b>", 
                x = 0.8, y = 1.08, xref='paper', yref='paper', 
                font = dict(size = 9)
                )
    fig.update_annotations(align = 'right')
    return fig

