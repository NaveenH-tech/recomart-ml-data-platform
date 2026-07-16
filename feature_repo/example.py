from feast import FeatureStore

store = FeatureStore(repo_path=".")

features = store.get_historical_features(
    entity_df={
        "user_id": [1, 2, 3]
    },
    features=[
        "user_features:activity_count",
        "user_features:average_rating"
    ]
).to_df()

print(features)
