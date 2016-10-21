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


class SDNPluginProvider(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:sdn-plugin}-relation-{joined,changed}')
    def joined_or_changed(self):
        ''' Set the connected state from the provides side of the relation. '''
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

        config = self.get_sdn_config()
        # Ensure we have the expected data points from the sdn provider
        # to ensure we have everything expected by the assumptions being
        # made of the .available state
        if config['mtu'] and config['subnet'] and config['cidr']:
            conv.set_state('{relation_name}.available')
        else:
            conv.remove_state('{relation_name}.available')

    @hook('{provides:sdn-plugin}-relation-{departed}')
    def broken_or_departed(self):
        '''Remove connected state from the provides side of the relation. '''
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.available')

    def get_sdn_config(self):
        ''' Return a dict of the SDN configuration. '''
        config = {}
        conv = self.conversation()
        config['mtu'] = conv.get_remote('mtu')
        config['subnet'] = conv.get_remote('subnet')
        config['cidr'] = conv.get_remote('cidr')
        return config
