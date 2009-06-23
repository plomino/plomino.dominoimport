# -*- coding: utf-8 -*-
#
# File: manager.py
#
# GNU General Public License (GPL)
#

"""
Created on 20 may 2009

@author: Emmanuelle Helly

File DxlConfig.py is required
"""

__author__ = """Emmanuelle Helly"""
__docformat__ = 'plaintext'

from binascii import a2b_base64
import mimetypes

class PlominoBuilder(object):
    """
    create all elements in the correct database from a dict 
    (not implemented yet)
    """ 

    def __init__(self, plominoDatabase):
        self.plominoDatabase = plominoDatabase
    
    
    def createForm(self, formInfos):
        """
        Create form in the database

        @param dict formInfos : 
        @return string :
        @author
        """
        pass

    def createView(self, viewInfos):
        """
         

        @param dict viewInfos : 
        @return string :
        @author
        """
        pass

    def createDoc(self, docInfos):
        """
         

        @param dict docInfos : 
        @return string :
        @author
        """
        pass

    def createAgent(self, agentInfos):
        """
         

        @param dict agentInfos : 
        @return string :
        @author
        """
        pass

    def createResource(self, resourceInfos):
        """
        Add files into the database "resources" folder
        @param dict resourceInfos : 
        @return string :
        """
        print 'creating resource in database: ', resourceInfos['name'] 
        #if not(hasattr(self.plominoDatabase.resources, resourceInfos['name'])):
        self.plominoDatabase.manage_addFile('truc')
        bidon1 = getattr(self.plominoDatabase.ressources, 'truc')
        self.plominoDatabase.manage_addFile(resourceInfos['name'])
        obj = getattr(self.plominoDatabase.resources, resourceInfos['name'])
        print bidon1
        print self.plominoDatabase.resources._objects
        #obj.meta_type = fileMimeType
        #print resourceInfos['content']
        obj.update_data(resourceInfos['content'].decode('base64'), content_type=resourceInfos['type'])
        print obj.__class__
#            
#        except Exception, inst:
#            print type(inst)     # the exception instance
#            print inst.args      # arguments stored in .args
#            print inst           # __str__ allows args to printed directly

    def createElementInDatabase(self, elementInfos):
        """

        @param dict elementInfos : 
        @return  :
        """
        pass

    def addFileInDocument(self, fileInfos):
        """

        @param dict fileInfos : 
        @return  :
        """
        pass

    def addFileToResources(self, fileInfos):
        """

        @param dict fileInfos : 
        @return  :
        """
        pass