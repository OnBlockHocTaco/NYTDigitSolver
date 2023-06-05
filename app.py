from flask import Flask, render_template, redirect, url_for, request, session
from main import bfs_digit_solver

app = Flask(__name__)
app.secret_key = "BBBBBBBBB"

ordinal_words = ["first", "second", "third", "fourth", "fifth", "sixth"]

@app.route("/", methods=["POST", "GET"])
def insert():
    if request.method == "POST":
        trgt = request.form["trgt"]
        session["trgt"] = int(trgt)
        #Grab the Target Number from the HTML Form
        usable_numbers = [int(request.form[ordnl_word]) for ordnl_word in ordinal_words]
        session["usable_numbers"] = usable_numbers
        #Grab the Usable Numbers from the HTML Form
        return redirect(url_for("result"))
    else:
        return render_template("index.html")


@app.route("/result")
def result():
    if "trgt" in session and "usable_numbers" in session: #Verify that a set of numbers exists
        trgt = session["trgt"]
        solution = bfs_digit_solver(trgt, session["usable_numbers"])
        return render_template("result.html", target=trgt, steps=solution)
    else:
        return redirect(url_for("insert"))


if __name__ == "__main__":
    app.run(debug=True, port=3000)
