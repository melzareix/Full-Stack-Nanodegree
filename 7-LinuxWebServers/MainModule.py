from flask import Flask, render_template, request, flash, redirect, url_for, \
    session, make_response, abort, jsonify
from database_models import Category, Item, db, User
from oauth2client import client, crypt
import httplib2
import os
import hashlib
import json
from functools import wraps

app = Flask(__name__)
CLIENT_ID = '260923875640-m7otrchquhoafo8p8m9c447qqfn7s1q4.apps.googleusercontent.com'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalogp:hello@localhost:5432/ItemCatalogue'
db.init_app(app)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# HELPER METHODS
# ---------------------------------------------------------------------------
@app.before_first_request
def create_database():
    """
    Create the database file.
    """
    db.create_all()


@app.before_request
def csrf_protect():
    """
    Checks for CSRF tokens in POST Requests.
    """
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_user_authenticated():
            flash('You must be logged in to access that page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def is_user_authenticated():
    """
    Checks If user credentials exists in session, and that the access token
    is still valid.
    """
    if 'credentials' not in session:
        return False
    credentials = client.OAuth2Credentials.from_json(
        session['credentials'])
    if credentials.access_token_expired:
        return False
    return True


def user_exists(user_id):
    """
    :returns True if the user exists in the Database.
    """
    return User.query.filter_by(id=user_id).first() is not None


def generate_csrf():
    if '_csrf_token' not in session:
        session['_csrf_token'] = hashlib.sha256(os.urandom(1024)).hexdigest()
    return session['_csrf_token']


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# MAIN METHOD AND ROUTES
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    latest_items = Item.query.limit(limit=10).all()
    return render_template('index.html', latest_items=latest_items)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# CATEGORY METHODS AND ROUTES
# ---------------------------------------------------------------------------

@app.route('/cats')
def view_categories():
    categories = Category.query.all()
    return render_template('cats.html', categories=categories, solid='solid')


@app.route('/cats/<int:cat_id>')
def view_category(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    return render_template('category.html', category=category, solid='solid')


@app.route('/cats/new', methods=['GET', 'POST'])
@login_required
def add_cat():
    if request.method == 'GET':
        return render_template('add_cat.html', solid='solid')
    cat_name = request.form.get('cat_name')

    if not cat_name:
        flash('Please Enter A Valid Category name.')
        return redirect(request.url)

    cat = Category(name=cat_name, user_id=session['g_userID'])
    db.session.add(cat)
    db.session.commit()
    flash('Category Added!')
    return redirect(url_for('view_categories'))


@app.route('/cats/<int:cat_id>/del')
@login_required
def del_cat(cat_id):
    cat = Category.query.filter_by(id=cat_id).first()
    if cat.user_id != session['g_userID']:
        flash('You are not authorized to perform this action.')
        return redirect(url_for('view_category', cat_id=cat_id))

    if cat:
        db.session.delete(cat)
        db.session.commit()
        flash('Category Deleted!')
    else:
        flash('You don\'t have enough permission to delete this category!')

    return redirect(url_for('view_categories'))


@app.route('/cats/<int:cat_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_cat(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    if category.user_id != session['g_userID']:
        flash('You are not authorized to perform this action.')
        return redirect(url_for('view_category', cat_id=cat_id))

    if request.method == 'GET':
        return render_template('edit_cat.html', solid='solid',
                               category=category)

    cat_name = request.form.get('cat_name')
    if not cat_name:
        flash('Please Enter A Valid Category name.')
        return redirect(request.url)

    category.name = cat_name
    db.session.add(category)
    db.session.commit()
    flash('Category Updated!')
    return redirect(url_for('view_categories'))


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ITEMS METHODS AND ROUTES
# ---------------------------------------------------------------------------

@app.route('/cats/<int:cat_id>/items/<int:item_id>/')
def view_item(cat_id, item_id):
    item = Item.query.filter_by(id=item_id).first()
    return render_template('item.html', item=item, solid='solid')


@app.route('/items/new', methods=['GET', 'POST'])
@login_required
def add_item():
    categories = Category.query.all()
    if request.method == 'GET':
        return render_template('add_item.html', solid='solid',
                               categories=categories)

    item_title = request.form.get('item_name')
    item_desc = request.form.get('item_desc')
    cat_id = request.form.get('cat_id')

    errors = []
    if not item_title:
        errors.append("Please Enter a Valid Title.")
    if not item_desc:
        errors.append("Please Enter a Valid Description.")
    if not cat_id:
        errors.append("Please Choose a category.")

    if len(errors) == 0:
        new_item = Item(name=item_title, description=item_desc, cat_id=cat_id,
                        user_id=session['g_userID'])
        db.session.add(new_item)
        db.session.commit()
        flash("New Item Added!")
        return redirect(url_for('view_category', cat_id=cat_id))
    else:
        for x in errors:
            flash(x)
        return redirect(request.url)


@app.route('/items/<int:cat_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(cat_id, item_id):
    item = Item.query.filter_by(cat_id=cat_id, id=item_id).first()

    if item.user_id != session['g_userID']:
        flash('You are not authorized to perform this action.')
        return redirect(url_for('view_item', cat_id=cat_id, item_id=item_id))

    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('edit_item.html', categories=categories,
                               item=item, solid='solid')
    item_title = request.form.get('item_name')
    item_desc = request.form.get('item_desc')
    cat_id = request.form.get('cat_id')

    errors = []
    if not item_title:
        errors.append("Please Enter a Valid Title.")
    if not item_desc:
        errors.append("Please Enter a Valid Description.")
    if not cat_id:
        errors.append("Please Choose a category.")

    if len(errors) == 0:
        item.name = item_title
        item.description = item_desc
        item.cat_id = cat_id
        db.session.add(item)
        db.session.commit()
        flash('Item Updated!')
        return redirect(url_for('view_item', item_id=item_id, cat_id=cat_id))
    else:
        for x in errors:
            flash(x)
        return redirect(request.url)


@app.route('/items/<int:cat_id>/<int:item_id>/delete')
@login_required
def del_item(cat_id, item_id):
    item = Item.query.filter_by(cat_id=cat_id, id=item_id).first()

    if item.user_id != session['g_userID']:
        flash('You are not authorized to perform this action.')
        return redirect(url_for('view_item', cat_id=cat_id, item_id=item_id))

    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item Deleted!')
        return redirect(url_for('view_category', cat_id=cat_id))
    else:
        flash('You don\'t have enough permission to delete this item!')
        return redirect(url_for('view_categories'))


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# USER GOOGLE LOGIN METHODS AND ROUTES
# ---------------------------------------------------------------------------

@app.route('/login')
def login():
    if is_user_authenticated():
        flash('You are already logged in.')
        return redirect(url_for('view_categories'))

    return render_template('login.html', solid='solid')


@app.route('/glogin')
def glogin():
    if not is_user_authenticated():
        return redirect(url_for('google_callback'))
    else:
        flash('Successfully logged in!')
        return redirect(url_for('view_categories'))


# noinspection PyUnboundLocalVariable
@app.route('/goauth2callback')
def google_callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='email', redirect_uri=url_for('google_callback', _external=True))

    if 'code' not in request.args:
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        session['state'] = state
        auth_uri = flow.step1_get_authorize_url(state=state)
        return redirect(auth_uri)
    else:
        request_state = request.args.get('state')
        if request_state != session['state']:
            response = make_response(json.dumps('Invalid state parameter.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'
            return response

        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session.permanent = True
        try:
            idinfo = client.verify_id_token(
                credentials.token_response['id_token'], CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                flash('An error occurred trying to connect to google servers,'
                      ' Try again later.')
                return redirect(url_for('login'))
        except crypt.AppIdentityError:
            flash('An error occurred trying to connect to google servers,'
                  ' Try again later.')
            flash(credentials.to_json())
            return redirect(url_for('login'))

        if not user_exists(credentials.id_token['sub']):
            newUser = User(id=credentials.id_token['sub'],
                           email=credentials.id_token['email'])
            db.session.add(newUser)
            db.session.commit()
            flash('You are now registered in our website!')
        else:
            flash('You are now logged in!')

        session['credentials'] = credentials.to_json()
        session['g_userID'] = credentials.id_token['sub']
        session['g_email'] = credentials.id_token['email']
        session['g_accessToken'] = credentials.token_response[
            'access_token']

        return redirect(url_for('view_categories'))


@app.route('/logout')
@login_required
def logout():
    try:
        credentials = client.OAuth2Credentials.from_json(
            session['credentials'])
        credentials.revoke(httplib2.Http())
        del session['credentials']
        del session['g_accessToken']
        del session['g_userID']
        del session['g_email']
        flash('You are now logged out.')
        return redirect(url_for('view_categories'))
    except Exception, e:
        flash('An error occurred with logout.')
        flash(str(e))
        return redirect(url_for('view_categories'))


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# JSON METHODS AND ROUTES
# ---------------------------------------------------------------------------

@app.route('/api/cats')
def view_categories_json():
    categories = Category.query.all()
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/api/cats/<int:cat_id>')
def view_category_json(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    error = {'error': 'Item not found.'}
    if not category:
        return jsonify(error)

    return jsonify(Category=category.serialize)


@app.route('/api/cats/<int:cat_id>/items/<int:item_id>/')
def view_item_json(cat_id, item_id):
    item = Item.query.filter_by(id=item_id).first()
    error = {'error': 'Item not found.'}
    if not item:
        return jsonify(error)
    return jsonify(Item=item.serialize)


app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
app.jinja_env.globals['csrf_token'] = generate_csrf
app.jinja_env.globals['is_authenticated'] = is_user_authenticated
app.jinja_env.auto_reload = True

if __name__ == '__main__':
    app.run(debug=True)
