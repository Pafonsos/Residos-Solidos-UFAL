import dash
from layout import layout
from callbacks import callbacks

app = dash.Dash(__name__)

app.layout = layout

# Registrar todos os callbacks
callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)