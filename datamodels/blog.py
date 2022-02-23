from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class BlogPostInfo(Datamodel):
    _name = "blog.post.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    subtitle = fields.String(required=True, allow_none=False)
    content = fields.String(required=True, allow_none=False)
    author_name = fields.String(required=False, allow_none=True)


class BlogPostUpdate(Datamodel):
    _name = "blog.post.update"

    name = fields.String(required=False, allow_none=False)
    subtitle = fields.String(required=False, allow_none=False)
    content = fields.String(required=False, allow_none=False)
