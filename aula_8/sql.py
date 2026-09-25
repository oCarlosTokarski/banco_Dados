#lib para se comuicar com o sqlite
import sqlite3 as sql

conexao = sql.connect("reserva_salas.db")


#permite o controle transacional
cursor = conexao.cursor()


cursor.execute("PRAGMA foreing_keys = ON;")
print("Conexão aberta")


cursor.executescript("""

    DROP TABLE IF EXISTS usuario;
    DROP TABLE IF EXISTS telefone_usuario;
    DROP TABLE IF EXISTS reserva;
    DROP TABLE IF EXISTS sala;
    DROP TABLE IF EXISTS bloco;

    CREATE TABLE usuario (
        id_usuario INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
    );
    
    CREATE TABLE telefone_usuario(
        id_usuario INTEGER NOT NULL,
        telefone TEXT NOT NULL,
        PRIMARY KEY (id_usuario, telefone),
        FOREIGN KEY (id_usuario)
            REFERENCES usuario(id_usuario)
            ON DELETE CASCADE
    );

    CREATE TABLE bloco (
        id_bloco INTEGER PRIMARY KEY,
        nome_bloco TEXT NOT NULL UNIQUE 

    );

    CREATE TABLE sala (
        id_sala INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        capacidade INTEGER NOT NULL
            CHECK (capacidade > 0),
        id_bloco INTEGER NOT NULL,
        FOREIGN KEY (id_bloco)
            REFERENCES bloco(id_bloco)
            ON DELETE RESTRICT
    );

    CREATE TABLE reserva (
        id_reserva INTEGER PRIMARY KEY,
        id_usuario INTEGER NOT NULL,
        id_sala INTEGER NOT NULL,
        data DATE NOT NULL,
        hora_inicio TIME NOT NULL,
        situacao TEXT NOT NULL
            DEFAULT 'ativa'
            CHECK (situacao IN ('ativa', 'cancelada', 'reservada')),
        FOREIGN KEY (id_usuario)
            REFERENCES usuario(id_usuario)
            ON DELETE RESTRICT,
        
        FOREIGN KEY (id_sala)
            REFERENCES sala(id_sala)
            ON DELETE RESTRICT

    );


""")
# Commit efetiva as modificaçoes
conexao.commit()

print("Estrutura criada")
