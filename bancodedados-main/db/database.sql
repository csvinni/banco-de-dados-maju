CREATE DATABASE if not EXISTS `db_mytasks`;
USE `db_mytasks`;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT NOT NULL,
    data_criacao DATE,
    data_limite DATE,
    prioridade TEXT NOT NULL,
    categoria TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
