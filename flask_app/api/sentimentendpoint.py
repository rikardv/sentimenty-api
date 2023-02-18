from flask import request
from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger
from .models import SentimentResult
from .errors import JsonRequiredError
from .errors import JsonInvalidError

class SentimentEndpoint(Resource):
    @swagger.operation(
        responseClass=SentimentResult.__name__,
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
    @marshal_with(SentimentResult.resource_fields)
    def post(self):
        """Return a sentiment object

            User sends in a hashtag as a parameter and the response is the sentiment"""
        reqs = request.get_json()
        if not reqs:
            raise JsonRequiredError()
        try:
            reqs['tag']
            return SentimentResult(tag=reqs['tag'])
        except KeyError:
            raise JsonInvalidError()


