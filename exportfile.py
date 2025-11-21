import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore
import json
import os

# ---------------------- Initialize Firebase ----------------------
cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------------- Helper Function ----------------------
def export_collection_to_json(collection_name):
    """
    Exports a Firestore collection to a JSON file in the current folder.
    """
    print(f"🔄 Exporting collection '{collection_name}'...")

    collection_ref = db.collection(collection_name)
    docs = list(collection_ref.stream())

    if not docs:
        print(f"⚠️ No documents found in {collection_name}")
        return

    data = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        data.append(doc_dict)

    file_path = os.path.join(os.getcwd(), f"{collection_name}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ '{collection_name}.json' exported with {len(data)} documents.")


# ---------------------- Main ----------------------
if __name__ == "__main__":
    collections = ["users", "recipes", "interactions"]

    for col in collections:
        export_collection_to_json(col)

    print("🎉 All collections exported successfully!")

