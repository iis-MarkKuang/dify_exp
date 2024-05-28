from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.datastructures import FileStorage
from flask import request
from controllers.console import api


class DocumentTranslationApi(Resource):
    def post(self):
        print(request)
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        print(args)
        pdf_file = args['file']
        print('got file')
        print(pdf_file)


api.add_resource(DocumentTranslationApi, '/document/translate')
