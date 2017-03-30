# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ecl.identity import identity_service
from ecl import resource


class User(resource.Resource):
    resource_key = 'user'
    resources_key = 'users'
    base_path = '/users'
    service = identity_service.IdentityService()

    # capabilities
    allow_create = True
    allow_retrieve = True
    allow_update = True
    allow_delete = True
    allow_list = True
    patch_update = True

    # Properties
    #: References the user's default project ID against which to authorize,
    #: if the API user does not explicitly specify one when creating a token.
    #: Setting this attribute does not grant any actual authorization on the
    #: project, and is merely provided for the user's convenience.
    #: Therefore, the referenced project does not need to exist within the
    #: user's domain.
    #:
    #: *New in version 3.1* If the user does not have authorization to
    #: their default project, the default project will be ignored at token
    #: creation. *Type: string*
    default_project_id = resource.prop('default_project_id')
    #: The description of this user. *Type: string*
    description = resource.prop('description')
    #: References the domain ID which owns the user; if a domain ID is not
    #: specified by the client, the Identity service implementation will
    #: default it to the domain ID to which the client's token is scoped.
    #: *Type: string*
    domain_id = resource.prop('domain_id')
    #: The email of this user. *Type: string*
    email = resource.prop('email')
    #: Setting this value to ``False`` prevents the user from authenticating or
    #: receiving authorization. Additionally, all pre-existing tokens held by
    #: the user are immediately invalidated. Re-enabling a user does not
    #: re-enable pre-existing tokens. *Type: bool*
    is_enabled = resource.prop('enabled', type=bool)
    #: Unique user name, within the owning domain. *Type: string*
    name = resource.prop('name')
    #: The default form of credential used during authentication.
    #: *Type: string*
    password = resource.prop('password')
