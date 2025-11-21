import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore

# -----------------------------
# Initialize Firebase
# -----------------------------

# Path to your service account key
cred = credentials.Certificate("ServiceAccountKey.json")

# Initialize the Firebase app
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

print("🔥 Firebase Initialization Successful!")
