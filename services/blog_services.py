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
    _collection = "base.rest.webservices.public.services"
    _description = """
        Blog post
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/<int:id>"], "GET")],
        output_param=Datamodel("blog.vehicle.info", partial=True),
        auth="public",
    )
    def get_blog_info(self, _id):
        """
        Get vehicle's information
        """
        blog_id = self.env["blog.post"].browse(_id)
        PostInfo = self.env.datamodels["blog.post.info"]
        post_info = PostInfo(partial=True)
        post_info.name = blog_id.name
        post_info.subtitle = blog_id.subtitle
        post_info.content = blog_id.content
        return post_info
