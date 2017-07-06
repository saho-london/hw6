#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import urllib, json
import sys

app = Flask(__name__)
WORLD = "pokemon"

# from https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([(start, "None")])
    visited = []
    visited.append(start)
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1][0]
        # path found
        if node == end:
            del path[0]
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for line in graph:
            if node in line['Stations']:
                index = line['Stations'].index(node)
                if index != 0:
                    pre = line['Stations'][index - 1]
                    if pre not in visited:
                        visited.append(pre)
                        new_path = list(path)
                        new_path.append((pre, line['Name']))
                        queue.append(new_path)
                if index != len(line['Stations']) - 1:
                    fwd = line['Stations'][index - 1]
                    if fwd not in visited:
                        visited.append(fwd)
                        new_path = list(path)
                        new_path.append((fwd, line['Name']))
                        queue.append(new_path)
                
    return "No path found"     


@app.route('/', methods=['GET', 'POST'])
def root():

    global WORLD
    WORLD = request.form.get('world', WORLD)

    url = {"pokemon":"http://pokemon.fantasy-transit.appspot.com/net?format=json",
            "tokyo":"http://fantasy-transit.appspot.com/net?format=json",
            "alice":"http://alice.fantasy-transit.appspot.com/net?format=json",
            "nausicaa":"http://nausicaa.fantasy-transit.appspot.com/net?format=json",
            "lotr":"http://lotr.fantasy-transit.appspot.com/net?format=json"}
    neturl = urllib.urlopen(url[WORLD])
    net = json.loads(neturl.read())
    
    towns = []
    for line in net:
        for town in line['Stations']:
            if town not in towns:
                towns.append(town)
                
    
    
    frIndex = request.form.get('fr', default=1, type=int)
    toIndex = request.form.get('to', default=0, type=int)
    
    fr = towns[frIndex - 1]
    to = towns[toIndex - 1]
    
    path = bfs(net, fr, to)
    
    return render_template("hello.html", towns=towns, fr=fr, to=to, path=path, world=WORLD)


