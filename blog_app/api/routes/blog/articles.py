import logging

from flask import request
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.parser import pagination_parser
from blog_app.api.serializers import page_of_articles, blog_article
from blog_app.api.services import article_service
from blog_app.auth import auth

log = logging.getLogger(__name__)

ns = api.namespace('blog/articles', description='blog articles related operations')


@ns.route('/')
class ArticleCollection(Resource):

    @api.expect(pagination_parser)
    @api.marshal_with(page_of_articles)
    def get(self):
        """
        :return: list of blog articles
        """
        data = pagination_parser.parse_args(request)
        return article_service.paginate(data)

    @api.expect(blog_article)
    @auth.login_required
    def post(self):
        """
        creates a new blog article
        :return: None, status_code=201
        """
        data = request.json
        return article_service.create(data)


@ns.route('/<int:article_id>')
class ArticleItem(Resource):

    @api.marshal_with(blog_article)
    @api.response(404, 'article not found')
    def get(self, article_id):
        """
        :param article_id: the article to get
        :return: the article for the given id
        """
        return article_service.find(article_id)

    @api.expect(blog_article)
    @auth.login_required
    def put(self, article_id):
        """
        update a blog article

        use this operation to change the title, the content,
        or the related category of an article for the given id

        all the fields are mandatory

        * send a JSON object with the fields in the request body

        '''
        {
            "title": "New Awesome Title",
            "content": "Some New Awesome Content",
            "category_id" "42"
        }
        '''
        :param article_id: the article to update
        :return: None, status_code=204
        """
        data = request.json
        return article_service.update(article_id, data)

    @auth.login_required
    def delete(self, article_id):
        """
        deletes the article for the given id
        :param article_id: the article to delete
        :return: None, status_code=204
        """
        return article_service.delete(article_id)
