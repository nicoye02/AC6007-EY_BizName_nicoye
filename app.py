# flask

from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

if __name__ == "__main__":  #__xxx__: means reserved for python to use
    app.run()