import pandas as pd

print("\nLayer 01 (Data Collector) Output\n")
df_preprocessed = pd.read_csv("./01_preprocessed/CC_9-10.csv")
print(df_preprocessed)

print("\nLayer 02 (Feature Extractor) Output\n")
df_feature = pd.read_csv("./02_features/CC_9-10.csv")
print(df_feature)
