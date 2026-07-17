import sys
import sqlite3
from pathlib import Path
 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
 
# ------------------------------------------------------------------
# Project Path Setup
# ------------------------------------------------------------------
 
src_dir = str(Path(__file__).resolve().parent.parent)
 
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
 
from common.logger import logger
 
 
def run_feature_pipeline():
 
    logger.info(
        "Initializing Feature Engineering & Database Transformation engine...",
        extra={"pipeline_step": "FEATURE_START"}
    )
 
    try:
 
        # ----------------------------------------------------------
        # DIRECTORY CONFIGURATION
        # ----------------------------------------------------------
 
        project_root = Path(src_dir).parent
 
        processed_dir = project_root / "data" / "processed"
        warehouse_dir = project_root / "data" / "warehouse"
 
        warehouse_dir.mkdir(parents=True, exist_ok=True)
 
        db_path = warehouse_dir / "recomart_warehouse.db"
        
        # Drop existing database to ensure fresh start
        if db_path.exists():
            db_path.unlink()
            logger.info(
                f"Deleted existing warehouse database: {db_path}",
                extra={"pipeline_step": "DB_CLEANUP"}
            )
 
        # ----------------------------------------------------------
        # INPUT FILES
        # ----------------------------------------------------------
 
        users_file = processed_dir / "users.csv"
        products_file = processed_dir / "products.csv"
        reviews_file = processed_dir / "reviews.csv"
        sessions_file = processed_dir / "sessions.csv"
        clickstream_file = processed_dir / "clickstream.csv"
 
        # ----------------------------------------------------------
        # FILE VALIDATION
        # ----------------------------------------------------------
 
        required_files = [
            users_file,
            products_file,
            reviews_file,
            sessions_file,
            clickstream_file
        ]
 
        missing_files = [
            str(file)
            for file in required_files
            if not file.exists()
        ]
 
        if missing_files:
            raise FileNotFoundError(
                f"Missing input files: {missing_files}"
            )
 
        # ----------------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------------
 
        users_df = pd.read_csv(users_file)
        products_df = pd.read_csv(products_file)
        reviews_df = pd.read_csv(reviews_file)
        sessions_df = pd.read_csv(sessions_file)
        clickstream_df = pd.read_csv(clickstream_file)
        logger.info(
            "Processed datasets loaded successfully.",
            extra={"pipeline_step": "LOAD_DATA"}
        )
 
        # ----------------------------------------------------------
        # EMPTY DATA CHECK
        # ----------------------------------------------------------
 
        if reviews_df.empty:
            raise ValueError(
                "reviews.csv is empty."
            )
 
        # ----------------------------------------------------------
        # REQUIRED COLUMN VALIDATION
        # ----------------------------------------------------------
 
        required_review_columns = [
            "user_id",
            "product_id",
            "rating"
        ]
 
        for col in required_review_columns:
 
            if col not in reviews_df.columns:
 
                raise ValueError(
                    f"Required column '{col}' missing in reviews.csv"
                )
        # ----------------------------------------------------------
        # REQUIRED COLUMN VALIDATION - CLICKSTREAM
        # ----------------------------------------------------------
        required_clickstream_columns = [
            "event_id",
            "session_id",
            "user_id",
            "product_id",
            "event_timestamp",
            "event_type",
            "page",
            "device",
            "browser",
            "traffic_source",
            "dwell_time_sec",
            "recommendation_flag"
        ]
 
        missing_clickstream_columns = [
            col
            for col in required_clickstream_columns
            if col not in clickstream_df.columns
        ]
 
        if missing_clickstream_columns:
            raise ValueError(
                f"Missing columns in clickstream.csv: {missing_clickstream_columns}"
            )
 
        if "event_hour" not in clickstream_df.columns or "event_weekday" not in clickstream_df.columns:
            if "event_timestamp" not in clickstream_df.columns:
                raise ValueError(
                    "clickstream.csv must contain event_timestamp to derive event_hour and event_weekday"
                )
 
            event_timestamp = pd.to_datetime(
                clickstream_df["event_timestamp"],
                errors="coerce"
            )
 
            if "event_hour" not in clickstream_df.columns:
                clickstream_df["event_hour"] = event_timestamp.dt.hour.fillna(0)
 
            if "event_weekday" not in clickstream_df.columns:
                clickstream_df["event_weekday"] = event_timestamp.dt.weekday.fillna(0)
 
        # ----------------------------------------------------------
        # OPTIONAL TYPE CLEANING FOR CLICKSTREAM
        # ----------------------------------------------------------
 
        clickstream_df["dwell_time_sec"] = pd.to_numeric(
            clickstream_df["dwell_time_sec"],
            errors="coerce"
        ).fillna(0)
 
        clickstream_df["recommendation_flag"] = pd.to_numeric(
            clickstream_df["recommendation_flag"],
            errors="coerce"
        ).fillna(0).astype(int)
 
        clickstream_df["event_hour"] = pd.to_numeric(
            clickstream_df["event_hour"],
            errors="coerce"
        ).fillna(0)
 
        clickstream_df["event_weekday"] = pd.to_numeric(
            clickstream_df["event_weekday"],
            errors="coerce"
        ).fillna(0)

        # ----------------------------------------------------------
        # FEATURE 1 : USER ACTIVITY FREQUENCY
        # ----------------------------------------------------------
 
        logger.info(
            "Generating User Activity Frequency...",
            extra={"pipeline_step": "USER_ACTIVITY"}
        )
 
        user_activity = (
            sessions_df.groupby("user_id")
            .size()
            .reset_index(
                name="user_activity_frequency"
            )
        )
 
        # ----------------------------------------------------------
        # FEATURE 2 : AVERAGE USER RATING
        # ----------------------------------------------------------
 
        logger.info(
            "Generating Average User Rating...",
            extra={"pipeline_step": "USER_AVG_RATING"}
        )
 
        user_avg_rating = (
            reviews_df.groupby("user_id")["rating"]
            .mean()
            .reset_index(
                name="user_avg_rating"
            )
        )
 
        # ----------------------------------------------------------
        # BUILD USER FEATURE TABLE
        # ----------------------------------------------------------
 
        transformed_users = users_df.merge(
            user_activity,
            on="user_id",
            how="left"
        )
 
        transformed_users = transformed_users.merge(
            user_avg_rating,
            on="user_id",
            how="left"
        )
 
        transformed_users[
            "user_activity_frequency"
        ] = transformed_users[
            "user_activity_frequency"
        ].fillna(0).astype(int)
 
        transformed_users[
            "user_avg_rating"
        ] = transformed_users[
            "user_avg_rating"
        ].fillna(0.0)
 
        # ----------------------------------------------------------
        # FEATURE 3 : AVERAGE ITEM RATING
        # ----------------------------------------------------------
 
        logger.info(
            "Generating Item Rating Features...",
            extra={"pipeline_step": "ITEM_RATING"}
        )
 
        item_avg_rating = (
            reviews_df.groupby("product_id")["rating"]
            .mean()
            .reset_index(
                name="item_avg_rating"
            )
        )
 
        # ----------------------------------------------------------
        # FEATURE 4 : ITEM POPULARITY
        # ----------------------------------------------------------
 
        item_review_count = (
            reviews_df.groupby("product_id")
            .size()
            .reset_index(
                name="item_interaction_count"
            )
        )
 
        transformed_products = products_df.merge(
            item_avg_rating,
            on="product_id",
            how="left"
        )
 
        transformed_products = transformed_products.merge(
            item_review_count,
            on="product_id",
            how="left"
        )
 
        transformed_products[
            "item_avg_rating"
        ] = transformed_products[
            "item_avg_rating"
        ].fillna(0.0)
 
        transformed_products[
            "item_interaction_count"
        ] = transformed_products[
            "item_interaction_count"
        ].fillna(0).astype(int)
 
        # ----------------------------------------------------------
        # FEATURE 5 : COSINE SIMILARITY
        # ----------------------------------------------------------
 
        logger.info(
            "Generating Item Similarity Matrix...",
            extra={"pipeline_step": "ITEM_SIMILARITY"}
        )
 
        user_item_matrix = reviews_df.pivot_table(
            index="user_id",
            columns="product_id",
            values="rating",
            fill_value=0
        )
 
        similarity_matrix = cosine_similarity(
            user_item_matrix.T
        )
 
        # Create DataFrame with product IDs
        product_ids = user_item_matrix.columns
        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=product_ids,
            columns=product_ids
        )
        
        # Reset index and column names to avoid conflicts during stack
        similarity_df.index.name = None
        similarity_df.columns.name = None
        
        # Stack, reset index, and rename columns
        similarity_long = (
            similarity_df.stack()
            .reset_index(name='similarity_score')
        )
        similarity_long.columns = ['product_id', 'similar_product_id', 'similarity_score']
 
        # Remove self-similarity records
 
        similarity_long = similarity_long[
            similarity_long['product_id']
            != similarity_long['similar_product_id']
        ]
 
        logger.info(
            f"Generated {len(similarity_long)} similarity records.",
            extra={"pipeline_step": "ITEM_SIMILARITY"}
        )

        # ----------------------------------------------------------
        # CLICKSTREAM FEATURES FOR FACT_INTERACTIONS
        # ----------------------------------------------------------
        logger.info(
            "Generating clickstream features for fact_interactions...",
            extra={"pipeline_step": "CLICKSTREAM_FACT_FEATURES"}
        )

        interaction_clickstream = (
            clickstream_df
            .groupby(["user_id", "product_id"])
            .agg(
                click_count=("event_id", "count"),
                avg_dwell_time=("dwell_time_sec", "mean"),
                recommendation_views=("recommendation_flag", "sum"),
                distinct_sessions=("session_id", "nunique"),
                unique_event_types=("event_type", "nunique"),
                avg_event_hour=("event_hour", "mean"),
                avg_event_weekday=("event_weekday", "mean")
            )
            .reset_index()
        )

        logger.info(
            f"Generated {len(interaction_clickstream)} user-product clickstream aggregates.",
            extra={"pipeline_step": "CLICKSTREAM_FACT_FEATURES"}
        )

        # ----------------------------------------------------------
        # ENRICH REVIEWS WITH CLICKSTREAM FEATURES
        # ----------------------------------------------------------
        interactions_sql_payload = reviews_df.merge(
            interaction_clickstream,
            on=["user_id", "product_id"],
            how="left"
        )

        clickstream_fact_columns = [
            "click_count",
            "avg_dwell_time",
            "recommendation_views",
            "distinct_sessions",
            "unique_event_types",
            "avg_event_hour",
            "avg_event_weekday"
        ]

        interactions_sql_payload[clickstream_fact_columns] = (
            interactions_sql_payload[clickstream_fact_columns]
            .fillna(0)
        )

        integer_fact_columns = [
            "click_count",
            "recommendation_views",
            "distinct_sessions",
            "unique_event_types"
        ]
 
        for col in integer_fact_columns:
            interactions_sql_payload[col] = (
                interactions_sql_payload[col]
                .astype(int)
            )
 
        # Keep only columns needed for warehouse fact table
        interactions_columns = [
            "review_id",
            "user_id",
            "product_id",
            "rating",
            "sentiment_encoded",
            "click_count",
            "avg_dwell_time",
            "recommendation_views",
            "distinct_sessions",
            "unique_event_types",
            "avg_event_hour",
            "avg_event_weekday"
        ]
 
        interactions_sql_payload = interactions_sql_payload[
            [
                col
                for col in interactions_columns
                if col in interactions_sql_payload.columns
            ]
        ]

 
        # ----------------------------------------------------------
        # FEATURE STORE TIMESTAMP
        # ----------------------------------------------------------
 
        transformed_users[
            "created_timestamp"
        ] = pd.Timestamp.now()
 
        transformed_products[
            "created_timestamp"
        ] = pd.Timestamp.now()
 
        # ----------------------------------------------------------
        # DATABASE CONNECTION
        # ----------------------------------------------------------
 
        logger.info(
            f"Connecting to warehouse : {db_path}",
            extra={"pipeline_step": "DB_LOAD"}
        )
 
        conn = sqlite3.connect(db_path)
 
        cursor = conn.cursor()
 
        # ----------------------------------------------------------
        # CREATE WAREHOUSE TABLES
        # ----------------------------------------------------------
        
        # Only create columns that will exist in the data
        user_col_types = {
            "user_id": "TEXT PRIMARY KEY",
            "age": "INTEGER",
            "gender": "TEXT",
            "city": "TEXT",
            "membership": "TEXT",
            "signup_year": "INTEGER",
            "user_activity_frequency": "INTEGER",
            "user_avg_rating": "REAL",
            "created_timestamp": "TEXT"
        }
        
        # Filter to only columns that exist in transformed_users
        user_cols = [col for col in user_col_types.keys() if col in transformed_users.columns]
        user_cols_sql = ", ".join([f"{col} {user_col_types[col]}" for col in user_cols])
        
        cursor.execute("DROP TABLE IF EXISTS dim_users")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS dim_users (
                {user_cols_sql}
            )
        """)
        
        product_col_types = {
            "product_id": "TEXT PRIMARY KEY",
            "product_name": "TEXT",
            "category": "TEXT",
            "brand": "TEXT",
            "price": "REAL",
            "item_avg_rating": "REAL",
            "item_interaction_count": "INTEGER",
            "description": "TEXT",
            "created_timestamp": "TEXT"
        }
        
        # Filter to only columns that exist in transformed_products
        product_cols = [col for col in product_col_types.keys() if col in transformed_products.columns]
        product_cols_sql = ", ".join([f"{col} {product_col_types[col]}" for col in product_cols])
        
        cursor.execute("DROP TABLE IF EXISTS dim_products")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS dim_products (
                {product_cols_sql}
            )
        """)
                # ----------------------------------------------------------
        # UPDATED FACT_INTERACTIONS SCHEMA WITH CLICKSTREAM FEATURES
        # ----------------------------------------------------------

        cursor.execute("DROP TABLE IF EXISTS fact_interactions")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_interactions (
                review_id TEXT PRIMARY KEY,
                user_id TEXT,
                product_id TEXT,
                rating REAL,
                sentiment_encoded INTEGER,
                click_count INTEGER,
                avg_dwell_time REAL,
                recommendation_views INTEGER,
                distinct_sessions INTEGER,
                unique_event_types INTEGER,
                avg_event_hour REAL,
                avg_event_weekday REAL,
                FOREIGN KEY(user_id)
                    REFERENCES dim_users(user_id),
                FOREIGN KEY(product_id)
                    REFERENCES dim_products(product_id)
            )
        """)
 
        cursor.execute("DROP TABLE IF EXISTS item_similarity")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_similarity (
                product_id TEXT,
                similar_product_id TEXT,
                similarity_score REAL
            )
        """)
 
        conn.commit()
 
        # ----------------------------------------------------------
        # LOAD DATA INTO WAREHOUSE
        # ----------------------------------------------------------
        
        # Select only columns that exist in the dataframe for users
        users_columns = [
            "user_id",
            "age",
            "gender",
            "city",
            "membership",
            "signup_year",
            "user_activity_frequency",
            "user_avg_rating",
            "created_timestamp"
        ]
        users_sql_payload = transformed_users[[col for col in users_columns if col in transformed_users.columns]]
        
        # Select only columns that exist in the dataframe for products
        products_columns = [
            "product_id",
            "product_name",
            "category",
            "brand",
            "price",
            "item_avg_rating",
            "item_interaction_count",
            "description",
            "created_timestamp"
        ]
        products_sql_payload = transformed_products[[col for col in products_columns if col in transformed_products.columns]]
        
        # Select only columns that exist in the dataframe for interactions
        interactions_columns = [
            "review_id",
            "user_id",
            "product_id",
            "rating",
            "sentiment_encoded",
            "click_count",
            "avg_dwell_time",
            "recommendation_views",
            "distinct_sessions",
            "unique_event_types",
            "avg_event_hour",
            "avg_event_weekday"
        ]
        interactions_sql_payload = interactions_sql_payload[[
            col
            for col in interactions_columns
            if col in interactions_sql_payload.columns
        ]]
 
        users_sql_payload.to_sql(
            "dim_users",
            conn,
            if_exists="replace",
            index=False
        )
 
        products_sql_payload.to_sql(
            "dim_products",
            conn,
            if_exists="replace",
            index=False
        )
 
        interactions_sql_payload.to_sql(
            "fact_interactions",
            conn,
            if_exists="replace",
            index=False
        )
 
        similarity_long.to_sql(
            "item_similarity",
            conn,
            if_exists="replace",
            index=False
        )
 
        conn.commit()
 
        # ----------------------------------------------------------
        # VALIDATION COUNTS
        # ----------------------------------------------------------
 
        db_users_count = pd.read_sql_query(
            "SELECT COUNT(*) cnt FROM dim_users",
            conn
        ).iloc[0]["cnt"]
 
        db_products_count = pd.read_sql_query(
            "SELECT COUNT(*) cnt FROM dim_products",
            conn
        ).iloc[0]["cnt"]
 
        db_interactions_count = pd.read_sql_query(
            "SELECT COUNT(*) cnt FROM fact_interactions",
            conn
        ).iloc[0]["cnt"]
 
        similarity_count = pd.read_sql_query(
            "SELECT COUNT(*) cnt FROM item_similarity",
            conn
        ).iloc[0]["cnt"]

        fact_schema = pd.read_sql_query(
            "PRAGMA table_info(fact_interactions)",
            conn
        )

 
        conn.close()
 
        # ----------------------------------------------------------
        # SUMMARY OUTPUT
        # ----------------------------------------------------------
 
        print("\n" + "=" * 70)
        print("TASK 6 FEATURE ENGINEERING COMPLETED")
        print("=" * 70)
        print(f"Users Loaded             : {db_users_count:,}")
        print(f"Products Loaded          : {db_products_count:,}")
        print(f"Interactions Loaded      : {db_interactions_count:,}")
        print(f"Similarity Records       : {similarity_count:,}")
        print(f"Warehouse Database       : {db_path}")
        print("-" * 70)
        print("fact_interactions columns:")
        print(", ".join(fact_schema["name"].tolist()))
        print("=" * 70 + "\n")
 
        logger.info(
            "Feature Engineering completed successfully.",
            extra={"pipeline_step": "FEATURE_COMPLETE"}
        )
 
    except FileNotFoundError as e:
 
        logger.error(
            f"File Not Found: {e}",
            extra={"pipeline_step": "ERROR"}
        )
        raise
 
    except pd.errors.EmptyDataError as e:
 
        logger.error(
            f"Empty File Error: {e}",
            extra={"pipeline_step": "ERROR"}
        )
        raise
 
    except sqlite3.Error as e:
 
        logger.error(
            f"Database Error: {e}",
            extra={"pipeline_step": "ERROR"}
        )
        raise
 
    except ValueError as e:
 
        logger.error(
            f"Validation Error: {e}",
            extra={"pipeline_step": "ERROR"}
        )
        raise
 
    except Exception as e:
 
        logger.exception(
            f"Unexpected Error: {e}",
            extra={"pipeline_step": "ERROR"}
        )
        raise
 
 
if __name__ == "__main__":
    run_feature_pipeline()