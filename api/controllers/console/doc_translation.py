import sys

from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from controllers.console import api


class DocumentTranslationApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("file", type=FileStorage, location="files")
        args = parser.parse_args()
        pdf_file = args["file"]
        print("Got file")
        print(sys.getsizeof(pdf_file))
        pdf_file.save("/home/ykuang/a.pdf")


api.add_resource(DocumentTranslationApi, "/document/translate")
