from flask import Flask, redirect, render_template, request, url_for
import requests 
from dotenv import load_dotenv
load_dotenv() 
import os
apikey= os.getenv("APIKEY")
import mysql.connector
con=mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)
cursor=con.cursor()
url="https://api.api-ninjas.com/v1/quotes"
headers={'X-Api-Key': apikey}
def get_quote():
    response=requests.get(url,headers=headers)
    data=response.json()
    if isinstance(data,list) and len(data)>0:
        quote_value = data[0]['quote']
        author_value = data[0]['author']
        category_value = data[0]['category']
        return quote_value, author_value, category_value
    else:
        return "No quote found"
        
app=Flask(__name__)
@app.route('/h')
def home():
    quote,author,category=get_quote()
    return render_template('ai_quote.html',
                           quote1 =quote,
                           author1=author,
                           category1=category)

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return "This is the about page."
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM registration WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('home'))  # goes to ai_quote.html
        else:
            return "❌ Invalid username or password"
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor.execute("INSERT into registration  (username, password, email) VALUES (%s, %s, %s)", [user, password, email])
        con.commit()
        return "values stored successfully"
    return render_template('registration.html')

@app.route('/index')
def index():
    return render_template('index.html')
app.run(use_reloader=True)