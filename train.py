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
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    matthews_corrcoef,
    cohen_kappa_score,
    balanced_accuracy_score,
)


def conf_matrix(y_test, y_pred):
    ((tn, fp), (fn, tp)) = metrics.confusion_matrix(y_test, y_pred)
    ((tnr, fpr), (fnr, tpr)) = metrics.confusion_matrix(
        y_test, y_pred, normalize="true"
    )
    return pd.DataFrame(
        [
            [f"TN = {tn} (TNR = {tnr:1.2%})", f"FP = {fp} (FPR = {fpr:1.2%})"],
            [f"FN = {fn} (FNR = {fnr:1.2%})", f"TP = {tp} (TPR = {tpr:1.2%})"],
        ],
        index=["True 0(Normal)", "True 1(Attack)"],
        columns=["Pred 0(Detect as Normal)", "Pred 1(Alert as Attack)"],
    )


def run_svm():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Training the SVM model on the Training set
    from sklearn.svm import SVC

    classifier = SVC(kernel="linear", random_state=0, class_weight="balanced")
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Validation Test
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)

    k_precisions = cross_val_score(
        estimator=classifier, X=X_train, y=y_train, cv=10, scoring="recall"
    )
    print(k_precisions.mean())


def run_kernel_svm():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.svm import SVC

    classifier = SVC(kernel="rbf", random_state=0)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_nb():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Training the Naive Bayes model on the Training set
    from sklearn.naive_bayes import GaussianNB

    classifier = GaussianNB()
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_dtc():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.tree import DecisionTreeClassifier

    classifier = DecisionTreeClassifier(criterion="entropy", random_state=0)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
    y_hat = classifier.predict_proba(X_test)

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_rfc():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.ensemble import RandomForestClassifier

    classifier = RandomForestClassifier(
        n_estimators=10, criterion="entropy", random_state=0
    )
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_lr():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

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
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_knn():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Training the K-NN model on the Training set
    from sklearn.neighbors import KNeighborsClassifier

    classifier = KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
    y_hat = classifier.predict_proba(X_test)
    y_prob = y_hat[:, 1]

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_xgboost():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from xgboost import XGBClassifier

    classifier = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
    classifier.fit(X_train, y_train)
    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
    y_hat = classifier.predict_proba(X_test)
    y_prob = y_hat[:, 1]

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    precision = precision_score(y_test, y_pred)
    print("Precision: %.3f" % precision)
    recall = recall_score(y_test, y_pred)
    print("Recall: %.3f" % recall)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("F-1: %.3f" % f1)
    mcc = matthews_corrcoef(y_test, y_pred)
    print("MCC: %.3f" % mcc)


def run_ocSVM():
    cwd = os.getcwd()
    training_folder_path = os.path.join(cwd, pu.root.get("train"))
    training_file_path = os.path.join(training_folder_path, "TRAINING.csv")

    df_training = pd.read_csv(training_file_path)

    X_train = df_training.iloc[:, 2:-1].values
    y_train = df_training.iloc[:, -1].values

    testing_folder_path = os.path.join(cwd, pu.root.get("live_throughput"))
    testing_file_path = os.path.join(testing_folder_path, "TESTING.csv")

    df_testing = pd.read_csv(testing_file_path)

    X_test = df_testing.iloc[:, :-1].values
    y_test = df_testing.iloc[:, -1].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.svm import OneClassSVM

    classifier = OneClassSVM(gamma="scale", nu=0.01)


if __name__ == "__main__":
    print("\n" + "Logistic Regression started ..." + "\n")
    start = time.time()
    run_lr()
    end = time.time()
    print("\n" + "Logistic Regression time: " + str(end - start) + "\n")

    print("\n" + "Naive Bayes started ..." + "\n")
    start = time.time()
    run_nb()
    end = time.time()
    print("\n" + "Naive Bayes time: " + str(end - start) + "\n")

    print("\n" + "SVM started ..." + "\n")
    start = time.time()
    run_svm()
    end = time.time()
    print("\n" + "SVM time: " + str(end - start) + "\n")

    print("\n" + "Decision Tree Classification started ..." + "\n")
    start = time.time()
    run_dtc()
    end = time.time()
    print("\n" + "Decision Tree Classification Time: " + str(end - start) + "\n")

    print("\n" + "Random Forest Classification started ..." + "\n")
    start = time.time()
    run_rfc()
    end = time.time()
    print("\n" + "Random Forest Classification Time: " + str(end - start) + "\n")

    print("\n" + "XGBoost started ..." + "\n")
    start = time.time()
    run_xgboost()
    end = time.time()
    print("\n" + "XGBoost time: " + str(end - start) + "\n")

    if False:
        print("\n" + "Logistic Regression started ..." + "\n")
        start = time.time()
        run_lr()
        end = time.time()
        print("\n" + "Logistic Regression time: " + str(end - start) + "\n")
        print("\n" + "KNN started ..." + "\n")
        start = time.time()
        run_knn()
        end = time.time()
        print("\n" + "KNN time: " + str(end - start) + "\n")
        print("\n" + "Naive Bayes started ..." + "\n")
        start = time.time()
        run_nb()
        end = time.time()
        print("\n" + "Naive Bayes time: " + str(end - start) + "\n")
