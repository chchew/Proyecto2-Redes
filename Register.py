import sleekxmpp

import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File

class Register(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        #Eventos a utilizar
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.registerNewUser)

        #Plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0096') # File transfer 

    
    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

   
    def registerNewUser(self, iq):
        new_iq = self.Iq()
        new_iq['type'] = 'set'
        new_iq['register']['username'] = self.boundjid.user
        new_iq['register']['password'] = self.password
        
        try:
            new_iq.send(now=True)
            print("Se creó la cuenta: %s" % self.boundjid)
        except IqError as e:
            print("Error: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            self.disconnect()
