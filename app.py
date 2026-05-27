import dash
from layout import layout

app = dash.Dash(__name__)

app.layout = layout

if __name__ == "__main__":
    app.run(debug=True)