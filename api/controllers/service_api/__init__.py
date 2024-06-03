from flask import Blueprint

from libs.external_api import ExternalApi
from prometheus_flask_exporter import RESTfulPrometheusMetrics
from api.app import app

bp = Blueprint('service_api', __name__, url_prefix='/v1')
api = ExternalApi(bp)
metrics = RESTfulPrometheusMetrics(app, api)


from . import index
from .app import app, audio, completion, conversation, file, message, workflow
from .dataset import dataset, document, segment
