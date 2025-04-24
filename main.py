import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import pyodbc
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

# Configurações do Blob Storage
blobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')

# Configurações do SQL Server
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')   # Corrigi aqui, você tinha colocado SQL_USER no código
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

# Função para conectar no SQL Server usando pyodbc
def get_sql_connection():
    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER=tcp:{SQL_SERVER},1433;'
        f'DATABASE={SQL_DATABASE};'
        f'UID={SQL_USERNAME};'
        f'PWD={SQL_PASSWORD};'
        f'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    )
    return pyodbc.connect(conn_str)

# Streamlit UI
st.title("Cadastro de Produtos")

product_name = st.text_input('Nome do Produto')
product_price = st.number_input('Preço do Produto', min_value=0.0, format='%.2f')
product_description = st.text_area('Descrição do Produto')
product_image = st.file_uploader('Imagem do Produto', type=['jpg', 'png', 'jpeg'])

# Função para salvar imagem no Blob Storage
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    contaner_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + os.path.splitext(file.name)[1]  # Gera um nome único para o blob
    blob_client = contaner_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url


if st.button('Salvar Produto'):
    if product_name and product_price and product_description and product_image:
        image_url = upload_blob(product_image)

        try:
            conn = get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Produtos (nome, preco, descricao, image_url)
                VALUES (?, ?, ?, ?)
            """, (product_name, product_price, product_description, image_url))

            print(f"Produto {product_name, product_price, product_description, image_url} inserido com sucesso!")
            conn.commit()
            cursor.close()
            conn.close()
            st.success('✅ Produto salvo com sucesso!')
        except Exception as e:
            st.error(f'Erro ao salvar produto: {e}')
    else:
        st.warning('Por favor, preencha todos os campos e selecione uma imagem.')

st.header('Produtos Cadastrados')

if st.button('Listar Produtos'):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, preco, descricao, image_url FROM Produtos")
        rows = cursor.fetchall()
        for row in rows:
            st.subheader(row[0])
            st.write(f"Preço: R$ {row[1]:.2f}")
            st.write(f"Descrição: {row[2]}")
            st.image(row[3], width=200)
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f'Erro ao listar produtos: {e}')
