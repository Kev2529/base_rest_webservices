from odoo import _, tools
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component
from odoo.http import request
from odoo.exceptions import (
    AccessDenied,
    AccessError,
    MissingError,
    UserError,
    ValidationError,
)
import time
import jwt
import base64


class MailService(Component):
    _inherit = "base.rest.service"
    _name = "mail.service"
    _usage = "channel"
    _collection = "base.rest.webservices.mail.services"
    _description = """
        Mail post
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/channel/all"], "GET")],
        output_param=Datamodel("mail.channel.info", is_list=True),
        auth="public",
    )
    def get_all(self):
        """
        Get list of all channels
        """
        channel_list = self.env["mail.channel"].search([])
        res = []
        MailChannelInfo = self.env.datamodels["mail.channel.info"]
        for c in channel_list:
            channel = MailChannelInfo(
                partial=True,
                id=c.id,
                name=c.name,
                channel_type=c.channel_type,
            )
            if c.description:
                channel.description = self._html2text(c.description)
            res.append(channel)
        return res

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=Datamodel("mail.channel.info"),
        auth="public",
    )
    def get(self, _id):
        """
        Get channel's information
        """
        channel_id = self.env["mail.channel"].browse(_id)
        ChannelInfo = self.env.datamodels["mail.channel.info"]
        res = ChannelInfo(
            partial=True,
            id=channel_id.id,
            name=channel_id.name,
            channel_type=channel_id.channel_type
        )
        if channel_id.description:
            res.description = self._html2text(channel_id.description)

        res.channel_message_ids = []
        if channel_id.channel_message_ids:
            MessageInfo = self.env.datamodels["mail.channel.message"]
            for msg in channel_id.channel_message_ids:
                msg_info = MessageInfo(
                    partial=True,
                    id=msg.id,
                    author_name=msg.author_id.name,
                    author_id=msg.author_id.id,
                    create_date=msg.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                )
                # msg_info.channel_ids = self._get_channel_info(
                #     ChannelInfo, msg.channel_ids)
                # msg_info.channel_ids = []
                # for channel in msg.channel_ids:
                #     channel_ids = ChannelInfo(
                #         partial=True,
                #         id=channel.id,
                #         name=channel.name,
                #         channel_type=channel.channel_type,
                #     )
                #     if channel.body:
                #         channel_ids.description = self._html2text(channel.body)
                #     msg_info.channel_ids.append(channel_ids)
                if msg.body:
                    msg_info.description = self._html2text(msg.body)
                res.channel_message_ids.append(msg_info)
        return res

    @restapi.method(
        [(["/channel/new"], "POST")],
        input_param=Datamodel("mail.channel.create"),
        auth="public",
    )
    def create_channel(self, vals):
        """
        Create a new channel
        """
        msg_id = request.env['mail.channel'].channel_create(vals.name)
        __import__('pdb').set_trace()
        return {
            "status_code": 200,
            "channel": msg_id
        }

    @restapi.method(
        [(["/channel/<int:id>"], "DELETE")],
        auth="public"
    )
    def delete_channel(self, _id):
        """
        Delete channel
        """
        channel_id = self.env["mail.channel"].browse(_id)
        channel_id.unlink()
        return 200


    @restapi.method(
        [(["/message/new"], "POST")],
        input_param=Datamodel("mail.channel.message.create", partial=True),
        auth="public",
    )
    def create_message(self, vals):
        """
        Create a message linked to the api'sauthenticated user
        """
        new_msg = {
            "body": vals.body,
            "message_type": 'comment',
            "model": 'mail.channel',
            "moderation_status": 'accepted',
            "subtype_id": 1,
            "res_id": vals.channel_id,
            "record_name": vals.channel_name
        }
        if not vals.channel_id and not vals.channel_name:
            return 422
        msg_id = request.env['mail.message'].create(new_msg)
        msg_id.channel_ids = [(4, vals.channel_id, 0)]
        return {
            "status_code": 200,
            "id": msg_id.id
        }

    @restapi.method(
        [(["/message/update"], "POST")],
        input_param=Datamodel("mail.channel.message.update"),
        auth="public",
    )
    def update_message(self, vals):
        """
        Update message's content
        """
        msg_id = self.env['mail.message'].browse(vals.id)

        msg_id.body = vals.body
        return 200

    @restapi.method(
        [(["/message/<int:id>"], "DELETE")],
        auth="public"
    )
    def delete(self, _id):
        """
        Delete channel's message
        """
        message_id = self.env["mail.message"].browse(_id)
        message_id.unlink()
        return 200

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get_channel_info(self, datamodel, channels):
        res = []
        for c in channels:
            channel = datamodel(
                partial=True,
                id=c.id,
                name=c.name,
                channel_type=c.channel_type,
            )
            if c.body:
                channel.description = self._html2text(c.body)
            res.append(channel)
        return res

    def _html2text(self, html):
        return tools.html2plaintext(html)

    def _prepare_params(self, params):
        for key in ["country", "state"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params
