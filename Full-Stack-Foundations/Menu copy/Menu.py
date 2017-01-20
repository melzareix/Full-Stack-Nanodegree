from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database_models import Category, Item, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itemsCatalog.db'
db.init_app(app)


# @app.before_first_request
# def create_database():
#     db.create_all()
#
#
# @app.before_first_request
# def populate_data():
#     session = db.session
#
#     categories = [
#         'Football Players',
#         'Programming Languages',
#         'Companies',
#         'Social Networks'
#     ]
#
#     for cat in categories:
#         session.add(Category(name=cat))
#     session.commit()
#
#     items = [
#         {'name': 'Messi',
#          'description': 'The best football player in the world.',
#          'cat_id': 1},
#         {'name': 'Ronaldo',
#          'description': 'The second best player in the world.',
#          'cat_id': 1},
#         {'name': 'Suarez', 'description': 'The Best Forward in the world.',
#          'cat_id': 1},
#         {'name': 'Sergio Emad', 'description': 'Born in the 90th minute.',
#          'cat_id': 1},
#         {'name': 'Python', 'description': 'Easy and fun to use.',
#          'cat_id': 2},
#         {'name': 'C/C++',
#          'description': 'Low-level to the extent of pointers.',
#          'cat_id': 2},
#         {'name': 'Java', 'description': 'Should be renamed to verbose.',
#          'cat_id': 2},
#         {'name': 'Google', 'description': 'Dont be evil :).', 'cat_id': 3},
#         {'name': 'Udacity', 'description': 'Saving my ass.', 'cat_id': 3},
#         {'name': 'Apple', 'description': 'RIP Steve Jobs.', 'cat_id': 3},
#         {'name': 'Facebook', 'description': 'The famous .Copycat',
#          'cat_id': 4},
#         {'name': 'Snapchat', 'description': 'Because People are stupid.',
#          'cat_id': 4},
#         {'name': 'Twitter', 'description': 'RIP My friend', 'cat_id': 4}]
#
#     for item in items:
#         name, desc, cat_id = item['name'], item['description'], item['cat_id']
#         session.add(Item(name=name, description=desc, cat_id=cat_id))
#     session.commit()
#
#     print "Hurray! I added some data."


@app.route('/')
def index():
    items_num = db.session.query(db.func.count(Item.name)).scalar()
    cats_num = db.session.query(db.func.count(Category.name)).scalar()

    return render_template('index.html', items_num=items_num,
                           cats_num=cats_num)


@app.route('/categories')
def view_categories():
    categories = Category.query.all()
    return render_template('cats.html', categories=categories)


@app.route('/categories/<int:cat_id>')
def view_category(cat_id):
    category = Category.query.filter_by(id=cat_id).one()
    return render_template('category.html', category=category)


@app.route('/categories/<int:cat_id>/<int:item_id>/')
def view_item(cat_id, item_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
