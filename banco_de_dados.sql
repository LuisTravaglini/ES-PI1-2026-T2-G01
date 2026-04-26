CREATE DATABASE sist_votacao;

USE sist_votacao;

CREATE TABLE Candidato(
id_candidato int primary key auto_increment,
numero_Candidato int unique not null,
nome_Completo varchar(100) not null,
partido varchar(20) not null
);

CREATE TABLE Eleitor(
id_eleitor int primary key auto_increment,
CPF VARCHAR(11) not null,
nome_Completo varchar(100) not null,
titulo varchar(15) unique not null,
chave_Acesso VARCHAR(20) unique not null,
tipo_mesario boolean not null
);

CREATE TABLE registro_Voto(
id int primary key not null auto_increment,
numero_Candidato int unique not null,
foreign key (numero_Candidato) references Candidato(numero_Candidato),
data_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
