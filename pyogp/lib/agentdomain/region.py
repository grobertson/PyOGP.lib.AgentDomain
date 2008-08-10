from zope.interface import Interface
from urlparse import urljoin
from indra.base import llsd
import urllib2
import uuid
import random

class Region(object):
    """a region end point on a region domain"""
    
    def __init__(self, url, position=[128,128,128]):
        """initialize the region endpoint"""
        self.url = url
        self.position = position
        self.region_y = None
        self.region_x = None
        self.seed_capability = None
        self.region_id = None
        self.sim_access = None
        self.connect = None
        self.sim_port = None
        self.sim_ip = None
        
    def rez(self, agent):
        """rez an IAgent on that region"""
        
        session_id = str(uuid.uuid1())
        secure_session_id = session_id
	circuit_code = random.randint(0,9999999)
        data = {
          'agent_id' : agent.agent_id,
          'first_name': agent.first_name,
          'last_name': agent.last_name,
          'age_verified' : agent.age_verified, 
          'agent_access' : agent.agent_access,
          'allow_redirect': agent.allow_redirect,
          'god_level':  agent.god_level,
          'identified':  agent.identified,
          'transacted': agent.transacted,
          'limited_to_estate': agent.limited_to_estate,
          'sim_access' : agent.sim_access
        }
        xml = llsd.format_xml(data)

        url=urljoin(self.url,'agent/%s/request' %agent.agent_id)
        headers ={'Content-Type':'application/llsd+xml','Content-Length':len(xml)}
        request = urllib2.Request(url, xml, headers)
        result = urllib2.urlopen(request).read()

        result =  llsd.parse(result)
        # TODO: Error handling! What are the possible error conditions?
        
        # step two: rez_avatar
        url = result['rez_avatar/rez']

	# create the rez_avatar payload:
	data = {
	    'first_name': agent.first_name, 
	    'last_name': agent.last_name,
	    'secure_session_id': session_id, 
	    'age_verified': False, 
	    'region_id': '00000000-0000-0000-0000-000000000000', 
	    'transacted': False, 
	    'agent_access': False, 
	    'circuit_code': circuit_code, 
	    'identified': False, 
	    'session_id': session_id, 
	    'god_level': 0, 
	    'god_override': False, 
	    'inventory_host': 'inv4.mysql.agni.lindenlab.com', 
	    'limited_to_estate': '1', 
	    'position': self.position,
	    'start': 'safe'}

        xml = llsd.format_xml(data)
        headers ={'Content-Type':'application/llsd+xml','Content-Length':len(xml)}
        request = urllib2.Request(url, xml, headers)
        result = urllib2.urlopen(request).read()

        data = llsd.parse(result)
        
        self.region_y = data.get('region_y',None)
        self.region_x = data.get('region_x', None)
        self.seed_capability = data.get('seed_capability', None)
        self.region_id = data.get('region_id', None)
        self.sim_access = data.get('sim_access', None)
        self.connect = data.get('connect', None)
        self.sim_port = data.get('sim_port', None)
        self.sim_ip = data.get('sim_ip', None)
	self.session_id = session_id
	self.secure_session_id = secure_session_id
	self.circuit_code = circuit_code
	self.agent_id = agent.agent_id
        

        
    
    
