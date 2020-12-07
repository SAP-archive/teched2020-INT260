import base64
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
from uuid import uuid4

class STIConnectionDetails(NamedTuple):
    uaa_url: str
    service_url: str
    client_id: str
    client_secret: str


token_cache: dict = {}


def get_connection_object(config_file: Path) -> STIConnectionDetails:
    f = open(config_file,)
    config = json.load(f)
    connection = STIConnectionDetails(
        uaa_url=config["uaa"]["url"],
        service_url=config["sti_service_url"],
        client_id=config["uaa"]["clientid"],
        client_secret=config["uaa"]["clientsecret"],
    )
    return connection


def get_access_token(connection: STIConnectionDetails, print_message=True):
    """
    Performs OAuth authentication from provided client id/secret and caches jwt token.
    If token is expired new token is obtained else returned from cache
    """
    if token_cache.get("sti_access_token"):
        token = token_cache["sti_access_token"]
        jwt_token = jwt.decode(token, verify=False, algorithms="RS256")
        if int(time.time()) < jwt_token["exp"]:
            if print_message:
                print("Returning token from cache")
            return token

    url = f"{connection.uaa_url}/oauth/token"
    if print_message:
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
    if print_message:
        print(f"New token expires at {token_expiry}")
    return access_token


def add_headers(print_message=True):
    """
    Adds content type and bearer token to the request header, if not already added.
    """

    def decorate(func):
        def wrapper(sti_instance, *args, **kwargs):
            correlation_id = uuid4().hex
            print(f"Correlation id: {correlation_id}")
            if kwargs.get("headers") is None:
                headers = {
                    "content-type": "application/json",
                    "X-Request-ID": correlation_id,
                    "Authorization": "Bearer {}".format(
                        get_access_token(sti_instance.connection, print_message)
                    ),
                }
                kwargs["headers"] = headers
            return func(sti_instance, *args, **kwargs)

        return wrapper

    return decorate


def parse_response(print_message=True):
    """
    If return type is Response object this decorator prints the response time to console
    and returns the result as json object
    """

    def decorate(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, Response):
                if print_message:
                    print("Response time: {} ms".format(result.elapsed.total_seconds() * 1000))
                return result.json()
            return result

        return wrapper

    return decorate


def plot(cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues, subplot=None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        # print("Normalized confusion matrix")
    # else:
    # print("Confusion matrix, without normalization")

    if subplot:
        nrows, ncols, subplot_num = subplot
        plt.subplot(nrows, ncols, subplot_num)

    classes = [str(l[:20]) + '...' for l in classes]

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


def automation_accuracy_plot(threshold_list, automation_list, accuracy_list, category_name):
    fig, ax1 = plt.subplots(figsize=(15, 10))
    ax1.set_title(category_name, size=20)
    color = 'tab:red'
    ax1.set_xlabel('threshold', fontsize=20)
    ax1.set_ylabel('automation rate', color=color, fontsize=20)
    ax1.plot(threshold_list, automation_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('accuracy', color=color, fontsize=20)  # we already handled the x-label with ax1
    ax2.plot(threshold_list, accuracy_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


class STIFunctions:
    """
    Helper class with functions to access STI REST endpoints in pythonic way
    """

    def __init__(self, connection: STIConnectionDetails):
        self.connection = connection

    @add_headers(True)
    @parse_response(True)
    def list_models(self, headers):
        url = f"{self.connection.service_url}/sti/training/model"
        response = requests.get(url, headers=headers)
        return response

    @add_headers(True)
    @parse_response(True)
    def get_model_accuracy(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/accuracy?model_id={model_id}"
        response = requests.get(url, headers=headers)
        return response

    @add_headers(False)
    @parse_response(False)
    def get_model_accuracy_with_threshold(self, model_id, threshold, headers):
        url = f"{self.connection.service_url}/sti/training/model/accuracy?model_id={model_id}&threshold={threshold}"
        response = requests.get(url, headers=headers)
        return response

    def plot_confusion_matrix(self, model_id):
        accuracy = self.get_model_accuracy(model_id)
        for idx, result in enumerate(accuracy["validation_results"]):
            fig = plt.figure(figsize=(20, 20))
            labels = accuracy["validation_results"][idx]["confusion_matrix"]["labels"]
            values = accuracy["validation_results"][idx]["confusion_matrix"]["values"]
            field = accuracy["validation_results"][idx]["field"]
            confusion_matrix = np.array(values).T
            plot(confusion_matrix, classes=labels, title=field)

    def plot_confusion_matrix_for_different_threshold(self, model_id):
        threshold_list = np.arange(0, 1, 0.1)
        tmp = self.get_model_accuracy(model_id)
        category_number = len(tmp['validation_results'])

        for idx in range(category_number):
            fig = plt.figure(figsize=(50, 50))
            for thresh_num, thresh in enumerate(threshold_list):
                accuracy = self.get_model_accuracy_with_threshold(model_id, thresh)
                if thresh == 0.0:
                    validation_results = accuracy['validation_results']
                else:
                    validation_results = accuracy['validation_results_at_thresholds']['validation_results']
                labels = validation_results[idx]["confusion_matrix"]["labels"]
                values = validation_results[idx]["confusion_matrix"]["values"]
                field = validation_results[idx]["field"]
                confusion_matrix = np.array(values, dtype=int).T
                plot(confusion_matrix, classes=labels, title=field + '_with_threshold_' + str(round(thresh, 2)),
                     subplot=(5, 2, 1 + thresh_num))

    def plot_automation_accuracy(self, model_id):
        threshold_list = np.arange(0, 1, 0.1)
        tmp = self.get_model_accuracy(model_id)
        num_categories = len(tmp['validation_results'])
        automation_list = [[] for _ in range(num_categories)]
        accuracy_list = [[] for _ in range(num_categories)]
        category_list = [item['field'] for item in tmp['validation_results']]

        for thresh in threshold_list:
            accuracy = self.get_model_accuracy_with_threshold(model_id, thresh)
            if thresh == 0.0:
                results = accuracy['validation_results']
                for num, cat_result in enumerate(results):
                    automation_list[num].append(1)
                    cm = np.array(cat_result['confusion_matrix']['values'])
                    accuracy_list[num].append(np.sum(cm.diagonal()) / np.sum(cm))
            else:
                validation_results = accuracy['validation_results_at_thresholds']['validation_results']
                for num, cat_result in enumerate(validation_results):
                    automation_list[num].append(cat_result['probability_of_exceeding_threshold'])
                    accuracy_list[num].append(cat_result['accuracy'])

        for accuracy, automation, category in zip(accuracy_list, automation_list, category_list):
            automation_accuracy_plot(threshold_list, automation, accuracy, category)

    @add_headers(True)
    @parse_response(True)
    def get_model_status(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/status?model_id={model_id}"
        response = requests.get(url, headers=headers)
        return response

    @add_headers(True)
    @parse_response(True)
    def start_model_training(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/train"
        data_payload = {"model_id": "{}".format(model_id)}
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers(True)
    @parse_response(True)
    def activate_model(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/activate"
        data_payload = {"model_id": "{}".format(model_id)}
        response = requests.put(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers(True)
    @parse_response(True)
    def deactivate_model(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model/deactivate"
        data_payload = {"model_id": "{}".format(model_id)}
        response = requests.put(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers(True)
    @parse_response(True)
    def classify_text(self, data_payload, headers):
        url = f"{self.connection.service_url}/sti/text/classify"
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers(True)
    @parse_response(True)
    def recommend(self, data_payload, headers):
        url = f"{self.connection.service_url}/sti/solution/recommend"
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response

    @add_headers(True)
    @parse_response(True)
    def delete_model(self, model_id, headers):
        url = f"{self.connection.service_url}/sti/training/model?model_id={model_id}"
        response = requests.delete(url, headers=headers)
        return response

    @add_headers(True)
    @parse_response(True)
    def file_upload(self, data_payload, headers):
        url = f"{self.connection.service_url}/sti/training/model"
        response = requests.post(url, headers=headers, data=json.dumps(data_payload))
        return response
