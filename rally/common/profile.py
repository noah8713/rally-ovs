#
# Created on Jan 27, 2016
#
# @author: lhuang8
#

import functools
from oslo_config import cfg

from rally.common import fileutils
from rally.cli import envutils
from rally.exceptions import InvalidArgumentsException

PROFILE_OPENSTACK = "openstack"
PROFILE_OVS = "ovs"
PROFILE_ALL = "all"

PROFILE_ALL_LIST = [PROFILE_OPENSTACK,PROFILE_OVS]


PROFILE_OPTS = [cfg.StrOpt("profile", default=None,
                       help="Set profile for Rally, default is openstack."
                            "Must be one of [openstack|ovs]")]

CONF = cfg.CONF
CONF.register_cli_opts(PROFILE_OPTS)



NAMESPACE_DEFAULT = "default"
NAMESPACE_OPENSTACK = "openstack"
NAMESPACE_OVS = "ovs"

profile = PROFILE_OPENSTACK
namespace = NAMESPACE_OVS

def setup(): 
    if CONF.profile:
        profile = CONF.profile
    else:
        profile = envutils.get_global("RALLY_PROFILE")
        if profile == None:
            profile = PROFILE_OPENSTACK
            
    if not profile in PROFILE_ALL_LIST:
        raise InvalidArgumentsException("Unknown profile %s" % profile)
    
    fileutils.update_globals_file("RALLY_PROFILE", profile)
    
    print("Using profile: %s" % profile)    



def is_openstack():
    return profile == PROFILE_OPENSTACK


def use_openstack():
    return profile == PROFILE_OPENSTACK


def configure(include=[PROFILE_ALL], exclude=None):
    
    def decorator(func):
        profile = {"include" : include, "exclude" : exclude}
        func.meta = {"profile" : profile}
        
        return func
    
    return decorator

    
def is_disabled(include, exclude):
    include = include or []
    exclude = exclude or []
    
    if PROFILE_ALL in exclude or profile in exclude:
        return True
    
    if PROFILE_ALL in include or profile in include:
        return False
    
    return True


