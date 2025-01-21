from flask import Flask, redirect, request, session, render_template, jsonify, send_file
from utils import decode_binary_file, encode_data_to_binary_file
import io
import hashlib


app = Flask(__name__)
app.secret_key = "w0w"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        file = request.files.get("file_to_decode")
        if not file:
            return redirect("/")

        file_decoded = decode_binary_file(file.stream)
        if "uploaded_files" not in session:
            session["uploaded_files"] = None

        session["uploaded_files"] = file_decoded

        return render_template("index.html", data=session["uploaded_files"])

    data = session.get("uploaded_files", [])
    return render_template("index.html", data=data)


@app.route("/save", methods=["POST"])
def save_data():
    updated_data = request.json.get("data")
    if not updated_data:
        return jsonify({"error": "No data provided"}), 400

    binary_file = io.BytesIO()
    encode_data_to_binary_file(updated_data, binary_file)
    binary_file.seek(0)

    return send_file(
        binary_file,
        as_attachment=True,
        download_name="updated_data.bin",
        mimetype="application/octet-stream",
    )


@app.route("/compare_hashes", methods=["POST", "GET"])
def compare_hashes():
    if request.method == "POST":
        if "file1" not in request.files or "file2" not in request.files:
            return jsonify({"error": "Please upload two files."}), 400

        file1 = request.files["file1"].read()
        file2 = request.files["file2"].read()

        hash1 = hashlib.sha256(file1).hexdigest()
        hash2 = hashlib.sha256(file2).hexdigest()

        result = {"hash1": hash1, "hash2": hash2, "match": hash1 == hash2}

        return jsonify(result)

    return render_template("compare_hashes.html")


@app.route("/clear", methods=["POST"])
def clear_session():
    session.pop("uploaded_files", None)
    return redirect("/")


# TODO: multiple file upload?
# TODO: limits values for each type
# TODO: proper handling of float numbers

if __name__ == "__main__":
    app.run(debug=True)
