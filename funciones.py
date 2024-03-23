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