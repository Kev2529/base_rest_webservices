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


class BlogService(Component):
    _inherit = "base.rest.service"
    _name = "blog.post.service"
    _usage = "blog"
    _collection = "base.rest.webservices.blog.services"
    _description = """
        Blog post
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/channel/<int:id>/get", "/channel//<int:id>"], "GET")],
        output_param=Datamodel("blog.post.info"),
        auth="public",
    )
    def get(self, _id):
        """
        Get post' information
        """
        post_id = self.env["blog.post"].browse(_id)
        PostInfo = self.env.datamodels["blog.post.info"]
        post_info = PostInfo(partial=True)
        post_info.id = post_id.id
        post_info.name = post_id.name
        post_info.subtitle = post_id.subtitle
        post_info.content = post_id.content
        post_info.author_name = post_id.author_name
        return post_info

    @restapi.method(
        [(["/<int:id>"], "POST")],
        input_param=Datamodel("blog.post.update", partial=False),
        auth="public",
    )
    def update(self, _id, message):
        """
        Update post informations
        """
        post = self.env["blog.post"].browse(_id)
        post.name = post.name + ' test '

        return {
            'name': post.name,
            'subtitle': post.subtitle,
            'content': post.content,
        }

    @restapi.method(
        [(["/create"], "POST")],
        input_param=Datamodel("blog.post.update", partial=False),
        auth="public",
    )
    def create(self, vals):
        new_post = {
            'blog_id': 1,
            'name': vals.name,
            'content': vals.name,
            'parent_id': False,
            'tag_ids': [[6, 0, []]]
        }
        post_id = request.env['blog.post'].create(new_post)
        new_post["id"] = post_id.id
        return new_post
