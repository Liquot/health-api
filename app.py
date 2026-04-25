from flask import Flask, request, jsonify
from reportanalyser import analyze_report
import os

app = Flask(__name__)

# Allow file uploads (up to 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# ✅ Home route (for testing API is alive)
@app.route('/')
def home():
    return "Health API is running 🚀"


# ✅ Main API endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Debug log (check Railway logs)
        print("FILES RECEIVED:", request.files)

        # ❌ If no file
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        # ❌ If empty filename
        if file.filename == '':
            return jsonify({"error": "Empty file"}), 400

        # ✅ Save file temporarily
        file_path = "temp.jpg"
        file.save(file_path)

        # ✅ Process report
        result = analyze_report(file_path)

        return jsonify(result)

    except Exception as e:
        # 🔴 Catch all errors
        return jsonify({"error": str(e)}), 500

    finally:
        # 🧹 Cleanup file
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")


# ✅ Run locally
if __name__ == '__main__':
    app.run(debug=True)