from zope.interface import Interface, Attribute

class ILoginContext(Interface):
    """defines the context on which the login is supposed to work
    
    This is mainly a marker interface for anything you want to pass in 
    to a login handler. It could be some object in the case of Zope or some
    database handler for other frameworks.
    
    """
    
class ISeedCapability(Interface):
    """a seed capability to be sent to the client"""
    
    payload = Attribute("""the payload we need to send encoded in whatever format you want to""")
    content_type = Attribute("""the content type of the serialization used""")
    
    # TODO: move this into a serializer component
    
class IAgent(Interface):
    """models an agent for the agent domain implementation
    
    TODO: check if that's reusable from lib.base.
    """
    
    seedcap = Attribute("""the seed capability""")

class ILoginHandler(Interface):
    """a login handler handles the login to an agent domain
    
    You need to implement an adapter implementing this interface in your
    own agent domain implementation. It is supposed to be a multi adapter
    which takes an ICredential and an IContext.
    """
    
    def login():
        """try to login an agent
        
        This method cqn take the passed credentials and the context to
        login the user. If that works, an agent object should be returned
        which implements IAgent. If an agent wasn't found, you can raise
        AgentNotFound, if it couldn't be logged in, raise AgentUnauthorized.
        """
        
        