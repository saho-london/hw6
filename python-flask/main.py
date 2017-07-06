#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():

    pato = request.form.get('a', u"パトカー")
    taku = request.form.get('b', u"タクシー")
    
    pata = ""
    
    for i in range(min(len(pato), len(taku))):
        pata = pata + pato[i]
        pata = pata + taku[i]
    
    return render_template("hello.html", pata=pata)


