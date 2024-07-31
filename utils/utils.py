import numpy as np
from lightfm import LightFM
import pickle
import os 
from dotenv import load_dotenv
import logging

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

MODEL_PATH = os.getenv('MODEL_PATH')
MODEL_UTILS_PATH = os.getenv('MODEL_UTILS_PATH')
NUM_RECOMMENDATIONS=os.getenv('NUM_RECOMMENDATIONS')

# Load model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
logging.info("Model loaded successfully")

with open(MODEL_UTILS_PATH, 'rb') as f:
    model_utils = pickle.load(f)

# get values from model utils
user_id_mapping, item_id_mapping, item_representations = model_utils.values()
# Create reverse mapping for models internal indices to real item ids
reverse_item_id_mapping = {v: k for k, v in item_id_mapping.items()}

# Get N item recommendation for given user id
def get_recommendation(user_id, N=NUM_RECOMMENDATIONS):
    if user_id not in user_id_mapping:
        raise KeyError(f"User ID {user_id} either not valid or not an old user. Please provide a valid user ID or use similar endpoint to get recommendations for a new user.")
    
    # Get model's internal id for given user_id
    user_idx = user_id_mapping[user_id]

    # Get top N recommendation
    item_ids = np.arange(len(item_id_mapping))
    scores = model.predict(user_idx, item_ids)
    top_items = np.argsort(-scores)[:N]

    # Extract original ids of items
    recommended_items = [reverse_item_id_mapping[item_id] for item_id in top_items]
    
    return recommended_items

# Get similar items for given item_id.
def get_similar_items(item_id, N=NUM_RECOMMENDATIONS):
    if item_id not in item_id_mapping:
        raise KeyError(f"Item ID {item_id} not found. Please provide a valid item ID.")

    # Get model's internal id for given item_id
    item_idx = item_id_mapping[item_id]

    # Cosine similarity
    scores = item_representations.dot(item_representations[item_idx, :])
    item_norms = np.linalg.norm(item_representations, axis=1)

    scores /= item_norms
    best = np.argpartition(scores, -N)[-N:]
    similar = sorted(zip(best, scores[best]/ item_norms[item_idx] ), key=lambda x: -x[1])

    similar_idx = [x[0] for x in similar]
    recommended_items = [reverse_item_id_mapping[item_idx] for item_idx in similar_idx]
    
    return recommended_items


