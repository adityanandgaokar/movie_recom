# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 18:03:29 2021

@author: Aditya
"""


from flask import Flask, flash, request, redirect, url_for, render_template
from prediction import recom



app= Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/search_movie', methods=['GET', 'POST'])
def search_movie():
    if request.method == 'POST':
        movies = recom(request.form.get("query"))
        
        return render_template('results.html', query=request.form.get("query"), movies=movies)
            

    elif request.method == 'GET':
        return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)


