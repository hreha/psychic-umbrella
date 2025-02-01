import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def personality_report_generation(test_taker_df, name, item_number):
    """
    Generates a Plotly-based personality report for the given test taker.
    
    Args:
        test_taker_df (DataFrame): DataFrame containing personality scores.
        name (str): Full name of the test taker.
        item_number (int): Number of personality items (120 or 300).
        
    Returns:
        fig (Plotly Figure): Generated report figure.
    """
    personality_score_total = 5 * item_number
    dimension_data_list = {}
    for dimension in test_taker_df['Dimension'].dropna().unique():
        dimension_data_dimension = test_taker_df[test_taker_df['Facet'].str.contains(dimension, na=False)]
        dimension_data_facet = test_taker_df[test_taker_df['Dimension'].str.contains(dimension, na=False)]
        dimension_data_list[dimension] = pd.concat([dimension_data_dimension, dimension_data_facet])
    
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    
    # Helper function to compute opacities safely
    def compute_opacities(values):
        max_val = max(values) if max(values) != 0 else 1  # Avoid division by zero
        return [value / max_val for value in values]
    
    # Define dimensions with associated colors and subplot row numbers
    dimensions_info = [
        ('Openness', 'LightSkyBlue', 1),
        ('Conscientiousness', 'DarkOrange', 2),
        ('Extroversion', 'IndianRed', 3),
        ('Agreeableness', 'lightseagreen', 4),
        ('Neuroticism', 'MediumPurple', 5)
    ]
    
    for dim, color, row in dimensions_info:
        if dim not in dimension_data_list:
            continue
        data = dimension_data_list[dim]
        if name not in data.columns:
            continue
        values = data.loc[:, name].tolist()
        opacities = compute_opacities(values)
        # Use the first value for the overall dimension, the rest for facets
        y_labels = [f"<b>{dim}</b>"] + data.reset_index().iloc[1:]['Facet'].tolist()
        fig.add_trace(go.Bar(
            x=values,
            y=y_labels,
            orientation='h',
            text=values,
            textposition='outside',
            textfont_size=9,
            marker=dict(color=color, opacity=opacities)
        ), row, 1)
    
    individual_data = test_taker_df.set_index('Facet')
    title_text = (
        f"Personality Report <br><sub><b>{name}</b></sub> "
        f"<br><sub>{individual_data.loc['Email address'].iloc[0]}</sub>"
    )
    annotation_text = (
        f"DATE/TIME OF COMPLETION<br><b>{individual_data.loc['Completion Time'].iloc[0]}</b>"
        f"<br><br>TIME TO COMPLETION <br><b>{individual_data.loc['Response Time'].iloc[0]}</b>"
        f"<br><br>PERSONALITY SCORE<br><b>{individual_data.loc['Personality Score'].iloc[0]} (Out of {personality_score_total} Total)</b>"
        f"<br><br>SOCIAL DESIRABILITY SCORE<br><b>{individual_data.loc['Social Desirability Score'].iloc[0]}</b>"
        f"<br><br>VARIATION SCORE<br><b>{individual_data.loc['Response Variance'].iloc[0]}</b>"
    )
    
    fig.update_layout(
        autosize=True,
        height=1200,
        title=dict(text=title_text, y=0.95, yanchor='top', font=dict(size=15)),
        font=dict(size=9),
        yaxis=dict(autorange="reversed", showgrid=False, type='category'),
        yaxis2=dict(autorange="reversed", showgrid=False, type='category'),
        yaxis3=dict(autorange="reversed", showgrid=False, type='category'),
        yaxis4=dict(autorange="reversed", showgrid=False, type='category'),
        yaxis5=dict(autorange="reversed", showgrid=False, type='category'),
        xaxis5=dict(showgrid=False, visible=False),
        margin=dict(t=200, l=10, r=20, b=30),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False
    )
    fig.add_annotation(
        text=annotation_text,
        x=0.8, y=1.08, xref='paper', yref='paper',
        font=dict(size=9),
        align='right'
    )
    return fig
