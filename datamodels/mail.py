from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class MailChannelInfo(Datamodel):
    _name = "mail.channel.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    description = fields.String(required=False, allow_none=True)
    channel_type = fields.String(required=False, allow_none=True)
    channel_message_ids = fields.List(
        NestedModel("mail.channel.message"), required=False, allow_none=True)


class MailChannelCreate(Datamodel):
    _name = "mail.channel.create"

    name = fields.String(required=True, allow_none=False)


class MailChannelMessage(Datamodel):
    _name = "mail.channel.message"

    id = fields.Integer(required=True, allow_none=False)
    author_name = fields.String(required=False, allow_none=False)
    author_id = fields.Integer(required=False, allow_none=False)
    description = fields.String(required=False, allow_none=False)
    create_date = fields.DateTime(required=False, allow_none=False)
    attachment_ids = fields.List(NestedModel(
        "mail.channel.attachment"), required=False)
    # channel_ids = fields.List(
    #     NestedModel("mail.channel.message"), required=False, allow_none=True)


class Attachment(Datamodel):
    _name = "mail.channel.attachment"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    type = fields.String(required=True, allow_none=False)
    file_size = fields.Integer(required=True, allow_none=False)
    mimetype = fields.String(required=True, allow_none=False)


class MailChannelMessageCreate(Datamodel):
    _name = "mail.channel.message.create"

    body = fields.String(required=False, allow_none=False)
    channel_name = fields.String(required=True, allow_none=False)
    channel_id = fields.Integer(required=True, allow_none=False)


class MailChannelMessageUpdate(Datamodel):
    _name = "mail.channel.message.update"

    id = fields.Integer(required=True, allow_none=False)
    body = fields.String(required=True, allow_none=False)
    # channel_name = fields.String(required=True, allow_none=False)
    # channel_id = fields.Integer(required=True, allow_none=False)
