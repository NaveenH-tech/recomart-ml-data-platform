from datetime import timedelta

from feast import Entity
from feast import FeatureView
from feast import Field
from feast import FileSource
from feast.types import Float32
from feast.types import Int64

user = Entity(
    name="user_id",
    join_keys=["user_id"],
)

user_source = FileSource(
    path="../data/feature_store/user_features.csv",
    timestamp_field=None,
)

user_feature_view = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=365),
    schema=[
        Field(name="activity_count", dtype=Int64),
        Field(name="average_rating", dtype=Float32),
    ],
    source=user_source,
)
