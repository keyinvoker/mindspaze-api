from marshmallow import (
    EXCLUDE,
    fields,
    Schema,
    validate,
    validates_schema,
)


class InputDataSchema(Schema):
    article_text = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
