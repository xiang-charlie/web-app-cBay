#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, make_response
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
import subprocess

# instantiate the app
app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
import credentials
config = credentials.get()

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# make one persistent connection to the database
connection = pymongo.MongoClient(config['MONGO_HOST'], 27017, 
                                username=config['MONGO_USER'],
                                password=config['MONGO_PASSWORD'],
                                authSource=config['MONGO_DBNAME'])
db = connection[config['MONGO_DBNAME']] # store a reference to the database

# set up the routes

@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template('index.html')


@app.route('/read')
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    docs = db.market.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('read.html', docs=docs) # render the read template


@app.route('/read/accessories')
def read_accessories():
    docs = db.market.find({"category":"Accessories"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/arts')
def read_arts():
    docs = db.market.find({"category":"Arts"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/automotive')
def read_automotive():
    docs = db.market.find({"category":"Automotive"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/beauty')
def read_beauty():
    docs = db.market.find({"category":"Beauty"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/books')
def read_books():
    docs = db.market.find({"category":"Books"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/clothing')
def read_clothing():
    docs = db.market.find({"category":"Clothing"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/electronics')
def read_electronics():
    docs = db.market.find({"category":"Electronics"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/handmade')
def read_handmade():
    docs = db.market.find({"category":"Handmade"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/kitchen')
def read_kitchen():
    docs = db.market.find({"category":"Kitchen"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/pets')
def read_pets():
    docs = db.market.find({"category":"Pets"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/toys')
def read_toys():
    docs = db.market.find({"category":"Toys"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/videogames')
def read_videogames():
    docs = db.market.find({"category":"Video games"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/cheapest')
def read_cheapest():
    docs = db.market.find({"price":{"$lte":5.00}}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/cheaper')
def read_cheaper():
    docs = db.market.find({"price":{"$lte":20.00}}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read/cheap')
def read_cheap():
    docs = db.market.find({"price":{"$lte":50.00}}).sort("created_at", -1)
    return render_template('read.html', docs=docs)

@app.route('/read/New')
def read_New():
    docs = db.market.find({"condition":"New"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)

@app.route('/read/LikeNew')
def read_LikeNew():
    docs = db.market.find({"condition":"Like new"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)

@app.route('/read/Used')
def read_Used():
    docs = db.market.find({"condition":"Used"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)

@app.route('/read/NeedsFixing')
def read_NeedsFixing():
    docs = db.market.find({"condition":"Needs fixing"}).sort("created_at", -1)
    return render_template('read.html', docs=docs)


@app.route('/read', methods=['POST'])
def read_filterby():

    condition = request.form['fcondition']
    category = request.form['fcategory']
    price = request.form['fprice']
    shipping = request.form['fshipping']

    '''
    condition - done
    condition and category - done
    condition and price - done
    condition and shipping - done
    condition and category and price - done
    condition and category and shipping - done
    condition and price and shipping - done
    condition and category and shipping and price - done
    category - done
    category and price - done
    category and shipping - done
    category and price and shipping - done
    price - done
    price and shipping - done
    shipping - done
    none - done
    '''

    if condition != "":
        if category != "":
            if shipping != "":
                if price != "":
                    if price == "Cheap":
                        # condition, category, shipping, price(low to high)
                        docs = db.market.find({"condition":condition,"category":category,"shipping":shipping}).sort("price",1)
                    else:
                        # condition, category, shipping, price(high to low)
                        docs = db.market.find({"condition":condition,"category":category,"shipping":shipping}).sort("price",-1)
                else:
                    # condition, category, shipping
                    docs = db.market.find({"condition":condition,"category":category,"shipping":shipping}).sort("created_at",-1)
            else:
                if price != "":
                    if price == "Cheap":
                        # condition, category, price(low to high)
                        docs = db.market.find({"condition":condition,"category":category}).sort("price",1)
                    else:
                        # condition, category, price(high to low)
                        docs = db.market.find({"condition":condition,"category":category}).sort("price",-1)
                else:
                    # condition, category
                    docs = db.market.find({"condition":condition,"category":category}).sort("created_at",-1)
        else:
            if shipping != "":
                if price != "":
                    if price == "Cheap":
                        # condition, shipping, price(low to high)
                        docs = db.market.find({"condition":condition,"shipping":shipping}).sort("price",1)
                    else:
                        # condition, shipping, price(high to low)
                        docs = db.market.find({"condition":condition,"shipping":shipping}).sort("price",-1)
                else:
                    # condition, shipping
                    docs = db.market.find({"condition":condition,"shipping":shipping}).sort("created_at",-1)
            else:
                if price != "":
                    if price == "Cheap":
                        # condition, price(low to high)
                        docs = db.market.find({"condition":condition}).sort("price",1)
                    else:
                        #condition, price(high to low)
                        docs = db.market.find({"condition":condition}).sort("price",-1)
                else:
                    # condition
                    docs = db.market.find({"condition":condition}).sort("created_at",-1)
    else:
        if category != "":
            if shipping != "":
                if price != "":
                    if price == "Cheap":
                        # category, shipping, price(low to high)
                        docs = db.market.find({"category":category,"shipping":shipping}).sort("price",1)
                    else:
                        # category, shipping, price(high to low)
                        docs = db.market.find({"category":category,"shipping":shipping}).sort("price",-1)
                else:
                    # category, shipping
                    docs = db.market.find({"category":category,"shipping":shipping}).sort("created_at",-1)
            else:
                if price != "":
                    if price == "Cheap":
                        # category, price(low to high)
                        docs = db.market.find({"category":category}).sort("price",1)
                    else:
                        # category, price(high to low)
                        docs = db.market.find({"category":category}).sort("price",-1)
                else:
                    # category
                    docs = db.market.find({"category":category}).sort("created_at",-1)
        else:
            if shipping != "":
                if price != "":
                    if price == "Cheap":
                        # shipping, price(low to high)
                        docs = db.market.find({"shipping":shipping}).sort("price",1)
                    else:
                        # shipping, price(high to low)
                        docs = db.market.find({"shipping":shipping}).sort("price",-1)
                else:
                    # shipping
                    docs = db.market.find({"shipping":shipping}).sort("created_at",-1)
            else:
                if price != "":
                    if price == "Cheap":
                        # price(low to high)
                        docs = db.market.find({}).sort("price",1)
                    else:
                        # price(high to low)
                        docs = db.market.find({}).sort("price",-1)
                else:
                    # no filters
                    docs = db.market.find({}).sort("created_at",-1)

    return render_template('read.html', docs=docs)


@app.route('/create')
def create():
    """
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    """
    return render_template('create.html') # render the create template


@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name = request.form['fname']
    email = request.form['femail']
    item = request.form['fitem']
    condition = request.form['fcondition']
    category = request.form['fcategory']
    price = float(request.form['fprice'])
    display_price = "{:.2f}".format(float(request.form['fprice']))
    shipping = request.form['fshipping']
    description = request.form['fdescription']
    sold = request.form['fsold']
    password = request.form['fpassword']

    # create a new document with the data the user entered
    doc = {
        "name": name,
        "email": email,
        "item_name": item,
        "condition": condition,
        "category": category,
        "price": price,
        "display_price": display_price, 
        "shipping": shipping,
        "description": description,
        "sold": sold,
        "password": password,
        "created_at": datetime.datetime.utcnow()
    }
    db.market.insert_one(doc) # insert a new document

    # read(title)

    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.market.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/edit/password/<mongoid>')
def edit_p(mongoid):

    doc = db.market.find_one({"_id":ObjectId(mongoid)})
    return render_template('edit-password.html', mongoid=mongoid, doc=doc)


@app.route('/edit/password/<mongoid>', methods=['POST'])
def edit_password(mongoid):
    
    password = request.form['fpassword']

    doc = db.market.find_one({"_id":ObjectId(mongoid)})
    correct_password = doc["password"]

    if password == correct_password:
        return render_template('edit.html', mongoid=mongoid, doc=doc)
    else:
        return render_template('wrong-password.html')


@app.route('/delete/password/<mongoid>')
def delete_p(mongoid):

    doc = db.market.find_one({"_id":ObjectId(mongoid)})
    return render_template('delete-password.html', mongoid=mongoid, doc=doc)


@app.route('/delete/password/<mongoid>', methods=['POST'])
def delete_password(mongoid):
    
    password = request.form['fpassword']

    doc = db.market.find_one({"_id":ObjectId(mongoid)})
    correct_password = doc["password"]

    if password == correct_password:
        db.market.delete_one({"_id": ObjectId(mongoid)})
        return render_template('delete-successful.html', mongoid=mongoid, doc=doc)
    else:
        return render_template('wrong-password.html')


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    name = request.form['fname']
    item = request.form['fitem']
    condition = request.form['fcondition']
    category = request.form['fcategory']
    price = float(request.form['fprice'])
    display_price = "{:.2f}".format(float(request.form['fprice']))
    shipping = request.form['fshipping']
    description = request.form['fdescription']
    sold = request.form['fsold']

    doc = {
        # "_id": ObjectId(mongoid),
        "name": name,
        "item_name": item,
        "condition": condition,
        "category": category,
        "price": price,
        "display_price": display_price, 
        "shipping": shipping,
        "description": description,
        "sold": sold,
        "created_at": datetime.datetime.utcnow()
    }

    db.market.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": doc }
    )

    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/create/comment/<mongoid>')
def comment(mongoid):
    '''
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    '''
    doc = db.market.find_one({"_id": ObjectId(mongoid)})
    return render_template('create_comment.html', mongoid=mongoid, doc=doc) # render the create template



@app.route('/create/comment/<mongoid>', methods=['POST'])
def create_comment(mongoid):
    '''
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    '''
    name = request.form['fname']
    comment = request.form['fcomment']

    doc = db.market.find_one({"_id":ObjectId(mongoid)})
    id = doc["_id"]

    # create a new document with the data the user entered
    doc = {
        "name": name,
        "comment": comment, 
        "item_id": id, 
        "created_at": datetime.datetime.utcnow()
    }
    db.comments.insert_one(doc) # insert a new document

    return redirect(url_for('read_comments', mongoid=mongoid) ) # tell the browser to make a request for the /read route


@app.route('/read/comments/<mongoid>')
def read_comments(mongoid):
    doc = db.market.find_one({"_id":ObjectId(mongoid)})
    id = doc["_id"]

    listing = doc
    docs = db.comments.find({"item_id":id}).sort("created_at", -1)
    return render_template('comments.html', listing=listing, docs=docs)



@app.route('/comment/edit/<mongoid>')
def edit_c(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.comments.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit_comment.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/comment/edit/<mongoid>', methods=['POST'])
def edit_comment(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    name = request.form['fname']
    comment = request.form['fcomment']

    comment_info = db.comments.find_one({"_id": ObjectId(mongoid)})

    item_id = comment_info["item_id"]

    doc = {
        "name": name, 
        "comment": comment,
        "created_at": datetime.datetime.utcnow()
    }

    db.comments.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": doc }
    )

    listing = db.market.find_one({"_id": ObjectId(item_id)})
    docs = db.comments.find({"item_id":item_id}).sort("created_at", -1)

    return render_template('comments.html', listing=listing, docs=docs)


@app.route('/delete/comments/<mongoid>')
def delete_comment(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """

    db.comments.delete_one({"_id":ObjectId(mongoid)})
    return redirect(url_for('read')) # tell the web browser to make a request for the /read route.


@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    db.market.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('read')) # tell the web browser to make a request for the /read route.


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    GitHub can be configured such that each time a push is made to a repository, GitHub will make a request to a particular web URL... this is called a webhook.
    This function is set up such that if the /webhook route is requested, Python will execute a git pull command from the command line to update this app's codebase.
    You will need to configure your own repository to have a webhook that requests this route in GitHub's settings.
    Note that this webhook does do any verification that the request is coming from GitHub... this should be added in a production environment.
    """
    # run a git pull command
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    pull_output = process.communicate()[0]
    # pull_output = str(pull_output).strip() # remove whitespace
    process = subprocess.Popen(["chmod", "a+x", "flask.cgi"], stdout=subprocess.PIPE)
    chmod_output = process.communicate()[0]
    # send a success response
    response = make_response('output: {}'.format(pull_output), 200)
    response.mimetype = "text/plain"
    return response

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)