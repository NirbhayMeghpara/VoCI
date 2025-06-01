from flask import Blueprint, request, jsonify
from services.analyzer import analyze_reviews_file

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze-reviews', methods=['POST'])
def analyze_reviews():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        response = analyze_reviews_file(file)
        return jsonify(response)
    except Exception as e:
        import traceback
        print("Error occurred:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
