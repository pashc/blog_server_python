from blog_app.database import db
from blog_app.database.models.blog.category import Category


def find(category_id):
    return Category.query.filter(Category.id == category_id).one()


def find_all():
    return Category.query.all()


def create(data):
    name = data.get('name')
    category_id = data.get('id')
    category = Category(name)
    if category_id:
        category.id = category_id

    db.session.add(category)
    db.session.commit()
    return None, 201


def update(category_id, data):
    category = find(category_id)
    category.name = data.get['name']
    db.sesson.add(category)
    db.session.commit()
    return None, 204


def delete(category_id):
    category = find(category_id)
    db.session.delete(category)
    db.session.commit()
    return None, 204
