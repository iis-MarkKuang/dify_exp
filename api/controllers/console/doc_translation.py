from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.datastructures import FileStorage
from core.file.file_obj import FileVar

from flask import request
from controllers.console import api


class DocumentTranslationApi(Resource):
    def post(self):
        print(dict(request.form)['data']['file'])
        print(request.form)
        print(request.data)
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileVar, location='form')
        args = parser.parse_args()
        print(args)
        pdf_file = args['file']
        print('got file')
        print(pdf_file)


api.add_resource(DocumentTranslationApi, '/document/translate')
