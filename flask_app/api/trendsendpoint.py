from flask import request
from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger
from .errors import JsonRequiredError
from .errors import JsonInvalidError
from .models import TrendsResult

class TrendsEndpoint(Resource):
    @swagger.operation(
        responseClass=TrendsResult.__name__,
        nickname='sentiment',
        responseMessages=[
            {"code": 400, "message": "Input required"},
            {"code": 500, "message": "JSON format not valid"},
        ],
        parameters=[
            {
                "name": "hashtag",
                "description": "JSON-encoded name",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
        ])
    @marshal_with(TrendsResult.resource_fields)
    def post(self):
        """Return a sentiment object

            User sends in a hashtag as a parameter and the response is the sentiment"""
        reqs = request.get_json()
        if not reqs:
            raise JsonRequiredError()
        try:
            reqs['woeid']
            return TrendsResult(woeid=reqs['woeid'])
        except KeyError:
            raise JsonInvalidError()