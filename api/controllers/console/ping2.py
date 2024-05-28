from flask_restful import Resource

from controllers.console import api


class Ping2Api(Resource):

    def get(self):
        """
        For connection health check
        """
        return {
            "result": "pong"
        }


api.add_resource(Ping2Api, '/ping2')
