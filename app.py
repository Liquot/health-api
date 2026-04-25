from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Health Analyzer Running 🚀"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "API working ✅"})


# ✅ THIS WAS MISSING
@app.route("/analyze", methods=["POST"])
def analyze():
    print("API HIT")

    # import here to avoid crash at startup
    from reportanalyser import analyze_report

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        file_path = "uploaded_report.jpg"
        file.save(file_path)

        print("📂 File saved:", file_path)

        result = analyze_report(file_path)

        print("✅ RESULT:", result)

        return jsonify(result)

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ✅ THIS MUST BE OUTSIDE ALL FUNCTIONS
if __name__ == "__main__":
    print("🚀 STARTING FLASK SERVER...")
    app.run(debug=True)