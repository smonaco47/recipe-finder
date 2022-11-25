from flask import Flask
from flask import request
import json
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

MODELS = {
    2: {
        "model": "/src/models/trained_kmeans_2_20221023-221709.pkl",
        "recipes": "/src/cleaned_data/labeled_recipes_df_2.pkl"
    },
    6: {
        "model": "/src/models/trained_kmeans_6_20221023-221759.pkl",
        "recipes": "/src/cleaned_data/labeled_recipes_df_6.pkl"
    },
    10: {
        "model": "/src/models/trained_kmeans_10_20221023-221848.pkl",
        "recipes": "/src/cleaned_data/labeled_recipes_df_10.pkl"
    },
    20: {
        "model": "/src/models/trained_kmeans_20_20221023-222054.pkl",
        "recipes": "/src/cleaned_data/labeled_recipes_df_20.pkl"
    },
    28: {
        "model": "/src/models/trained_kmeans_28_20221023-222235.pkl",
        "recipes": "/src/cleaned_data/labeled_recipes_df_28.pkl"
    }
}

VERSION = 20

def load_model():
    path = MODELS[VERSION]["model"]
    model = pickle.load(open(path, 'rb'))
    features = model.feature_names_in_
    print(f"Loaded model with {len(features)} features")
    return model, features
    
@app.route('/ingredients', methods=['GET'])
def ingredients():
    search_term = request.args.get('search', '')
    model, features = load_model()
    if search_term:
        features_series = pd.Series(features)
        filtered_features = features_series[features_series.str.contains(search_term)]
        return filtered_features.tolist()
    else:
        return list(features)
    
@app.route('/predict', methods=['POST'])
def predict():
    json_input = request.get_json()
    ingredients_list = json.loads(json_input)
    
    print(f"got ingredients: {ingredients_list}")
    model, features = load_model()
    
    model_input = pd.DataFrame(np.zeros(shape=(1,len(features))), columns=features)
    for value in ingredients_list:
        model_input[value]=1
    labels = model.predict(model_input)
    prediction = labels[0]

    print(prediction)
    return {"label": int(prediction)}

@app.route('/recipes', methods=['GET'])
def recipes():
    label = int(request.args.get('label', ''))
    limit = int(request.args.get('limit', 10))

    #     TODO How best to cache? should we do a sqlite db?

    path = MODELS[VERSION]["recipes"]
    result_df = pd.read_pickle(path)
    if label:
        result_df = result_df[result_df["label"] == label]
    result_df["recipe_id"]=result_df.index
    
    return result_df[:limit].to_dict(orient="records")