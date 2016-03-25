from flask import Flask, render_template, jsonify, url_for, request, redirect
app = Flask(__name__)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Item, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def main_page():
    categories = session.query(Catalog).all()
    catagory_amount = []
    for c in categories:
        items_in_catagory = session.query(Item).filter_by(catalog_id = c.id).all()
        catagory_amount.append(len(items_in_catagory))

    items = session.query(Item).order_by(desc(Item.created_date)).all()

    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state

    directory = []
    directory_main = {}
    directory_main['link'] = url_for('main_page')
    directory_main['name'] = 'Catalog App'
    directory.append(directory_main)

    user = getUserInfo(login_session['user_id'])
    login = False
    if 'username' in login_session:
        login = True

    return render_template('index.html', categories = categories, catagory_amount=catagory_amount,
            items = items, login = login, directory=directory, state = state, user=user)

@app.route('/catalog/JSON')
def all_items_json():
    items = session.query(Item).all()
    return jsonify(Item=[i.serialize for i in items])

@app.route('/catalog/<int:catalog_id>/<int:item_id>')
def single_catagory(catalog_id, item_id):
    categories = session.query(Catalog).all()

    catagory_amount = []
    for c in categories:
        items_in_catagory = session.query(Item).filter_by(catalog_id = c.id).all()
        catagory_amount.append(len(items_in_catagory))

    item = session.query(Item).filter_by(id = item_id).one()
    creator = getUserInfo(item.user_id)

    user = getUserInfo(login_session['user_id'])
    login = True
    if 'username' not in login_session:
        login = False

    directory = []
    directory_main = {}
    directory_main['link'] = url_for('main_page')
    directory_main['name'] = 'Catalog App'
    directory.append(directory_main)

    directory_catalog = {}
    directory_catalog['link'] = url_for('items_by_catalog', catalog_id=catalog_id)
    directory_catalog['name'] = item.catalog.name
    directory.append(directory_catalog)

    directory_item = {}
    directory_item['link'] = url_for('single_catagory', catalog_id=catalog_id, item_id=item_id)
    directory_item['name'] = item.title
    directory.append(directory_item)

    if 'username' not in login_session or creator is None or creator.id != login_session['user_id']:
        return render_template('public_item_details.html', item = item, categories = categories,
            catagory_amount=catagory_amount, directory=directory, login=login, user=user)
    else:
        return render_template('item_details.html', item = item, categories = categories,
            catagory_amount=catagory_amount, directory=directory, login=login, user=user)

@app.route('/catalog/<int:catalog_id>')
def items_by_catalog(catalog_id):
    categories = session.query(Catalog).all()

    catagory = session.query(Catalog).filter_by(id = catalog_id).one()
    items = session.query(Item).filter_by(catalog_id = catalog_id).all()

    catagory_amount = []
    for c in categories:
        items_in_catagory = session.query(Item).filter_by(catalog_id = c.id).all()
        catagory_amount.append(len(items_in_catagory))

    user = getUserInfo(login_session['user_id'])
    login = True
    if 'username' not in login_session:
        login = False

    directory = []
    directory_main = {}
    directory_main['link'] = url_for('main_page')
    directory_main['name'] = 'Catalog App'
    directory.append(directory_main)

    directory_catalog = {}
    directory_catalog['link'] = url_for('items_by_catalog', catalog_id=catalog_id)
    directory_catalog['name'] = catagory.name
    directory.append(directory_catalog)

    return render_template('items_by_catalog.html',
        items = items, catagory = catagory, categories = categories,
        catagory_amount=catagory_amount, directory=directory, login=login, user=user)


@app.route('/catalog/add_item', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newItem = Item(title = request.form['title'],
            description = request.form['description'],
            price = request.form['price'],
            catalog_id = request.form['catalog_id'],
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('main_page'))
    else:
        categories = session.query(Catalog).all()
        return render_template('newItem.html', categories = categories)

@app.route('/api/newItem', methods=['POST'])
def newItem_API():
    if 'username' not in login_session:
        return redirect('/login')

    newItem = Item(title = request.json['title'],
        description = request.json['description'],
        price = request.json['price'],
        picture = request.json['picture'],
        catalog_id = request.json['catalog_id'],
        user_id=login_session['user_id'])
    session.add(newItem)
    session.commit()
    return redirect(url_for('main_page'))

@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')

    item_to_edit = session.query(Item).filter_by(id = item_id).one()

    if item_to_edit.user_id != login_session['user_id']:
        return "You are not authorized to edit this item!!"

    if request.method == 'POST':
        if request.form['title']:
            item_to_edit.title = request.form['title']
        if request.form['description']:
            item_to_edit.description = request.form['description']
        if request.form['price']:
            item_to_edit.price = request.form['price']
        if request.form['catalog_id']:
            item_to_edit.catalog_id = request.form['catalog_id']

        session.add(item_to_edit)
        session.commit()
        return redirect(url_for('main_page'))
    else:
        categories = session.query(Catalog).all()

        catagory_amount = []
        for c in categories:
            items_in_catagory = session.query(Item).filter_by(catalog_id = c.id).all()
            catagory_amount.append(len(items_in_catagory))

        user = getUserInfo(login_session['user_id'])
        login = True
        if 'username' not in login_session:
            login = False

        directory = []
        directory_main = {}
        directory_main['link'] = url_for('main_page')
        directory_main['name'] = 'Catalog App'
        directory.append(directory_main)

        directory_catalog = {}
        directory_catalog['link'] = url_for('items_by_catalog', catalog_id=item_to_edit.catalog.id)
        directory_catalog['name'] = item_to_edit.catalog.name
        directory.append(directory_catalog)

        directory_item = {}
        directory_item['link'] = url_for('single_catagory', catalog_id=item_to_edit.catalog.id, item_id=item_to_edit.id)
        directory_item['name'] = item_to_edit.title
        directory.append(directory_item)

        return render_template('editItem.html', item = item_to_edit, categories = categories, directory=directory,
                catagory_amount=catagory_amount, login=login, user=user)

@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')

    item_to_delete = session.query(Item).filter_by(id = item_id).one()
    if item_to_delete.user_id != login_session['user_id']:
        return "You are not authorized to delete this item!!"

    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect(url_for('main_page'))
    else:
        return render_template('deleteItem.html', item = item_to_delete)

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state = state)
    # return "The current session state is %s" %login_session['state']

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print login_session

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]


    if result['status'] == '200':
        del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	return redirect(url_for('main_page'))
    else:
        login_session.clear()
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).first()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
