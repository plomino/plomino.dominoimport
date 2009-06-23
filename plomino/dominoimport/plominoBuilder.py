# -*- coding: utf-8 -*-
#
# File: manager.py
#
# GNU General Public License (GPL)
#

"""
Created on 20 may 2009

@author: Emmanuelle Helly

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
        
        formId = self.plominoDatabase.invokeFactory(formInfos['type'],
                                              id=formInfos['id'])
        print 'creating form:', formId
        if formId is not None:
            self.plominoDatabase.getForm(formId).setTitle(formInfos['title'])
            #self.importInsertedFiles(form, self.context.getForm(formId))
            
            # set the layout
            #self.context.getForm(formId).setFormLayout(formLayout)
            
            # Create the fields

    def createView(self, viewInfos):
        """
        Create view in the database

        @param dict viewInfos : 
        @return string :
        @author
        """
        viewId = self.createElementInDatabase(viewInfos)
        print 'creating view:', viewId
        if viewId is not None:
            self.plominoDatabase.getView(viewId).setTitle(viewInfos['title'])
            
            # Create the columns

    def createDoc(self, docInfos):
        """
        Create document in the database

        @param dict docInfos : 
        @return string :
        """
        pass

    def createAgent(self, agentInfos):
        """
        Create agent in the database

        @param dict agentInfos : 
        @return string :
        """
        agentId = self.createElementInDatabase(agentInfos)
        print 'creating agent:', agentId
        #self.plominoDatabase.at_post_create_script()

    def createResource(self, resourceInfos):
        """
        Add files into the database "resources" folder
        @param dict resourceInfos : 
        @return string :
        """
        print 'creating resource in database:', resourceInfos['name'] 
        #if not(hasattr(self.plominoDatabase.resources, resourceInfos['name'])):
        self.plominoDatabase.manage_addFile('truc')
        bidon1 = getattr(self.plominoDatabase.ressources, 'truc')
        print bidon1

        self.plominoDatabase.manage_addFile(resourceInfos['name'])
        obj = getattr(self.plominoDatabase.resources, resourceInfos['name'])
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
        elementId = None
        
        try:
            elementId=self.plominoDatabase.invokeFactory(elementInfos['type'], 
                                              id=elementInfos['id'])
    
        except ImportDXLException, e:
            logger.info('Error during import ' + elementInfos['type'] + ': ' + str(type(e)) + " - " + str(e))
            print str(type(e)) + " - " + str(e)
            
        except Exception, e:
            logger.info('Error during import ' + elementInfos['type'] + ': ' + str(type(e)) + " - " + str(e))
            print str(type(e)) + " - " + str(e)
        
        return elementId

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