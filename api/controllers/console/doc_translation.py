from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.datastructures import FileStorage
from controllers.console import api


class DocumentTranslationApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        pdf_file = args['file']
        print('got file')
        print(pdf_file)
        print(pdf_file.tell())

    def get(self):
        """
        For connection health check
        """
        return {
            "result": "pong"
        }


api.add_resource(DocumentTranslationApi, '/document/translate')
