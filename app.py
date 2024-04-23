from dash import Dash, html, dash_table, dcc, Input, Output, callback
import pandas as pd

df = pd.read_excel('D:\Projects\Online Expenditure Dashboard\Data\Expenditure.xlsx')

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Expenditure'),
    dash_table.DataTable
    (
        id='Expenditure-Interactive',
        columns=[
            {'name':'No',       'id':'No',       'type':'numeric'},
            {'name':'Title',    'id':'Title',    'type':'text'},
            {'name':'Category', 'id':'Category', 'type':'text'},
            {'name':'Amount',   'id':'Amount',   'type':'numeric'},
            {'name':'Balance',  'id':'Balance',  'type':'numeric'}
                ],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        page_size=10,
        editable=True,
        row_deletable=True
    ),
    #dcc.Graph(figure=px.histogram(df, x='Category', y='Amount', histfunc='sum',))
    html.Div(id='Expenditure-Interactive-Dynamic')
])

@callback(
    Output('Expenditure-Interactive', 'style_data_conditional'),
    Input('Expenditure-Interactive', 'selected_columns'))


def update_styles(selected_columns):
    return [{
        'background_color': '#D2F3FF'
    }]

@callback(
    Output('Expenditure-Interactive-Dynamic', "children"),
    Input('Expenditure-Interactive', "derived_virtual_data"),
    Input('Expenditure-Interactive', "derived_virtual_selected_rows"))

def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows=[]

    dff = df if rows is None else pd.DataFrame(rows)

    '''colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
            for i in range(len(dff))]'''
            
    return [
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": dff["Category"],
                        "y": dff["Amount"],
                        "type": "bar"
                        #"marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": "Money"}
                    },
                    "height": 500,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        
    ]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)