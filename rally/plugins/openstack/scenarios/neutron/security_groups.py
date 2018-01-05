#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from rally import consts
from rally.plugins.openstack import scenario
from rally.plugins.openstack.scenarios.neutron import utils
from rally.task import validation


class NeutronSecurityGroup(utils.NeutronScenario):
    """Benchmark scenarios for Neutron Security Groups."""

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure(context={"cleanup": ["neutron"]})
    def create_and_list_security_groups(self, security_group_create_args=None):
        """Create and list Neutron security-groups.

        Measure the "neutron security-group-create" and "neutron
        security-group-list" command performance.

        :param security_group_create_args: dict, POST /v2.0/security-groups
                                           request options
        """
        security_group_create_args = security_group_create_args or {}
        self._create_security_group(**security_group_create_args)
        self._list_security_groups()

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def create_and_delete_security_groups(self,
                                          security_group_create_args=None):
        """Create and delete Neutron security-groups.

        Measure the "neutron security-group-create" and "neutron
        security-group-delete" command performance.

        :param security_group_create_args: dict, POST /v2.0/security-groups
                                           request options
        """
        security_group_create_args = security_group_create_args or {}
        security_group = self._create_security_group(
            **security_group_create_args)
        self._delete_security_group(security_group)

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure(context={"cleanup": ["neutron"]})
    def create_and_update_security_groups(self,
                                          security_group_create_args=None,
                                          security_group_update_args=None):
        """Create and update Neutron security-groups.

        Measure the "neutron security-group-create" and "neutron
        security-group-update" command performance.

        :param security_group_create_args: dict, POST /v2.0/security-groups
                                           request options
        :param security_group_update_args: dict, POST /v2.0/security-groups
                                           update options
        """
        security_group_create_args = security_group_create_args or {}
        security_group_update_args = security_group_update_args or {}
        security_group = self._create_security_group(
            **security_group_create_args)
        self._update_security_group(security_group,
                                    **security_group_update_args)

    @validation.number("rules_per_security_group", minval=1, integer_only=True)
    @validation.number("port_range_offset", minval=1, integer_only=True)
    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def create_security_group_rules(self,
                                    security_group_rule_create_args=None,
                                    rules_per_security_group=None,
                                    port_range_offset=1):
        """Create Neutron security group rules.
        """
        args = security_group_rule_create_args or {}
        args['direction'] = args.get('direction') or 'ingress'
        args['protocol'] = args.get('protocol') or 'tcp'

        if not args.get('security_group_id'):
            sg_create_args = {}
            security_group = self._create_security_group(**sg_create_args)
            args['security_group_id'] = security_group['security_group']['id']

        for i in range(rules_per_security_group):
            port = port_range_offset + i
            args['port_range_min'] = port
            args['port_range_max'] = port
            self._create_security_group_rule(**args)

        self._list_security_group_rules()

