import sys
from flask_restful import Resource, fields, marshal_with, reqparse
from core.file.file_obj import FileVar

from controllers.console import api


class DocumentTranslationApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileVar, location='form')
        args = parser.parse_args()
        pdf_file = args['file']
        print('Got file')
        print(pdf_file)

api.add_resource(DocumentTranslationApi, '/document/translate')
