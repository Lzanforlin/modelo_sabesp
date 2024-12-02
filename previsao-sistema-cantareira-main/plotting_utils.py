import plotly.graph_objs as go
import numpy as np
import pandas as pd

# Extraído de: https://github.com/facebook/prophet/blob/main/python/prophet/plot.py
def plot_plotly(m, fcst, uncertainty=True, plot_cap=True, trend=False, changepoints=False, changepoints_threshold=0.01, xlabel='ds', ylabel='y', figsize=(900, 600), colorScheme='Claro'):
    """Plot the Prophet forecast with Plotly offline.
    
    Plotting in Jupyter Notebook requires initializing plotly.offline.init_notebook_mode():
    >>> import plotly.offline as py
    >>> py.init_notebook_mode()
    Then the figure can be displayed using plotly.offline.iplot(...):
    >>> fig = plot_plotly(m, fcst)
    >>> py.iplot(fig)
    see https://plot.ly/python/offline/ for details
    
    Parameters
    ----------
    m: Prophet model.
    fcst: pd.DataFrame output of m.predict.
    uncertainty: Optional boolean to plot uncertainty intervals.
    plot_cap: Optional boolean indicating if the capacity should be shown in the figure, if available.
    trend: Optional boolean to plot trend.
    changepoints: Optional boolean to plot changepoints
    changepoints_threshold: Threshold on trend change magnitude for significance.
    xlabel: Optional label name on X-axis.
    ylabel: Optional label name on Y-axis.
    figsize: Optional figure size.
    colorScheme: Optional color scheme ('Claro' or 'Escuro').
    
    Returns
    -------
    A Plotly Figure.
    """
    line_width = 2
    marker_size = 4
    
    if colorScheme == 'Claro':
    	prediction_color = '#0072B2'
    	error_color = 'rgba(0, 114, 178, 0.2)'  # '#0072B2' with 0.2 opacity
    	actual_color = 'black'
    	cap_color = 'black'
    	trend_color = '#B23B00'
    	bg_color = 'white'
    	txt_color = 'black'
    	grid_color = '#cfcfcf'
    	btn_color = 'white'
    	hover_bg_color = 'white'
    
    if colorScheme == 'Escuro':
    	prediction_color = '#03a3fc'
    	error_color = 'rgba(3, 163, 252, 0.2)'  # '#03a3fc' with 0.2 opacity
    	actual_color = 'white'
    	cap_color = 'white'
    	trend_color = '#B23B00'
    	bg_color = 'black'
    	txt_color = 'white'
    	grid_color = '#525151'
    	btn_color = '#4d4d4d'
    	hover_bg_color = '#4d4d4d'

    data = []
    
    # Add actual
    data.append(go.Scattergl(
        name='Observado',
        x=m.history['ds'],
        y=m.history['y'],
        marker=dict(color=actual_color, size=marker_size),
        mode='markers',
        xhoverformat='%d/%m/%Y'
    ))
    
    # Add lower bound
    if uncertainty and m.uncertainty_samples:
        data.append(go.Scatter(
            x=fcst['ds'],
            y=fcst['yhat_lower'],
            mode='lines',
            line=dict(width=0),
            hoverinfo='skip',
            xhoverformat='%d/%m/%Y'
        ))
    # Add prediction
    data.append(go.Scatter(
        name='Previsto',
        x=fcst['ds'],
        y=fcst['yhat'],
        mode='lines',
        xhoverformat='%d/%m/%Y',
        line=dict(color=prediction_color, width=line_width),
        fillcolor=error_color,
        fill='tonexty' if uncertainty and m.uncertainty_samples else 'none'
    ))
    # Add upper bound
    if uncertainty and m.uncertainty_samples:
        data.append(go.Scatter(
            x=fcst['ds'],
            y=fcst['yhat_upper'],
            mode='lines',
            xhoverformat='%d/%m/%Y',
            line=dict(width=0),
            fillcolor=error_color,
            fill='tonexty',
            hoverinfo='skip'
        ))
    # Add caps
    if 'cap' in fcst and plot_cap:
        data.append(go.Scattergl(
            name='Cap',
            x=fcst['ds'],
            y=fcst['cap'],
            mode='lines',
            xhoverformat='%d/%m/%Y',
            line=dict(color=cap_color, dash='dash', width=line_width),
        ))
    if m.logistic_floor and 'floor' in fcst and plot_cap:
        data.append(go.Scattergl(
            name='Floor',
            x=fcst['ds'],
            y=fcst['floor'],
            mode='lines',
            xhoverformat='%d/%m/%Y',
            line=dict(color=cap_color, dash='dash', width=line_width),
        ))
    # Add trend
    if trend:
        data.append(go.Scattergl(
            name='Trend',
            x=fcst['ds'],
            y=fcst['trend'],
            mode='lines',
            xhoverformat='%d/%m/%Y',
            line=dict(color=trend_color, width=line_width),
        ))
    # Add changepoints
    if changepoints and len(m.changepoints) > 0:
        signif_changepoints = m.changepoints[
            np.abs(np.nanmean(m.params['delta'], axis=0)) >= changepoints_threshold
        ]
        data.append(go.Scattergl(
            x=signif_changepoints,
            y=fcst.loc[fcst['ds'].isin(signif_changepoints), 'trend'],
            marker=dict(size=50, symbol='line-ns-open', color=trend_color,
                        line=dict(width=line_width)),
            mode='markers',
            hoverinfo='skip'
        ))

    layout = dict(
        showlegend=False,
        width=figsize[0],
        height=figsize[1],
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(
        		color=txt_color,
        		size=15
        ),
        hoverlabel=dict(
        		bgcolor=hover_bg_color,
        		font=dict(
        				color=txt_color
        		)
        ),
        yaxis=dict(
            title=dict(
            		text=ylabel,
            		font=dict(
            				color=txt_color,
            				size=15
            		)
            ),
            tickfont=dict(
            		color=txt_color,
            		size=15
            ),
            gridcolor=grid_color
        ),
        xaxis=dict(
            title=dict(
            		text=xlabel,
            		font=dict(
            				color=txt_color,
            				size=15
            		)
            ),
            tickfont=dict(
            		color=txt_color,
            		size=15
            ),
            type='date',
            gridcolor=grid_color,
            rangeselector=dict(
            		bgcolor=btn_color,
                buttons=list([
                    dict(count=7,
                         label='1 semana',
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label='1 mês',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6 meses',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='1 ano',
                         step='year',
                         stepmode='backward'),
                    dict(label='Tudo',
                         step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    return fig