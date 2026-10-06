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

    def Search(self, query, limit=5):
        query_vector = self.model.encode(query)
        self.cursor.execute("""
            SELECT 
            info.Name AS Item,
            info.Description,
            info.Price,
            rest.Name AS Restaurant,
            rest.StreetAddress,
            rest.Postcode,
            rest.Image,
            vec_distance_cosine(vec.embedding, ?) AS distance
        FROM item_vectors vec
        JOIN ItemInfo info ON vec.item_id = info.id
        LEFT JOIN RestaurantInfo rest ON info.ScranHash = rest.ScranHash
        ORDER BY distance ASC 
        LIMIT ?
            """,
            (sqlite_vec.serialize_float32(query_vector), limit)
        )

        unsorted = [dict(row) for row in self.cursor.fetchall()]
        return unsorted

if __name__ == "__main__":
    import json
    engine = ScranSearchEngine()
    print(json.dumps(engine.Search("cheese"), indent=2))