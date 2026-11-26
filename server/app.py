#!/usr/bin/env python3

import os

from flask import request
from flask_restful import Resource

from config import create_app, db, api
from models import Book, BookSchema


env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

books_schema = BookSchema(many=True)


class Books(Resource):

    def get(self):
        page = request.args.get(
            'page',
            default=1,
            type=int
        )

        per_page = request.args.get(
            'per_page',
            default=5,
            type=int
        )

        pagination = Book.query.order_by(
            Book.id
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        response = {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': books_schema.dump(pagination.items)
        }

        return response, 200


api.add_resource(
    Books,
    '/books',
    endpoint='books'
)


if __name__ == '__main__':
    app.run(port=5555, debug=True)