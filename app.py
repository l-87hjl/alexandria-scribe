from flask import Flask, render_template, send_from_directory

app = Flask(__name__, template_folder="templates")

@app.route("/")
def landing():
    # Reuse the same landing content conceptually; backend landing
    return render_template("landing.html")

@app.route("/disassembler")
def disassembler():
    return render_template("disassembler.html")

@app.route("/fragments")
def fragments():
    return render_template("fragments.html")

@app.route("/recombulator")
def recombulator():
    return render_template("recombulator.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
