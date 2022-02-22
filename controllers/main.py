from odoo.addons.base_rest.controllers import main


class BaseRestWebservicesPublicApiController(main.RestController):
    _root_path = "/base_rest_webservices_api/public/"
    _collection_name = "base.rest.webservices.public.services"
    _default_auth = "public"


class BaseRestWebservicesPrivateApiController(main.RestController):
    _root_path = "/base_rest_webservices_api/private/"
    _collection_name = "base.rest.webservices.private.services"
    _default_auth = "user"


class BaseRestWebservicesNewApiController(main.RestController):
    _root_path = "/base_rest_webservices_api/new_api/"
    _collection_name = "base.rest.webservices.new_api.services"
    _default_auth = "public"

# class BaseRestWebservicesJwtApiController(main.RestController):
#     # JWT Webservices Controller, to be used with auth_jwt_webservices
#     # https://github.com/OCA/server-auth/tree/14.0/auth_jwt_webservices
#     _root_path = "/base_rest_webservices_api/jwt/"
#     _collection_name = "base.rest.webservices.jwt.services"
#     _default_auth = "jwt_webservices_keycloak"
#     _component_context_provider = "auth_jwt_component_context_provider"
#     _default_cors = "*"
