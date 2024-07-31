from flask import Flask, request, jsonify
from utils.utils import get_recommendation, get_similar_items
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv
import os

# Get default number for recommendations from .env file. If not set, default to 10
load_dotenv()
NUM_RECOMMENDATIONS = int(os.getenv('NUM_RECOMMENDATIONS', 10))

app = Flask(__name__)

@app.route("/")
def hello():
    return "I am alive!"

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    if not user_id:
        raise BadRequest("User ID is required")

    N = request.args.get('N', default=NUM_RECOMMENDATIONS, type=int)  # Default to NUM_RECOMMENDATIONS if not provided

    try:
        recommendations = get_recommendation(user_id, N=N)
    except KeyError:
        return jsonify({'error': 'User ID not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'user_id': user_id, 'recommended_items': recommendations})

@app.route('/similar', methods=['GET'])
def similar():
    item_id = request.args.get('item_id')
    
    if not item_id:
        raise BadRequest("Item ID is required")

    N = request.args.get('N', default=NUM_RECOMMENDATIONS, type=int)  # Default to NUM_RECOMMENDATIONS if not provided

    try:
        similar_items = get_similar_items(item_id, N=N)
    except KeyError:
        return jsonify({'error': 'Item ID not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'item_id': item_id, 'similar_items': similar_items})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)