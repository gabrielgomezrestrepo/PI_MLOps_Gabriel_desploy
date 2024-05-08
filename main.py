from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import funciones
import pandas as pd
import numpy as np

app = FastAPI()# estamos creando la clase FastAPI usando app = enves de la palabra class 

#cargar datos
global steam_games, user_reviews, users_items
steam_games=pd.read_csv("steam_games.csv")
user_reviews=pd.read_csv("user_reviews_con_sentimiento.csv")
users_items=pd.read_csv("users_items.csv")
games=pd.read_parquet('./steam_games_for_ml.parquet')

vector=CountVectorizer(tokenizer=lambda x: x.split(', '))
matriz_descripcion=vector.fit_transform(games['descripcion'])

#http://127.0.0.1:8000 como queremos ir aeste puerto debemos decorar la funcion
@app.get("/") #agregando este decorador
def index():
    return {"data":"para ver las posibles rutas, puedes visitar /doc"}

@app.get("/sentiment_analysis/{ano}")
def mostrar_sentimieto(ano:int):
    respuesta=funciones.sentiment_analysis(ano,steam_games=steam_games,user_reviews=user_reviews,users_items=users_items)
    return {"data":respuesta}

@app.get("/UsersRecommend/{ano}")
def mostrar_sentimieto(ano:int):
    top=funciones.UsersRecommend(ano,steam_games=steam_games,user_reviews=user_reviews,users_items=users_items)
    respuesta={}
    for i,k in enumerate(top):
        respuesta[f"Puesto {i+1}"]=k
    return respuesta

@app.get("/UsersNotRecommend/{ano}")
def mostrar_sentimieto(ano:int):
    top=funciones.UsersNotRecommend(ano,steam_games=steam_games,user_reviews=user_reviews,users_items=users_items)
    respuesta={}
    for i,k in enumerate(top):
        respuesta[f"Puesto {i+1}"]=k
    return respuesta


@app.get("/recomendacion_juego/{id_producto}") 
def recomendacion_juego(id_producto: int):
    recomendaciones=funciones.recomendacion_juego(id_producto=id_producto,games=games,matriz_descripcion=matriz_descripcion)
    return {"recomendaciones":recomendaciones}