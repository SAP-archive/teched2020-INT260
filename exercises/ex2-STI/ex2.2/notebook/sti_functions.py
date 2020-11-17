import base64
import configparser
import itertools
import json
import time
from pathlib import Path
from typing import NamedTuple
import jwt
import matplotlib.pyplot as plt
import numpy as np
import requests
from requests.models import Response
from sklearn.utils.multiclass import unique_labels


class STIConnectionDetails(NamedTuple):
    uaa_url: str
    service_url: str
    client_id: str
    client_secret: str


token_cache: dict = {}


def get_connection_object(config_file: Path) -> STIConnectionDetails:
    config = configparser.ConfigParser()
    config.read(config_file)
    connection = STIConnectionDetails(
        uaa_url=config["connection"]["uaa_url"],
        service_url=config["connection"]["service_url"],
        client_id=config["connection"]["client_id"],
        client_secret=config["connection"]["client_secret"],
    )
    return connection


def get_access_token(connection: STIConnectionDetails):
    """
    Performs OAuth authentication from provided client id/secret and caches jwt token.
    If token is expired new token is obtained else returned from cache
    """
    if token_cache.get("sti_access_token"):
        token = token_cache["sti_access_token"]
        jwt_token = jwt.decode(token, verify=False, algorithms="RS256")
        if int(time.time()) < jwt_token["exp"]:
            print("Returning token from cache")
            return token

    url = f"{connection.uaa_url}/oauth/token"
    print(f"Getting new token from {url}")

    subscription_text = connection.client_id + ":" + connection.client_secret
    xsuaa_subscription_key_base64 = base64.b64encode(
        subscription_text.encode("utf-8")
    ).decode("utf-8")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {xsuaa_subscription_key_base64}",
    }
    data_payload = {"grant_type": "client_credentials"}
    response = requests.post(url, data=data_payload, headers=headers)

    access_token = response.json().get("access_token")
    token_cache["sti_access_token"] = access_token
    token_expiry = jwt.decode(access_token, verify=False, algorithms="RS256")["exp"]
    token_expiry = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(token_expiry))
    print(f"New token expires at {token_expiry}")
    return access_token


def add_headers(func):
    """
    Adds content type and bearer token to the request header, if not already added.
    """

    def wrapper(sti_instance, *args, **kwargs):
        if kwargs.get("headers") is None:

            headers = {
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(
                    get_access_token(sti_instance.connection)
                ),
            }
            kwargs["headers"] = headers
        return func(sti_instance, *args, **kwargs)

    return wrapper


def parse_response(func):
    """
    If return type is Response object this decorator prints the response time to console
    and returns the result as json object
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, Response):
            print("Response time: {} ms".format(result.elapsed.total_seconds() * 1000))
            return result.json()
        return result

    return wrapper


def plot(cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes, rotation=45)

    fmt = ".2f" if normalize else "d"
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            horizontalalignment="center",
            color="red" if cm[i, j] > thresh else "black",
        )

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")


class STIFunctions:
    """
    Helper class with functions to access STI REST endpoints in pythonic way
    """

    def __init__(self, connection: STIConnectionDetails):
        self.connection = connection

    @add_headers
    @parse_response
    def list_models(self, headers):
        url = f"{self.connection.service_url}/sti/training/model"
        response = requests.get(url, headers=headers)
        return response

    @add_headers
    @parse_response
    def get_model_accuracy(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/accuracy?model_id={model_id}"
        response = requests.get(url, headers=headers)
        return response

    def plot_confusion_matrix(self, model_id):
        accuracy = self.get_model_accuracy(model_id)        
        for idx, result in enumerate(accuracy["validation_results"]):
            fig = plt.figure(figsize=(20, 20))
            labels = accuracy["validation_results"][idx]["confusion_matrix"]["labels"]
            values = accuracy["validation_results"][idx]["confusion_matrix"]["values"]
            confusion_matrix = np.array(values).T
            plot(confusion_matrix, classes=labels, title="Confusion matrix")

    @add_headers
    @parse_response
    def get_model_status(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/status?model_id={model_id}"
        response = requests.get(url, headers=headers)
        return response

    @add_headers
    @parse_response
    def start_model_training(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/train"
        data_payload = {"model_id": "{}".format(model_id)}
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers
    @parse_response
    def activate_model(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/activate"
        data_payload = {"model_id": "{}".format(model_id)}
        response = requests.put(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers
    @parse_response
    def deactivate_model(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/deactivate"
        data_payload = {"model_id": "{}".format(model_id)}
        response = requests.put(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers
    @parse_response
    def classify_text(self, data_payload, headers):
        url = f"{self.connection.service_url}/sti/text/classify"
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers
    @parse_response
    def recommend(self, data_payload, headers):
        url = f"{self.connection.service_url}/sti/solution/recommend"
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers
    @parse_response
    def delete_model(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model?model_id={model_id}"
        response = requests.delete(url, headers=headers)
        return response

    @add_headers
    @parse_response
    def file_upload(self, data_payload, headers):
        url = f"{self.connection.service_url}/sti/training/model"
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response
