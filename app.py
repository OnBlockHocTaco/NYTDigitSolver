from flask import Flask, render_template, redirect, url_for, request, session
from solver import bfs_digit_solver, bfs_digit_solver_steps

app = Flask(__name__)
app.secret_key = "BBBBBBBBB"

ordinal_words = ["first", "second", "third", "fourth", "fifth", "sixth"]

@app.route("/", methods=["POST", "GET"])
def insert():
    if request.method == "POST":
        trgt = request.form["trgt"]
        if trgt == '':
            session["trgt"] = 0
        else:
            session["trgt"] = int(trgt)
        #Grab the Target Number from the HTML Form
        #usable_numbers = [int(request.form[ordnl_word]) for ordnl_word in ordinal_words]
        usable_numbers = [0 if request.form[ordnl_word] == '' else
                          int(request.form[ordnl_word]) for ordnl_word in ordinal_words]
        session["usable_numbers"] = usable_numbers
        #Grab the Usable Numbers from the HTML Form
        return redirect(url_for("result"))
    else:
        return render_template("input_page.html")

@app.route("/result")
def result():
    if "trgt" in session and "usable_numbers" in session: #Verify that a set of numbers exists
        trgt = session["trgt"]
        #solution = bfs_digit_solver(trgt, session["usable_numbers"])
        solution = bfs_digit_solver_steps(trgt, session["usable_numbers"])
        return render_template("result.html", target=trgt, steps=solution, length = len(solution))
    else:
        return redirect(url_for("insert"))

if __name__ == "__main__":
    app.run(debug=True, port=3000)
