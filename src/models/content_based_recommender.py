"""
Content-Based Recommendation using TF-IDF
"""

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROCESSED_DIR = Path("data/processed")


class ContentBasedRecommender:

    def __init__(self):

        self.products = pd.read_csv(PROCESSED_DIR / "products.csv")

        # Combine text columns
        self.products["content"] = (
            self.products["product_name"].fillna("") + " " +
            self.products["category"].fillna("") + " " +
            self.products["about_product"].fillna("")
        )

        vectorizer = TfidfVectorizer(stop_words="english")

        tfidf_matrix = vectorizer.fit_transform(self.products["content"])

        self.similarity = cosine_similarity(tfidf_matrix)

    def recommend(self, product_id, top_n=5):

        if product_id not in self.products["product_id"].values:
            return pd.DataFrame()

        idx = self.products[
            self.products["product_id"] == product_id
        ].index[0]

        scores = list(enumerate(self.similarity[idx]))

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        scores = scores[1:top_n + 1]

        indices = [i[0] for i in scores]

        return self.products.iloc[
            indices
        ][["product_id", "product_name", "category"]]


if __name__ == "__main__":

    recommender = ContentBasedRecommender()

    sample_product = recommender.products.iloc[0]["product_id"]

    recommendations = recommender.recommend(sample_product)

    print("\nRecommendations\n")

    print(recommendations)
