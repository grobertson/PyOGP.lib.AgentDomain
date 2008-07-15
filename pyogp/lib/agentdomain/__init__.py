from zope.component import getUtility, getMultiAdapter
from zope.interface import implements
from pyogp.lib.base.interfaces import ICredentialDeserializer
from interfaces import ILoginHandler
from pyogp.lib.agentdomain.interfaces import IAgent

class Agent(object):
    implements(IAgent)
    
    def __init__(self,credentials):
        self.credentials
    

def login(context, payload):
    """login an agent"""
    deserializer = getUtility(ICredentialDeserializer)
    credentials = deserializer.deserialize(payload)
    
    # now try to get the user from the host system
    login_handler = getMultiAdapter((credentials,context), ILoginHandler)
    agent = login_handler.login()
    
    # now cast it to IAgent
    agent = IAgent(agent)
    return agent
    
    
    # TOOD: do not assume that it's always plain password
    
    firstname = payload['firstname'].lower()
    lastname = payload['lastname'].lower()
    password = payload['password']
    username = "%s-%s" %(firstname,lastname)
    user = self.context.get(username,None)
    
    