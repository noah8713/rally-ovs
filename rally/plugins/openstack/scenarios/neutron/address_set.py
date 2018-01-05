import netaddr

from rally import consts
from rally import exceptions
from rally.common import utils as common_utils
from rally.plugins.openstack import scenario
from rally.plugins.openstack.scenarios.neutron import utils
from rally.task import validation



class NeutronAddress(utils.NeutronScenario):
    """Benchmark scenarios for Neutron Address Sets."""

    def _do_create_address_set_addr(self,
                            address_set_id,
                            addresses_per_address_set=1,
                            addresses_start_cidr='10.0.0.0/8',
                            addresses_create_bulk=False,
                            addresses_create_batch=1):

        addr_cidr = netaddr.IPNetwork(addresses_start_cidr)
        end_ip = addr_cidr.ip + addresses_per_address_set
        if not end_ip in addr_cidr:
            message = _("Address CIDR %s's size is not big enough for %d addresses.")
            raise exceptions.InvalidConfigException(message  %
                            (addresses_start_cidr, addresses_per_address_set))

        addrs_list = []
        for ip in netaddr.iter_iprange(addr_cidr.ip + 1, end_ip):
            addrs_list.append({'addr': {'address': str(ip)}})

        for addrs in common_utils.chunks(addrs_list, addresses_create_batch):
            if addresses_create_bulk:
                self._create_address_set_addr_bulk(address_set_id, addrs)
            else:
                self._create_address_set_addrs(address_set_id, addrs)

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def create_and_list_address_sets(self,
                                     address_set_create_args=None,
                                     addresses_per_address_set=1,
                                     addresses_start_cidr='10.0.0.0/8',
                                     addresses_create_bulk=False,
                                     addresses_create_batch=1):
        """Create and list Neutron address sets.
        """
        address_set_create_args = address_set_create_args or {}
        addr_set = self._create_address_set(**address_set_create_args)

        addr_set_id = addr_set['address_set']['id']
        self._do_create_address_set_addr(addr_set_id,
                                         addresses_per_address_set,
                                         addresses_start_cidr,
                                         addresses_create_bulk,
                                         addresses_create_batch)

        self._list_address_sets()

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def create_and_delete_address_sets(self,
                                       address_set_create_args=None,
                                       addresses_per_address_set=1,
                                       addresses_start_cidr='10.0.0.0/8',
                                       addresses_create_bulk=False,
                                       addresses_create_batch=1):
        """Create and delete Neutron address-sets.
        """
        address_set_create_args = address_set_create_args or {}
        addr_set = self._create_address_set(**address_set_create_args)

        addr_set_id = addr_set['address_set']['id']
        self._do_create_address_set_addr(addr_set_id,
                                         addresses_per_address_set,
                                         addresses_start_cidr,
                                         addresses_create_bulk,
                                         addresses_create_batch)

        self._delete_address_set(addr_set)

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @scenario.configure()
    def create_and_update_address_sets(self,
                                          address_set_create_args=None,
                                          address_set_update_args=None):
        """Create and update Neutron address-sets.
       """
        address_set_create_args = address_set_create_args or {}
        address_set_update_args = address_set_update_args or {}
        address_set = self._create_address_set(
            **address_set_create_args)
        self._update_address_set(address_set,
                                 **address_set_update_args)

