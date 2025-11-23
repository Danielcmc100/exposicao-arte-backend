"""Reúne serviços utilizados na manipulação de eventos."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

from models.evento import PrevisaoEvento

model_filename = (
    Path.cwd() / "src" / "resources" / "models" / "prever_evento.joblib"
)

eventos_preview_model: LinearRegression = joblib.load(model_filename)


def prever_pessoas_em_evento(evento: PrevisaoEvento) -> int:
    """Prevê a quantidade de pessoas em um evento.

    Args:
        evento (PrevisaoEvento): Objeto contendo as características do evento
            para previsão.

    Returns:
        int: Número previsto de pessoas no evento, arredondado para o inteiro
            mais próximo.

    """
    data_frame_input = pd.DataFrame([evento.model_dump()])
    resultado = eventos_preview_model.predict(data_frame_input)
    return int(round(resultado[0], 0))
