import dash
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from bson.objectid import ObjectId

#-------------CONNECT TO MONGODB-----------------
client = MongoClient("mongodb+srv://oscarmejias:oscar123@cluster0.bunlk55.mongodb.net/?retryWrites=true&w=majority")

# test connection
# data = list(db.data1.find())
# print(data)
# exit()

db = client.get_database('example_db')
collection = db.data2

# Define Layout of App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('Web Application connected to a Live Database', style={'textAlign': 'center'}),
    # interval activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div(id='mongo-datatable', children=[]),

    html.Div([
        html.Div(id='pie-graph', className='five columns'),
        html.Div(id='hist-graph', className='six columns'),
    ], className='row'),

    # dcc.Graph(
    #     id='example-graph',
    #     # figure=fig  # commented out to make the example runnable
    # ),

    html.Iframe(src="https://charts.mongodb.com/charts-project-0-vcbpq/embed/charts?id=639bf7f3-7ce0-4341-8206-0c5e3e7d422a&maxDataAge=10&theme=dark&autoRefresh=true",
                style={"background": "#21313C", "border": "none", "border-radius": "2px", "box-shadow": "0 2px 10px 0 rgba(70, 76, 79, .2);", "width":"60%", "height":"1000"},
                height= 800,
                ),

    html.Iframe(src="https://charts.mongodb.com/charts-project-0-vcbpq/embed/charts?id=639c0544-7ae1-4fcf-80ff-e4247ea4fbba&maxDataAge=10&theme=dark&autoRefresh=true",
                style={"background": "#21313C", "border": "none", "border-radius": "2px", "box-shadow": "0 2px 10px 0 rgba(70, 76, 79, .2);", "width":"40%", "height":"1000"},
                height= 800,
                ),
                

    dcc.Store(id='changed-cell')
])


# Display Datatable with data from Mongo database
@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def populate_datatable(n_intervals):
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    # Convert id from ObjectId to string so it can be read by DataTable
    df['_id'] = df['_id'].astype(str)
    #print(df.head(20))

    columns = []
    for p in df:
        if p == 'date':
            columns.append({'id': p, 'name': p, 'editable': False})
        elif not p == '_id':
            columns.append({'id': p, 'name': p, 'editable': True})
    #else {'id': p, 'name': p, 'editable': True}

    return [
        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns= columns,
        ),
    ]



# store the row id and column id of the cell that was updated
app.clientside_callback(
    """
    function (input,oldinput) {
        if (oldinput != null) {
            if(JSON.stringify(input) != JSON.stringify(oldinput)) {
                for (i in Object.keys(input)) {
                    newArray = Object.values(input[i])
                    oldArray = Object.values(oldinput[i])
                    if (JSON.stringify(newArray) != JSON.stringify(oldArray)) {
                        entNew = Object.entries(input[i])
                        entOld = Object.entries(oldinput[i])
                        for (const j in entNew) {
                            if (entNew[j][1] != entOld[j][1]) {
                                changeRef = [i, entNew[j][0]] 
                                break        
                            }
                        }
                    }
                }
            }
            return changeRef
        }
    }    
    """,
    Output('changed-cell', 'data'),
    Input('our-table', 'data'),
    State('our-table', 'data_previous')
)

# Update MongoDB and create the graphs
@app.callback(
    Output("pie-graph", "children"),
    Output("hist-graph", "children"),
    Input("changed-cell", "data"),
    Input("our-table", "data"),
)
def update_d(cc, tabledata):
    if cc is None:
        # Build the Plots
        # print(f'Current DataTable: {tabledata}')
        pie_fig = px.pie(tabledata, values='masa', names='densidad')
        hist_fig = px.histogram(tabledata, x='densidad', y='masa')
    else:
        print(f'changed cell: {cc}')
        print(f'Current DataTable: {tabledata}')
        x = int(cc[0])

        # update the external MongoDB
        row_id = tabledata[x]['_id']
        col_id = cc[1]
        new_cell_data = tabledata[x][col_id]
        collection.update_one({'_id': ObjectId(row_id)},
                            {"$set": {col_id: float(new_cell_data)}})
        # Operations guide - https://docs.mongodb.com/manual/crud/#update-operations

        # pie_fig = px.pie(tabledata, values='quantity', names='day')
        # hist_fig = px.histogram(tabledata, x='department', y='quantity')

    return (), []
    # return dcc.Graph(figure=pie_fig), dcc.Graph(figure=hist_fig)

if __name__ == '__main__':
    app.run_server(debug=False)