import pandas as pd
import numpy as np



file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print("Loaded data:", df.shape)



print("\nFirst 5 rows:")
print(df.head())



average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage score   :", average_score)
print("Average comments:", average_comments)



scores = df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)
print("Max score    :", max_score)
print("Min score    :", min_score)



category_counts = df["category"].value_counts()

most_category = category_counts.idxmax()
most_category_count = category_counts.max()

print(
    "\nMost stories in:",
    most_category,
    "(",
    most_category_count,
    "stories)"
)



most_commented = df.loc[df["num_comments"].idxmax()]

print(
    "\nMost commented story:",
    most_commented["title"],
    "—",
    most_commented["num_comments"],
    "comments"
)



df["engagement"] = df["num_comments"] / (df["score"] + 1)



df["is_popular"] = df["score"] > average_score



output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print("\nSaved to", output_file)