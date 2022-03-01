from odoo import _
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


class ForumService(Component):
    _inherit = "base.rest.service"
    _name = "forum.post.service"
    _usage = "forum"
    _collection = "base.rest.webservices.forum.services"
    _description = """
        Forum post
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=Datamodel("forum.post.info", partial=True),
        auth="public",
    )
    def get(self, _id):
        """
        Get post's information
        """
        post_id = self.env["forum.post"].browse(_id)
        replies = []
        for reply in post_id.child_ids:
            replies.append({
                "name": reply.name,
                "date": reply.create_date,
                "content": reply.content,
                "comment": self._get_comment(reply.website_message_ids)
            })
        res = {
            "name": post_id.name,
            "date": post_id.create_date,
            "content": post_id.content,
            "replies": replies
        }
        return res

    @restapi.method(
        [(["/<int:id>"], "POST")],
        input_param=Datamodel("forum.post.update", partial=False),
        auth="public",
    )
    def update(self, _id, message):
        """
        Update post informations
        """
        post = self.env["forum.post"].browse(_id)

        if message.name:
            post.name += message.name
        if message.subtitle:
            post.subtitle += message.subtitle
        if message.content:
            post.content += message.content

        return 200

    @restapi.method(
        [(["/create"], "POST")],
        input_param=Datamodel("forum.post.update", partial=False),
        auth="public",
    )
    def create(self, vals):
        new_post = {
            'forum_id': 1,
            'name': vals.name,
            'content': vals.name,
            'parent_id': False,
            'tag_ids': [[6, 0, []]]
        }
        forum_id = request.env['forum.post'].create(new_post)
        new_post["id"] = forum_id.id
        return new_post

    @restapi.method(
        [(["/<int:id>"], "DELETE")],
        auth="public"
    )
    def delete(self, _id):
        post_id = self.env["forum.post"].browse(_id)
        post_id.unlink()
        return 200


    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get_comment(self, comments):
        res = []
        for comment in comments:
            res.append({
                "date": comment.create_date,
                "html_comment": comment.body,
                "text_comment": comment.description,
                "author": comment.author_id.name
            })
        return res
