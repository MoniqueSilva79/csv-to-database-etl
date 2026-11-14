# 🔄 ETL Simples: CSV ➜ Banco de Dados

Pipeline de ETL (**Extract, Transform, Load**) que lê planilhas CSV "sujas", limpa e padroniza os dados e carrega tudo em um banco SQLite (ou PostgreSQL), com log de qualidade.

## 🎯 Problema que resolve
Dados de clientes chegam com e-mails inválidos, datas em formatos diferentes, duplicados e campos vazios. O pipeline transforma isso em uma tabela confiável para análise.

## 🏗️ Fluxo
```
data/raw/*.csv ──► EXTRACT (pandas) ──► TRANSFORM (limpeza + validação) ──► LOAD (SQLite/PostgreSQL)
                                                  │
                                                  └──► rejeitados.csv (linhas inválidas)
```

## 🧹 Regras de transformação
- Remove espaços extras e padroniza nomes (Title Case)
- Valida e-mail com regex
- Converte datas em vários formatos para `AAAA-MM-DD`
- Normaliza UF para maiúsculas
- Converte valores "R$ 1.234,56" para número
- Remove duplicados por e-mail
- Salva as linhas inválidas em `rejeitados.csv`

## 🧰 Tecnologias
Python 3.10+, pandas, SQLAlchemy, SQLite (padrão) ou PostgreSQL

## 🚀 Como rodar
```bash
git clone https://github.com/MoniqueSilva79/csv-to-database-etl.git
cd csv-to-database-etl
pip install -r requirements.txt
python etl.py                       # carrega em clientes.db (SQLite)

# PostgreSQL:
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
python etl.py
```

## 📚 O que pratiquei
- Conceitos de ETL e qualidade de dados
- pandas para limpeza
- Carga em banco relacional com SQLAlchemy

## 🗺️ Próximos passos
- [ ] Agendar com Airflow ou Cloud Scheduler
- [ ] Testes unitários das regras de limpeza (pytest)
- [ ] Carga incremental
