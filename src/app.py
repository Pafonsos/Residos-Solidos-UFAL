import threading
import time
import sys
from pathlib import Path

import dash

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import webview
except ModuleNotFoundError:
    webview = None

from layout import layout
from src.banco_dados import criar_banco_dados, iniciar_banco_dados
from src.callbackv2 import registrar_grafico


def criar_app():
    criar_banco_dados(iniciar_banco_dados())
    app = dash.Dash(__name__)
    app.layout = layout
    registrar_grafico(app)
    return app


app = criar_app()


def iniciar_dash():
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=False,
    )


if __name__ == "__main__":
    if "--server" in sys.argv or webview is None:
        if webview is None:
            print("pywebview nao esta instalado. Abrindo apenas o servidor Dash.")
        print("Acesse: http://127.0.0.1:8050")
        iniciar_dash()
        raise SystemExit

    # inicia o servidor em segundo plano
    threading.Thread(target=iniciar_dash, daemon=True).start()

    # espera o servidor subir
    time.sleep(2)

    # abre uma janela desktop
    webview.create_window(
        "Meu Sistema",
        "http://127.0.0.1:8050",
        width=1400,
        height=900,
    )

    webview.start()
