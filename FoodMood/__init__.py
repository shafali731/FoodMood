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
@app.route('/result/<term>/<place>/<price>/<open>')
def welcome(term,place,price,open):
    ret = sample.query_api(term,place,price,open)
    if(ret == None):
        return render_template('error.html')
    print(ret)
    y = json.loads(ret)
    t = list(y.values())
    amount = t[-1]
    lats = ["" for p in range(int(amount))]
    longs = ["" for p in range(int(amount))]
    resturs_urls = ["" for x in range(int(amount))]
    resturs_names = ["" for x in range(int(amount))]
    resturs_img= ["" for x in range(int(amount))]
    phone= ["" for x in range(int(amount))]
    price_list= ["" for x in range(int(amount))]
    ratings= ["" for x in range(int(amount))]
    # locations = []
    # print(locations)
    for k in range(int(amount)):
        lats[k]= y[str(k)]["coordinates"]["latitude"]
        longs[k] = y[str(k)]["coordinates"]["longitude"]
        resturs_names[k]= y[str(k)]['name']
        resturs_urls[k]= y[str(k)]['url']
        resturs_img[k]= y[str(k)]['image_url']
        phone[k] = y[str(k)]['display_phone']
        price_list[k] = y[str(k)]['price']
        ratings[k] = y[str(k)]['rating']
    print(phone)
    return render_template('index.html', imgs= resturs_img, resturs_urls=resturs_urls, resturs_names=resturs_names,ret =y, lats=lats, longs= longs, amount = int(amount), term = term, place = place, price = price, phone = phone, price_list = price_list, ratings = ratings, open = open)

@app.route('/sort_price', methods=["GET"])
def results_price():
    term = request.args.get('term')
    loc = request.args.get('place')
    print("term:" + term)
    print("place:" + loc)
    first= request.args.get('one')
    second= request.args.get('two')
    third= request.args.get('three')
    fourth= request.args.get('four')
    open_n = request.args.get('open_now')
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
    if(open_n == "true"):
        open = "true"
    else:
        open = "false"
    print("prices" + prices)
    return redirect(url_for('welcome',term=term,place=loc,price = prices, open = open))
@app.route('/random/<term>/<place>/<price>/<open>')
def random_res(term,place,price,open):
    ret = sample.query_api(term,place,price,open)
    y = json.loads(ret)
    # print(y)
    t = list(y.values())
    amount = t[-1]
    lats = ["" for p in range(int(amount))]
    longs = ["" for p in range(int(amount))]
    resturs_urls = ["" for x in range(int(amount))]
    resturs_names = ["" for x in range(int(amount))]
    resturs_img= ["" for x in range(int(amount))]
    rating_ran= ["" for x in range(int(amount))]
    price_ran = ["" for x in range(int(amount))]
    phone_ran = ["" for x in range(int(amount))]

    # locations = []
    # print(locations)
    for k in range(int(amount)):
        lats[k]= y[str(k)]["coordinates"]["latitude"]
        longs[k] = y[str(k)]["coordinates"]["longitude"]
        resturs_names[k]= y[str(k)]['name']
        resturs_urls[k]= y[str(k)]['url']
        resturs_img[k]= y[str(k)]['image_url']
        rating_ran[k] = y[str(k)]['rating']
        price_ran[k] = y[str(k)]['price']
        phone_ran[k] = y[str(k)]['display_phone']
    rand_num = random.randrange(int(amount))

    latit = lats[rand_num]
    longit = longs[rand_num]
    rand_resturs_name= resturs_names[rand_num]
    rand_resturs_url= resturs_urls[rand_num]
    rand_resturs_img= resturs_img[rand_num]
    rand_rating_ran = rating_ran[rand_num]
    rand_price_ran = price_ran[rand_num]
    rand_phone_ran = phone_ran[rand_num]
    return render_template('random.html',lats = latit, longs = longit, term=term, place=place, price=price,rand_resturs_name=rand_resturs_name,rand_resturs_url=rand_resturs_url,rand_resturs_img=rand_resturs_img, rand_rating_ran= rand_rating_ran, rand_price_ran = rand_price_ran, phone = rand_phone_ran, amount =1, open = open)

@app.route('/res/<term>/<place>')
def search_result(term,place):
    ret = sample.query_api(term, place)
    y = json.loads(ret)
    t = list(y.values())
    amount = t[-1]
    lats =["" for p in range(int(amount))]
    longs =["" for p in range(int(amount))]
    for a in range(int(amount)):
        lats[a] = y[str(a)]["coordinates"]['latitude']
        longs[a] = y[str(a)]["coordinates"]['longitude']
    a = y['2']["coordinates"]['latitude']
    b = y['2']['coordinates']['longitude']

    return render_template('index.html',amount = amount,ret = ret, a= a, b= b, lats= lats,longs=longs)

@app.route('/search', methods=["GET"])
def search():
    term = request.args.get('term')
    loc = request.args.get('place')
    if(loc == ""):
        loc = "new york city"
    if(term == ""):
        term = "indian"
    price = "1,2,3,4"
    open = "false"
    return redirect(url_for('welcome',term=term,place=loc, price=price, open = open))


if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()
