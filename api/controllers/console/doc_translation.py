import sys
from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.datastructures import FileStorage
from controllers.console import api


class DocumentTranslationApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        pdf_file = args['file']
        print('Got file')
        print(sys.getsizeof(pdf_file))

api.add_resource(DocumentTranslationApi, '/document/translate')
