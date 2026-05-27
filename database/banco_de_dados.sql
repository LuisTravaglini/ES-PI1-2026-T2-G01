CREATE DATABASE sist_votacao;

USE sist_votacao;

-- CREATE TABLE Candidato(
-- id_candidato int primary key auto_increment,
-- numero_Candidato int unique not null,
-- nome_Completo varchar(100) unique not null,
-- partido varchar(20) not null,
-- votos int
-- );
CREATE TABLE Candidato(
    id_candidato INT PRIMARY KEY AUTO_INCREMENT,
    numero_Candidato INT UNIQUE NOT NULL,
    nome_Completo VARCHAR(100) UNIQUE NOT NULL,
    partido VARCHAR(20) NOT NULL
);

CREATE TABLE Eleitor(
id_eleitor int primary key auto_increment,
CPF VARCHAR(30) unique not null,
nome_Completo varchar(100) not null,
titulo varchar(15) unique not null,
chave_Acesso VARCHAR(20) unique not null,
tipo_mesario boolean not null,
votou boolean not null
);

CREATE TABLE registro_Voto(
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_Candidato INT,
    FOREIGN KEY (numero_Candidato)
        REFERENCES Candidato(numero_Candidato),
    data_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    protocolo VARCHAR(30)
); 