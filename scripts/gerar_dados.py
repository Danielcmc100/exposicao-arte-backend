import os
import random
import sys

import numpy as np
from faker import Faker
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.create import create_engine
from sqlmodel import Session, SQLModel, delete

# Add src to python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)

from database import engine
from models.avaliacoes_eventos import AvaliacaoEventoDB
from models.evento import EventoDB
from models.usuario import UsuarioDB

fake = Faker("pt_BR")


def limpar_banco(engine: Engine):
    with Session(engine) as session:
        print("Limpando banco de dados...")
        # Ordem importa por causa das Foreign Keys
        session.exec(delete(AvaliacaoEventoDB))
        session.exec(delete(EventoDB))
        session.exec(delete(UsuarioDB))
        session.commit()
        print("Banco limpo!")


def popular_banco_com_regras(
    engine: Engine, n_usuarios: int = 50, n_eventos: int = 20
):
    with Session(engine) as session:
        # 1. Criar Usuários (Organizadores e Participantes)
        usuarios = []
        print(f"Criando {n_usuarios} usuários...")
        for _ in range(n_usuarios):
            user = UsuarioDB(
                nome=fake.name(),
                email=fake.email(),
                funcao="CONSUMIDOR",  # Variar conforme necessidade
                biografia=fake.text(),
                senha="hash_senha_falsa",
            )
            session.add(user)
            usuarios.append(user)
        session.commit()

        # Separar alguns para serem organizadores "famosos"
        organizadores = usuarios[:5]

        # 2. Gerar Eventos com "Regras Escondidas"
        locais_score = {"Centro": 100, "Bairro": 50}

        print(f"Criando {n_eventos} eventos...")
        for _ in range(n_eventos):
            organizador = random.choice(organizadores)
            local_nome = random.choice(list(locais_score.keys()))
            data_evento = fake.date_time_between(
                start_date="-1y", end_date="now"
            )

            # Lógica da Opção 2: Calcular Base
            score_local = locais_score[local_nome]
            score_dia = (
                50 if data_evento.weekday() >= 5 else 10
            )  # Fim de semana vale mais
            multiplicador_org = (
                1.5 if organizador in organizadores[:2] else 1.0
            )

            publico_base = (score_local + score_dia) * multiplicador_org

            # Adicionar Ruído (NumPy é ótimo aqui para distribuição normal)
            ruido = np.random.normal(0, 10)  # Média 0, desvio padrão 10
            publico_final = int(publico_base + ruido)

            evento = EventoDB(
                nome=f"Exposição {fake.word().title()}",
                endereco=fake.address(),
                local=local_nome,
                data=data_evento,
                id_organizador=organizador.id,
                id_responsavel=organizador.id,
            )
            session.add(evento)
            session.commit()  # Commit para ter o ID do evento

            # 3. Gerar Avaliações baseadas no sucesso (opcional)
            # Se o evento foi um sucesso (publico_final alto), tende a ter notas melhores
            media_nota = 4.5 if publico_final > 150 else 3.0

            for user in random.sample(usuarios, k=random.randint(5, 20)):
                nota_com_ruido = np.clip(
                    np.random.normal(media_nota, 0.5), 1, 5
                )
                avaliacao = AvaliacaoEventoDB(
                    usuario_id=user.id,
                    evento_id=evento.id,
                    gostou="Sim" if nota_com_ruido > 3 else "Não",
                    avaliacao=int(round(nota_com_ruido)),
                )
                session.add(avaliacao)

        session.commit()


if __name__ == "__main__":
    print("Iniciando geração de dados...")
    # Cria o banco local para teste (se não existir)
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/exposicao_arte"
    )
    SQLModel.metadata.create_all(engine)

    limpar_banco(engine)
    popular_banco_com_regras(engine, n_usuarios=500, n_eventos=100)
    print("Dados gerados com sucesso!")
