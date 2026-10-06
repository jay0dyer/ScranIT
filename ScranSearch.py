import sqlite3
import sqlite_vec
from sentence_transformers import SentenceTransformer

class ScranSearchEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.conn = sqlite3.connect("ItemInfo.db")
        self.conn.enable_load_extension(True)
        self.conn.row_factory = sqlite3.Row
        sqlite_vec.load(self.conn)
        self.cursor = self.conn.cursor()

    def Search(self, query, sort="Relevance", limit=10, max_distance=0.50, initial_pool=50):
        query_vector = self.model.encode(query)

        sort_options = {
            'PriceLTH': "CAST(REPLACE(Price, '£', '') AS REAL) ASC",
            'PriceHTL': "CAST(REPLACE(Price, '£', '') AS REAL) DESC",
            'Relevance': 'distance ASC'
        }
        order_clause = sort_options.get(sort, 'distance ASC')
        # Prepare string for SQL LIKE wildcard search
        like_query = f"%{query}%"
        serialized_vec = sqlite_vec.serialize_float32(query_vector)

        sql = f"""
                WITH top_matches AS (
                    SELECT 
                        info.Name AS Item,
                        info.Description,
                        info.Price,
                        rest.Name AS Restaurant,
                        rest.StreetAddress,
                        rest.Postcode,
                        rest.Image,
                        vec_distance_cosine(vec.embedding, ?) AS distance,
                        -- 1 if query term is in Name or Description, 0 otherwise
                        (CASE 
                            WHEN info.Name LIKE ? OR info.Description LIKE ? THEN 1 
                            ELSE 0 
                        END) AS has_keyword
                    FROM item_vectors vec
                    JOIN ItemInfo info ON vec.item_id = info.id
                    LEFT JOIN RestaurantInfo rest ON info.ScranHash = rest.ScranHash
                    WHERE 
                        -- Keep items that explicitly mention the word OR pass a vector cutoff
                        info.Name LIKE ? 
                        OR info.Description LIKE ? 
                        OR vec_distance_cosine(vec.embedding, ?) < ?
                    ORDER BY 
                        has_keyword DESC,  -- Prioritize exact text matches in candidate pool
                        distance ASC
                    LIMIT ?
                )
                SELECT Item, Description, Price, Restaurant, StreetAddress, Postcode, Image, distance
                FROM top_matches
                ORDER BY {order_clause}
                LIMIT ?
            """

        self.cursor.execute(
            sql,
            (
                serialized_vec,  # 1: vec_distance in SELECT
                like_query,  # 2: Name LIKE in CASE
                like_query,  # 3: Description LIKE in CASE
                like_query,  # 4: Name LIKE in WHERE
                like_query,  # 5: Description LIKE in WHERE
                serialized_vec,  # 6: vec_distance in WHERE
                max_distance,  # 7: distance threshold (e.g. 0.45)
                initial_pool,  # 8: CTE candidate pool size
                limit  # 9: Final result set limit
            )
        )
        result = [dict(row) for row in self.cursor.fetchall()]
        return result

if __name__ == "__main__":
    import json
    engine = ScranSearchEngine()
    print(json.dumps(engine.Search("cheese"), indent=2))