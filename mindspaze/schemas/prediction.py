from marshmallow import EXCLUDE, fields

from mindspaze import ma


class InputDataSchema(ma.Schema):
    answers = fields.Raw(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
