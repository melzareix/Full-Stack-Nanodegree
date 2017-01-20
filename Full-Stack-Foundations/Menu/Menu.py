from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from database_models import Category, Item, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itemsCatalog.db'
db.init_app(app)


@app.route('/')
def index():
    latest_items = Item.query.limit(limit=10).all()
    return render_template('index.html', latest_items=latest_items)


@app.route('/cats')
def view_categories():
    categories = Category.query.all()
    return render_template('cats.html', categories=categories, solid='solid')


@app.route('/cats/<int:cat_id>')
def view_category(cat_id):
    category = Category.query.filter_by(id=cat_id).one()
    return render_template('category.html', category=category, solid='solid')


@app.route('/cats/<int:cat_id>/items/<int:item_id>/')
def view_item(cat_id, item_id):
    item = Item.query.filter_by(id=item_id).one()
    return render_template('item.html', item=item, solid='solid')


@app.route('/items/new', methods=['GET', 'POST'])
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
        new_item = Item(name=item_title, description=item_desc, cat_id=cat_id)
        db.session.add(new_item)
        db.session.commit()
        flash("New Item Added!")
        return redirect(url_for('view_category', cat_id=cat_id))
    else:
        for x in errors:
            flash(x)
        return redirect(request.url)


@app.route('/items/<int:cat_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(cat_id, item_id):
    item = Item.query.filter_by(cat_id=cat_id, id=item_id).one()

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


@app.route('/cats/new', methods=['GET', 'POST'])
def add_cat():
    if request.method == 'GET':
        return render_template('add_cat.html', solid='solid')
    cat_name = request.form.get('cat_name')

    if not cat_name:
        flash('Please Enter A Valid Category name.')
        return redirect(request.url)

    cat = Category(name=cat_name)
    db.session.add(cat)
    db.session.commit()
    flash('Category Added!')
    return redirect(url_for('view_categories'))


@app.route('/cats/<int:cat_id>/edit', methods=['GET', 'POST'])
def edit_cat(cat_id):
    category = Category.query.filter_by(id=cat_id).one()
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


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True)
