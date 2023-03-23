from flask_restful import Resource


class Banana(Resource):
    def get(self):
        return {"fruit": "banana"}
