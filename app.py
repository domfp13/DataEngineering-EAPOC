# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Luis Enrique Fuentes Plata

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    my_name = "Enrique Plata"
    number_list = [1,2,3]
    return render_template("index.html", number_list=number_list)

@app.route("/services")
def services():
    name = "Enrique"
    return render_template("services.html", name=name)

@app.route("/submitted")
def submitted():
    info_1 = request.args.get('info_1')
    info_2 = request.args.get('info_2')
    return render_template("submitted.html", info_1=info_1, info_2=info_2)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))
    #app.run(debug=True, host='0.0.0.0', port=8080) # run without container