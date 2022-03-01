from odoo.addons.base_rest.controllers import main


class BaseRestWebservicesBlogController(main.RestController):
    _root_path = "/base_rest_webservices_api/blog/"
    _collection_name = "base.rest.webservices.blog.services"
    _default_auth = "public"


class BaseRestWebservicesForumController(main.RestController):
    _root_path = "/base_rest_webservices_api/forum/"
    _collection_name = "base.rest.webservices.forum.services"
    _default_auth = "public"


class BaseRestWebservicesMailController(main.RestController):
    _root_path = "/base_rest_webservices_api/mail/"
    _collection_name = "base.rest.webservices.mail.services"
    _default_auth = "public"

# class BaseRestWebservicesJwtApiController(main.RestController):
#     # JWT Webservices Controller, to be used with auth_jwt_webservices
#     # https://github.com/OCA/server-auth/tree/14.0/auth_jwt_webservices
#     _root_path = "/base_rest_webservices_api/jwt/"
#     _collection_name = "base.rest.webservices.jwt.services"
#     _default_auth = "jwt_webservices_keycloak"
#     _component_context_provider = "auth_jwt_component_context_provider"
#     _default_cors = "*"
