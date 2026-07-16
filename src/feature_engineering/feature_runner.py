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
 
        # ----------------------------------------------------------
        # INPUT FILES
        # ----------------------------------------------------------
 
        users_file = processed_dir / "users" / "users.csv"
        products_file = processed_dir / "products" / "products.csv"
        reviews_file = processed_dir / "reviews" / "reviews.csv"
        sessions_file = processed_dir / "sessions" / "sessions.csv"
 
        # ----------------------------------------------------------
        # FILE VALIDATION
        # ----------------------------------------------------------
 
        required_files = [
            users_file,
            products_file,
            reviews_file,
            sessions_file
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
 
        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=user_item_matrix.columns,
            columns=user_item_matrix.columns
        )
 
        similarity_long = (
            similarity_df.stack()
            .reset_index()
        )
 
        similarity_long.columns = [
            "product_id",
            "similar_product_id",
            "similarity_score"
        ]
 
        # Remove self-similarity records
 
        similarity_long = similarity_long[
            similarity_long["product_id"]
            != similarity_long["similar_product_id"]
        ]
 
        logger.info(
            f"Generated {len(similarity_long)} similarity records."
        )
 
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
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_users (
                user_id TEXT PRIMARY KEY,
                age INTEGER,
                gender TEXT,
                city TEXT,
                membership TEXT,
                signup_year INTEGER,
                user_activity_frequency INTEGER,
                user_avg_rating REAL,
                created_timestamp TEXT
            )
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                brand TEXT,
                price REAL,
                item_avg_rating REAL,
                item_interaction_count INTEGER,
                description TEXT,
                created_timestamp TEXT
            )
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_interactions (
                review_id TEXT PRIMARY KEY,
                user_id TEXT,
                product_id TEXT,
                rating REAL,
                sentiment_encoded INTEGER,
                FOREIGN KEY(user_id)
                    REFERENCES dim_users(user_id),
                FOREIGN KEY(product_id)
                    REFERENCES dim_products(product_id)
            )
        """)
 
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
 
        users_sql_payload = transformed_users[[
            "user_id",
            "age",
            "gender",
            "city",
            "membership",
            "signup_year",
            "user_activity_frequency",
            "user_avg_rating",
            "created_timestamp"
        ]]
 
        products_sql_payload = transformed_products[[
            "product_id",
            "product_name",
            "category",
            "brand",
            "price",
            "item_avg_rating",
            "item_interaction_count",
            "description",
            "created_timestamp"
        ]]
 
        interactions_sql_payload = reviews_df[[
            "review_id",
            "user_id",
            "product_id",
            "rating",
            "sentiment_encoded"
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
 
        conn.close()
 
        # ----------------------------------------------------------
        # SUMMARY OUTPUT
        # ----------------------------------------------------------
 
        print("\n" + "=" * 65)
        print("TASK 6 FEATURE ENGINEERING COMPLETED")
        print("=" * 65)
        print(f"Users Loaded            : {db_users_count:,}")
        print(f"Products Loaded         : {db_products_count:,}")
        print(f"Interactions Loaded     : {db_interactions_count:,}")
        print(f"Similarity Records      : {similarity_count:,}")
        print(f"Warehouse Database      : {db_path}")
        print("=" * 65 + "\n")
 
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