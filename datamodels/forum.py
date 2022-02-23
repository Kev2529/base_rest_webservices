from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class ForumPostInfo(Datamodel):
    _name = "forum.post.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=False, allow_none=False)

class ForumPostUpdate(Datamodel):
    _name = "forum.post.update"

    name = fields.String(required=False, allow_none=False)
    subtitle = fields.String(required=False, allow_none=False)
    content = fields.String(required=False, allow_none=False)


class ForumPostCreate(Datamodel):
    _name = "forum.post.create"

    name = fields.String(required=True, allow_none=False)
    content = fields.String(required=True, allow_none=False)
