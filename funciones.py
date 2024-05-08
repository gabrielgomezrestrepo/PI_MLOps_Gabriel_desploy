def sentiment_analysis(year:int,steam_games,user_reviews,users_items):
    """
    sentimiento de consumidores de los juegos lanzados en año 'year'
    """
    juegos_por_año_lanzamiento=steam_games[steam_games["release_date"].str.contains(str(year))]["id"]
    juegos_por_año_lanzamiento=juegos_por_año_lanzamiento.to_list()

    compradores=users_items[ users_items["item_id"].isin(juegos_por_año_lanzamiento) ].user_id.to_list()
    
    user_reviews[ user_reviews["user_id"].isin(compradores) ][["user_id","sentiment_analysis"]]
    
    sentiment_analysis_data=user_reviews[ user_reviews["user_id"].isin(compradores) ][["user_id","sentiment_analysis"]]
    
    valoraciones_por_año=sentiment_analysis_data["sentiment_analysis"].value_counts()
    neutrales=valoraciones_por_año[1]
    positivas=valoraciones_por_año[2]
    negativas=valoraciones_por_año[0]
    #print("{{Negative = {}, Neutral = {}, Positive = {}}}".format(negativas,neutrales,positivas))
    respuesta="Negative = {}, Neutral = {}, Positive = {}".format(negativas,neutrales,positivas)
    return respuesta

def UsersRecommend(year:int,steam_games,user_reviews,users_items):
    year_review=user_reviews[user_reviews["posted"].str.contains(str(year))]
    totales=year_review[year_review["recommend"]==True]["item_id"].value_counts().head(3)
    topids=totales.index.tolist()
    topcount=totales.tolist()
    topgames=steam_games[steam_games["id"].isin(topids)]["app_name"].tolist()
    # print(topids)
    # print(topcount)
    # print(topgames)
    ouptstring="["
    for i,k in enumerate(topgames):
        ouptstring+=f'{{"Puesto {i+1}":"{k}"}},'
    ouptstring+="]"
    print(ouptstring)
    return topgames

def UsersNotRecommend(year:int,steam_games,user_reviews,users_items):
    year_review=user_reviews[user_reviews["posted"].str.contains(str(year))]
    totales=year_review[year_review["recommend"]==False]["item_id"].value_counts().head(3)
    topids=totales.index.tolist()
    topcount=totales.tolist()
    topgames=steam_games[steam_games["id"].isin(topids)]["app_name"].tolist()
    # print(topids)
    # print(topcount)
    # print(topgames)
    ouptstring="["
    for i,k in enumerate(topgames):
        ouptstring+=f'{{"Puesto {i+1}":"{k}"}},'
    ouptstring+="]"
    print(ouptstring)
    return topgames

def recomendacion_juego(id_producto: int,games,matriz_descripcion):
    '''
    Se ingresa el id de producto (item_id) y retorna una lista con 5 juegos recomendados similares al ingresado (title).
    
    '''
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # se verifica la existencia del id del producto
    if id_producto not in games['id'].values:
        return 'El id no ha sido tomado, intente con otro'
    else:
        # buscamos el índice del id del producto ingresado
        index = games.index[games['id']==id_producto][0]

        # De la matriz de conteo, tomamos el array de descripciones con índice igual a 'index':
        # esto significa que vamos a tomar aquellas posiciones donde se debe comparar el producto
        # con los demás
        description_index = matriz_descripcion[index]

        # Calculamos la similitud coseno entre la descripción de entrada y la descripción de las demás filas: cosine_similarity(description_index, matriz_descripcion)
        # Obtenemos los índices de las mayores similitudes mediante el método argsort() y las similitudes ordenadas de manera descendente
        # Tomamos los índices del 1 al 6 [0, 1:6] ya que el índice 0 es el mismo índice de entrada
        indices_maximos = np.argsort(-cosine_similarity(description_index, matriz_descripcion))[0, 1:6]

        # Construimos la lista
        recomendaciones = []
        for i in indices_maximos:
            recomendaciones.append(games['app_name'][i])
        
        return recomendaciones