from zope.component import getUtility, getMultiAdapter
from zope.interface import implements
from pyogp.lib.base.interfaces import ICredentialDeserialization
from interfaces import ILoginHandler
from pyogp.lib.agentdomain.interfaces import IAgent

from indra.base import llsd
import uuid
import urllib2
from region import Region


def rez(agent, region_url, position=[128,128,128]):
    """rez an agent on a region
    
    this will call request and rez_avatar/rez caps
    
    """
    
    region = Region(region_url, position)
    region.rez(agent)
    return region


class Agent(object):
    implements(IAgent)
    
    def __init__(self,credentials):
        self.credentials
    

def login(context, payload):
    """login an agent"""
    # TODO: check header for content type
    deserializer = getUtility(ICredentialDeserialization, name="application/llsd+xml")
    credentials = deserializer.deserialize(payload)
    
    # now try to get the user from the host system
    login_handler = getMultiAdapter((credentials,context), ILoginHandler)
    agent = login_handler.login()
    
    # now cast it to IAgent
    agent = IAgent(agent)
    return agent
    
