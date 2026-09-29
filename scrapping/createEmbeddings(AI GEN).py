import numpy as np
from sentence_transformers import SentenceTransformer
import sqlite3
import sqlite_vec

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = sqlite3.connect("ItemInfo.db")
conn.enable_load_extension(True)
sqlite_vec.load(conn)
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS item_vectors
               (
                   item_id INTEGER PRIMARY KEY,
                   embedding BLOB
               )
               """)

# 3. Fetch all items that don't have embeddings yet
cursor.execute("SELECT id, Name || ' - ' || Description FROM ItemInfo")
rows = cursor.fetchall()

BATCH_SIZE = 64  # Adjust based on your computer's RAM

print(f"Processing {len(rows)} items...")

# 4. Process the data in chunks
for i in range(0, len(rows), BATCH_SIZE):
    # Slice the rows into a batch
    batch = rows[i:i + BATCH_SIZE]

    ids = [row[0] for row in batch]
    texts = [row[1] for row in batch]

    # Generate vectors for the entire batch at once
    embeddings = model.encode(texts, batch_size=BATCH_SIZE)

    # Prepare data for insertion (sqlite-vec requires float32 serialization)
    update_data = [
        (item_id, sqlite_vec.serialize_float32(vector))
        for item_id, vector in zip(ids, embeddings)
    ]

    # 5. Insert vectors back into the database
    cursor.executemany(
        "INSERT OR REPLACE INTO item_vectors (item_id, embedding) VALUES (?, ?)",
        update_data
    )

    print(f"Processed {i + len(batch)} / {len(rows)}")

conn.commit()
print("Database embedding complete!")