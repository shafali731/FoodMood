from __future__ import print_function
import os
from flask import Flask, request, render_template, session, redirect, flash, url_for
from util import sample
from urllib.parse import quote

import argparse
import json
import pprint
import requests
import sys
import urllib
import random


app=Flask(__name__)

@app.route('/')
def start():
    return render_template('new_welcome.html')
@app.route('/result/<term>/<place>/<price>')
def welcome(term,place,price):
    ret = sample.query_api(term,place,price)
    y = json.loads(ret)
    t = list(y.values())
    amount = t[-1]
    lats = ["" for p in range(int(amount))]
    longs = ["" for p in range(int(amount))]
    resturs_urls = ["" for x in range(int(amount))]
    resturs_names = ["" for x in range(int(amount))]
    resturs_img= ["" for x in range(int(amount))]
    # locations = []
    # print(locations)
    for k in range(int(amount)):
        lats[k]= y[str(k)]["coordinates"]["latitude"]
        longs[k] = y[str(k)]["coordinates"]["longitude"]
        resturs_names[k]= y[str(k)]['name']
        resturs_urls[k]= y[str(k)]['url']
        resturs_img[k]= y[str(k)]['image_url']
    print(lats)
    # # print(page)
    # if(page==1):
    #     lats_1 = ["" for p in range(10)]
    #     longs_1 = ["" for p in range(10)]
    #     resturs_urls_1 = ["" for x in range(10)]
    #     resturs_names_1 = ["" for x in range(10)]
    #     resturs_img_1= ["" for x in range(10)]
    #     for q in range(10):
    #         lats_1[q] = lats[q]
    #         longs_1[q] = longs[q]
    #         resturs_urls_1[q] = resturs_urls[q]
    #         resturs_names_1[q] = resturs_names[q]
    #         resturs_img_1[q] = resturs_img[q]
    #     print(resturs_names_1)
    #     return render_template('index.html', imgs= resturs_img_1, resturs_urls=resturs_urls_1, resturs_names=resturs_names_1,ret =y, lats=lats, longs= longs, amount = 10,page=1, term = term, place = place)
    # if(page==2):
    #     lats_1 = ["" for p in range(10)]
    #     longs_1 = ["" for p in range(10)]
    #     resturs_urls_1 = ["" for x in range(10)]
    #     resturs_names_1 = ["" for x in range(10)]
    #     resturs_img_1= ["" for x in range(10)]
    #     for q in range(10):
    #         lats_1 = lats[10:20]
    #         longs_1 = longs[10:20]
    #         resturs_urls_1 = resturs_urls[10:20]
    #         resturs_names_1 = resturs_names[10:20]
    #         resturs_img_1 = resturs_img[10:20]
    #     return render_template('index.html', imgs= resturs_img_1, resturs_urls=resturs_urls_1, resturs_names=resturs_names_1,ret =y, lats=lats, longs= longs, amount = 20,page=2, term = term, place = place)
    return render_template('index.html', imgs= resturs_img, resturs_urls=resturs_urls, resturs_names=resturs_names,ret =y, lats=lats, longs= longs, amount = int(amount), term = term, place = place, price = price)
    # @app.route('/result/<term>/<place>')
    # def welcome(term,place):
    #     ret = sample.query_api(term,place)
    #     y = json.loads(ret)
    #     t = list(y.values())
    #     amount = t[-1]
    #     lats = ["" for p in range(int(amount))]
    #     longs = ["" for p in range(int(amount))]
    #     resturs_urls = ["" for x in range(int(amount))]
    #     resturs_names = ["" for x in range(int(amount))]
    #     resturs_img= ["" for x in range(int(amount))]
    #     # locations = []
    #     # print(locations)
    #     for k in range(int(amount)):
    #         lats[k]= y[str(k)]["coordinates"]["latitude"]
    #         longs[k] = y[str(k)]["coordinates"]["longitude"]
    #         # resturs[k]= y[str(k)]['name']
    #         # print(locations[k])
    #     # print(t[0])
    #     amount_double = (int(amount))
    #     u =0
    #     # while(u <amount_double):
    #     #     resturs_urls[u]= y[str(u)]['url']
    #     #     u+=1
    #     # print("u:  ")
    #     # print(u)
    #     # print(amount_double*2)
    #     for k in range(int(amount)):
    #         resturs_names[k]= y[str(k)]['name']
    #         resturs_urls[k]= y[str(k)]['url']
    #         resturs_img[k]= y[str(k)]['image_url']
    #     # while(u<(amount_double*2)):
    #     #     resturs[u]= y[str(u)]['name']
    #     #     u+=1
    #         # resturs[u+1]=y[str(u)]
    #         # u+=2
    #     # print(locations)
    #     # print(lats)
    #     # print(y)
    #     # print(y["1"]['name'])
    #     print(resturs_names)
    #     # print(amount)
    #     return render_template('index.html', imgs= resturs_img, resturs_urls=resturs_urls, resturs_names=resturs_names,ret =y, lats=lats, longs= longs, amount = int(amount))
# @app.route('/result/<term>/<place>/<check_one>/<check_two>/<check_three>/<check_four>')

@app.route('/sort_price', methods=["GET"])
def results_price():
    term = request.args.get('term')
    loc = request.args.get('place')
    print("term:" + term)
    print("place:" + loc)
    # term = term
    # loc = place
    first= request.args.get('one')
    second= request.args.get('two')
    third= request.args.get('three')
    fourth= request.args.get('four')
    prices = ""
    print(second)
    if(first==None and second == None and third == None and fourth == None):
        prices = "1,2,3,4"
    else:
        if(first != None):
            prices += first + ","
        if(second != None):
            prices += second+ ","
        if(third != None):
            prices += third+ ","
        if(fourth != None):
            prices += fourth+ ","
        prices = prices[:-1]
    print("prices" + prices)
    return redirect(url_for('welcome',term=term,place=loc,price = prices))
# @app.route('/random/<term>/<place>/<price>')
# def random_res(term,place,price):
#     ret = sample.query_api(term,place,price)
#     y = json.loads(ret)
#     t = list(y.values())
#     amount = t[-1]
#     lats = ["" for p in range(int(amount))]
#     longs = ["" for p in range(int(amount))]
#     resturs_urls = ["" for x in range(int(amount))]
#     resturs_names = ["" for x in range(int(amount))]
#     resturs_img= ["" for x in range(int(amount))]
#     # locations = []
#     # print(locations)
#     for k in range(int(amount)):
#         lats[k]= y[str(k)]["coordinates"]["latitude"]
#         longs[k] = y[str(k)]["coordinates"]["longitude"]
#         resturs_names[k]= y[str(k)]['name']
#         resturs_urls[k]= y[str(k)]['url']
#         resturs_img[k]= y[str(k)]['image_url']
#     rand_num = random.randrange(int(amount))
#
#     latit = lats[rand_num]
#     longit = longs[rand_num]
#     rand_resturs_name= resturs_names[rand_num]
#     rand_resturs_url= resturs_urls[rand_num]
#     rand_resturs_img= resturs_imgs[rand_num]
#     return render_template('random.html',lats = lait, longs = longit, term=term, place=place, price=price,rand_resturs_name=rand_resturs_name,rand_resturs_url=rand_resturs_url,rand_resturs_img=rand_resturs_img)

@app.route('/res/<term>/<place>')
def search_result(term,place):
    ret = sample.query_api(term, place)
    y = json.loads(ret)
    t = list(y.values())
    # amount = y.slice(-1);
    # amount = sorted(y.keys())[-4]
    # amount = sorted(y.keys())
    amount = t[-1]
    # for p in range(int(amount)):
    #     lats[p] = ""
    #     longs[p] = ""
    lats =["" for p in range(int(amount))]
    longs =["" for p in range(int(amount))]
    for a in range(int(amount)):
        lats[a] = y[str(a)]["coordinates"]['latitude']
        longs[a] = y[str(a)]["coordinates"]['longitude']
    a = y['2']["coordinates"]['latitude']
    b = y['2']['coordinates']['longitude']

    return render_template('index.html',amount = amount,ret = ret, a= a, b= b, lats= lats,longs=longs)
# def search_result():
#     ret = sample.query_api("turkish","New York")
#     y = json.loads(ret)
#     t = list(y.values())
#     # amount = y.slice(-1);
#     # amount = sorted(y.keys())[-4]
#     # amount = sorted(y.keys())
#     amount = t[-1]
#     # for p in range(int(amount)):
#     #     lats[p] = ""
#     #     longs[p] = ""
#     lats =["" for p in range(int(amount))]
#     longs =["" for p in range(int(amount))]
#     for a in range(int(amount)):
#         lats[a] = y[str(a)]["coordinates"]['latitude']
#         longs[a] = y[str(a)]["coordinates"]['longitude']
#     a = y['2']["coordinates"]['latitude']
#     b = y['2']['coordinates']['longitude']
#
#     return render_template('index.html',amount = amount,ret = ret, a= a, b= b, lats= lats,longs=longs)

    # return render_template('index.html', ret = ret)


@app.route('/search', methods=["GET"])
def search():
    term = request.args.get('term')
    loc = request.args.get('place')
    if(loc == ""):
        loc = "new york"
    if(term == ""):
        term = "indian"
    price = "1,2,3,4"
    return redirect(url_for('welcome',term=term,place=loc, price=price))

# @app.route('/searchp', methods=["GET"])
# def searchp():
#     term = request.args.get('term')
#     loc = request.args.get('place')
#     prices = requests.args.get('price')
#     if(loc == ""):
#         loc = "new york"
#     if(term == ""):
#         term = "indian"
#     # if(price =)
#     return redirect(url_for('welcome',term=term,place=loc))

# @app.route('/search', methods=["GET"])
# def search():
#     '''If search query is for books, then redirects to book_search.
#     If search query is for books, then redirects to movie_search.'''
#     place = request.args.get("h")
#     query =request.args.get("query").replace(" " , "+")
#     if(query==""):
#         return redirect(url_for('index'))
#     # if(type == "Books"):
#     #     return redirect(url_for('book_search', query=query))
#     # else:
#     #     return redirect(url_for('movie_search', query=query))


if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()
