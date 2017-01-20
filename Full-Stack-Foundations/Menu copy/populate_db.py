from Menu import db, Category, Item


def populate_data():
    session = db.session

    categories = [
        'Football Players',
        'Programming Languages',
        'Companies',
        'Social Networks'
    ]

    items = [
        {'name': 'Messi',
         'description': 'The best football player in the world.',
         'cat_id': 1},
        {'name': 'Ronaldo',
         'description': 'The second best player in the world.',
         'cat_id': 1},
        {'name': 'Suarez', 'description': 'The Best Forward in the world.',
         'cat_id': 1},
        {'name': 'Sergio Emad', 'description': 'Born in the 90th minute.',
         'cat_id': 1},
        {'name': 'Python', 'description': 'Easy and fun to use.',
         'cat_id': 2},
        {'name': 'C/C++',
         'description': 'Low-level to the extent of pointers.',
         'cat_id': 2},
        {'name': 'Java', 'description': 'Should be renamed to verbose.',
         'cat_id': 2},
        {'name': 'Google', 'description': 'Dont be evil :).', 'cat_id': 3},
        {'name': 'Udacity', 'description': 'Saving my ass.', 'cat_id': 3},
        {'name': 'Apple', 'description': 'RIP Steve Jobs.', 'cat_id': 3},
        {'name': 'Facebook', 'description': 'The famous .Copycat',
         'cat_id': 4},
        {'name': 'Snapchat', 'description': 'Because People are stupid.',
         'cat_id': 4},
        {'name': 'Twitter', 'description': 'RIP My friend', 'cat_id': 4}]

    for cat in categories:
        session.add(Category(name=cat))
    session.commit()

    for item in items:
        name, desc, cat_id = item.name, item.description, item.cat_id
        session.add(Item(name=name, description=desc, cat_id=cat_id))
    session.commit()

    print "Hurray! I added some data."
