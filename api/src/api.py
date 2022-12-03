import json
import os
import pickle

import numpy as np
import pandas as pd
from flask import Flask, request
from flask_cors import CORS


def load_configuration():
    config_file = os.environ["DATA_CONFIG_FILE"]
    data_root = os.environ["DATA_ROOT_FOLDER"]

    if not config_file:
        raise Exception(f"Unknown configuration file: {config_file}")
    if not os.path.exists(data_root):
        raise Exception(f"Data root file does not exist: {data_root}")

    with open(data_root + "/" + config_file) as file:
        models = json.loads(file.read())

    model_key = os.environ["MODEL_KEY"]
    if not model_key:
        raise Exception("MODEL_KEY environment variable not found.")

    target_config = None
    for item in models:
        if item["key"] == model_key:
            target_config = item

    if not target_config:
        raise Exception(f"model_key={model_key} not found in configruation")

    model = pickle.load(open(data_root + "/" + target_config["model"], "rb"))
    features = model.feature_names_in_
    recipes_df = pd.read_pickle((data_root + "/" + target_config["recipes"]))

    print(f"Loaded model with {len(features)} features")

    return model, features, recipes_df


MODEL, FEATURES, RECIPES_DF = load_configuration()
app = Flask(__name__)
CORS(app)


@app.route("/ingredients", methods=["GET"])
def ingredients():
    search_term = request.args.get("search", "")
    if search_term:
        features_series = pd.Series(FEATURES)
        filtered_features = features_series[features_series.str.contains(search_term)]
        return filtered_features.tolist()
    else:
        return list(FEATURES)


@app.route("/predict", methods=["POST"])
def predict():
    ingredients_list = request.get_json()

    print(f"got ingredients: {ingredients_list}")

    empty_array = np.zeros(shape=(1, len(FEATURES)))
    model_input = pd.DataFrame(empty_array, columns=FEATURES)
    for value in ingredients_list:
        model_input[value] = 1
    labels = MODEL.predict(model_input)
    prediction = labels[0]

    print(prediction)
    return {"label": int(prediction)}


@app.route("/recipes", methods=["GET"])
def recipes():
    label = int(request.args.get("label", ""))
    limit = int(request.args.get("limit", 10))

    # TODO How best to cache? should we do a sqlite db?

    result_df = RECIPES_DF
    if label:
        result_df = result_df[result_df["label"] == label]
    result_df["recipe_id"] = result_df.index
    result_df = result_df.replace(np.nan, "")
    return result_df[:limit].to_dict(orient="records")
