""""

This is a python utility to capture packets live over the Automotive Rig v1.0 from Thales.
The user needs to define only ONE of the following as an argument on the command line:

"""

import pyshark as ps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import pol_utilities as pu
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score


def get_thresholds(dataframe):
    pass


def merge():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))

    files_to_process = [
        f
        for f in os.listdir(input_folder_path)
        if os.path.isfile(os.path.join(input_folder_path, f))
        if f.endswith(".csv")
    ]

    frames = []

    for the_file in files_to_process:
        file_path = os.path.join(input_folder_path, the_file)
        dataset = pd.read_csv(file_path)
        frames.append(dataset)

    training_data = pd.concat(frames)

    output_file_path = os.path.join(input_folder_path, "MASTER.csv")
    training_data.to_csv(output_file_path, index=False)

    if False:
        output_file_path = os.path.join(input_folder_path, "not_cruising_training.csv")
        dataset_training.to_csv(output_file_path, index=False)


def train():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "MASTER.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :7].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    classifier = LogisticRegression(random_state=0)
    classifier.fit(X_train, y_train)

    # Predicting a new result
    print(classifier.predict(sc.transform([[45000, 13400, 13000, 0, 0, 0, 0]])))

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
    print(
        np.concatenate(
            (y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1
        )
    )

    # Making the Confusion Matrix

    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    acc_score = accuracy_score(y_test, y_pred)
    print(acc_score)


if __name__ == "__main__":
    print("Training layer started ...")
    start = time.time()
    train()
    end = time.time()
    print("Training layer execution time: " + str(end - start))
