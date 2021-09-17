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
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import cross_val_score


def run_lr():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)

    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    classifier = LogisticRegression(random_state=0)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix

    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_knn():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    from sklearn.preprocessing import StandardScaler

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Training the K-NN model on the Training set
    from sklearn.neighbors import KNeighborsClassifier

    classifier = KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2)
    classifier.fit(X_train, y_train)
    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)
    # Applying k-Fold Cross Validation
    from sklearn.model_selection import cross_val_score

    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_svm():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Training the SVM model on the Training set
    from sklearn.svm import SVC

    classifier = SVC(kernel="linear", random_state=0)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_kernel_svm():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.svm import SVC

    classifier = SVC(kernel="rbf", random_state=0)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_nb():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Training the Naive Bayes model on the Training set
    from sklearn.naive_bayes import GaussianNB

    classifier = GaussianNB()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_dtc():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.tree import DecisionTreeClassifier

    classifier = DecisionTreeClassifier(criterion="entropy", random_state=0)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_rfc():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.ensemble import RandomForestClassifier

    classifier = RandomForestClassifier(
        n_estimators=10, criterion="entropy", random_state=0
    )
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


def run_xgboost():
    cwd = os.getcwd()
    input_folder_path = os.path.join(cwd, pu.root.get("train"))
    input_file_path = os.path.join(input_folder_path, "TRAINING.csv")

    dataset = pd.read_csv(input_file_path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    from xgboost import XGBClassifier

    classifier = XGBClassifier()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.3f" % accuracy)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred, average="binary")
    print("Recall: %.3f" % recall)
    score = f1_score(y_test, y_pred, average="binary")
    print("F-Measure: %.3f" % score)

    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))

    # Applying k-Fold Cross Validation
    accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
    print("Accuracy: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard Deviation: {:.2f} %".format(accuracies.std() * 100))


if __name__ == "__main__":
    print("Logistic Regression started ...")
    start = time.time()
    run_lr()
    end = time.time()
    print("Logistic Regression time: " + str(end - start))
    print("KNN started ...")
    start = time.time()
    run_knn()
    end = time.time()
    print("KNN time: " + str(end - start))
    print("SVM started ...")
    start = time.time()
    run_svm()
    end = time.time()
    print("SVM time: " + str(end - start))
    print("Kernel SVM started ...")
    start = time.time()
    run_kernel_svm()
    end = time.time()
    print("Kernel SVM time: " + str(end - start))
    print("Naive Bayes started ...")
    start = time.time()
    run_nb()
    end = time.time()
    print("Naive Bayes time: " + str(end - start))
    print("Decision Tree Classification started ...")
    start = time.time()
    run_dtc()
    end = time.time()
    print("Decision Tree Classification Time: " + str(end - start))
    print("Random Forest Classification started ...")
    start = time.time()
    run_rfc()
    end = time.time()
    print("Random Forest Classification Time: " + str(end - start))

    if False:
        print("XGBoost started ...")
        start = time.time()
        run_xgboost()
        end = time.time()
        print("XGBoost time: " + str(end - start))
