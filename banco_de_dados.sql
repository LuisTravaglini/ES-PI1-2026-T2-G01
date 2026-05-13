CREATE DATABASE sist_votacao;

USE sist_votacao;

CREATE TABLE Candidato(
id_candidato int primary key auto_increment,
numero_Candidato int unique not null,
nome_Completo varchar(100) not null,
partido varchar(20) not null,
votos int
);

CREATE TABLE Eleitor(
id_eleitor int primary key auto_increment,
CPF VARCHAR(11) unique not null,
nome_Completo varchar(100) not null,
titulo varchar(15) unique not null,
chave_Acesso VARCHAR(20) unique not null,
tipo_mesario boolean not null,
votou boolean not null
);

CREATE TABLE registro_Voto(
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_Candidato INT NOT NULL,
    FOREIGN KEY (numero_Candidato)
        REFERENCES Candidato(numero_Candidato),
    data_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_eleitor)
);