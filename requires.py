#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class SDNPluginClient(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:sdn-plugin}-relation-{joined,changed}')
    def changed(self):
        ''' Indicate the relation is connected, and if the relation data is
        set it is also available. '''
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{requires:sdn-plugin}-relation-{departed}')
    def broken(self):
        ''' Indicate the relation is no longer available and not connected. '''
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def set_configuration(self, mtu, subnet, cidr):
        ''' Set the configuration keys on the wire '''
        conv = self.conversation()
        conv.set_remote(data={'mtu': mtu, 'subnet': subnet, 'cidr': cidr})
