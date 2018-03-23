# -*- coding: cp1252 -*- #to avoid encoding problem
from flask import Flask, request, render_template,url_for, redirect,session #importing flask to the environment and also required functions
from pyzomato import Pyzomato #importing zomato api
from nutritionix import Nutritionix #importing nutritionx api
import sys,os #importing miscellenous lib

app = Flask(__name__) #initialising flask framework as app
p = Pyzomato('b114ed71e5b2ec1fb505e869c891e157') #initialising zomato api and authenticating through api key
nix = Nutritionix(app_id="d6c8b53e", api_key="3f98f4237dd0e647591d10d4c6c56450") #initialising nutritionx api and authentication


@app.route('/', methods=['POST', 'GET']) #defining url and method of action
def hello_world(): 
    if request.method == 'GET': #fetching python file to user
        return render_template('admin.html') #using admin html as template 
    elif request.method == 'POST':
        username=request.form['username']#getting input from users to login
        password=request.form['password']
        if username=="admin" and password=="admin":#verifing username and password
            return redirect(url_for('home'))#if its correct its redirect to restaurant finding page
        else:
            kwargs = { #keyword arguments
                'error': "Invalid Username or Password", #sending error message to user if its wrong 
                }
            return render_template('admin.html', **kwargs) #displaying html with error message
	    
@app.route('/hotel', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('hotel.html') #displaying hotel finding html to user
    elif request.method == 'POST':
        name=request.form["city"] #getting location name from user
        loc=p.search(q=name) #using zomato api searching restaurants in user entered location
        nam=[] #defining list various parameter
        cus=[]
        price=[]
        rating=[]
        delhi=[]
        reid=[]
        for i in range(0,20): #displaying top 20 restaurants to user
            nam.append(loc['restaurants'][i]['restaurant']['name'].encode('UTF8')) #appending parameters to corresponding list
            cus.append(loc['restaurants'][i]['restaurant']['cuisines'])
            price.append(loc['restaurants'][i]['restaurant']['average_cost_for_two'])
            rating.append(loc['restaurants'][i]['restaurant']['user_rating']['rating_text'])
            delhi.append(loc['restaurants'][i]['restaurant']['is_delivering_now'])
            reid.append(loc['restaurants'][i]['restaurant']['id'])

        kwargs = {
            'name0': nam[0],'name1': nam[1],'name2': nam[2],'name3': nam[3],'name4': nam[4], #sending value for displaying by using keywords
            'cuisines0':cus[0],'cuisines1':cus[1],'cuisines2':cus[2],'cuisines3':cus[3],'cuisines4':cus[4],
            'cost0':price[0],'cost1':price[1],'cost2':price[2],'cost3':price[3],'cost4':price[4],
            'rate0':rating[0],'rate1':rating[1],'rate2':rating[2],'rate3':rating[3],'rate4':rating[4],
            'delivery0':delhi[0],'delivery1':delhi[1],'delivery2':delhi[2],'delivery3':delhi[3],'delivery4':delhi[4],
            'id0':reid[0],'id1':reid[2],'id2':reid[2],'id3':reid[3],'id4':reid[4],
            'name5':nam[5],'name6':nam[6],'name7':nam[7],'name8':nam[8],'name9':nam[9],
            'cuisines5':cus[5],'cuisines6':cus[6],'cuisines7':cus[7],'cuisines8':cus[8],'cuisines9':cus[9],
            'cost5':price[5],'cost6':price[6],'cost7':price[7],'cost8':price[8],'cost9':price[9],
            'rate5':rating[5],'rate6':rating[6],'rate7':rating[7],'rate8':rating[8],'rate9':rating[9],
            'delivery5':delhi[5],'delivery6':delhi[6],'delivery7':delhi[7],'delivery8':delhi[8],'delivery9':delhi[9],
            'id5':reid[5],'id6':reid[6],'id7':reid[7],'id8':reid[8],'id9':reid[9],
            }
        return render_template('hotel1.html',**kwargs)

@app.route('/calory', methods=['POST', 'GET'])
def calory():
    if request.method == 'GET':
        return render_template('calories.html')
    elif request.method == 'POST':
        calo=request.form["cal"] 
        food = nix.search(calo)#using nutritionx api searching for user entered item
        r=food.json()#converting result into json format
        ids=r['hits'][0]['_id']
        c=nix.item(id=ids).json()# nutritions parameter parsing
        kwargs={
            'cals':c['nf_calories'],'calfat':c['nf_calories_from_fat'],'calc':c['nf_calcium_dv'],'chol':c['nf_cholesterol'],'pro':c['nf_protein'],'sod':c['nf_sodium'],'sug':c['nf_sugars'],'corb':c['nf_total_carbohydrate'],'fat':c['nf_total_fat'],'vita':c['nf_vitamin_a_dv'],'vitc':c['nf_vitamin_c_dv'],
    
            }
        return render_template('calories1.html',**kwargs)

	
if __name__ == '__main__':#defining main program
   app.run()#running flask
    
