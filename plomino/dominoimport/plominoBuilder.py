# -*- coding: utf-8 -*-
#
# File: plominoBuilder.py
#
# GNU General Public License (GPL)
#

"""
Created on 22 June 2009

@author: Emmanuelle Helly

"""

__author__ = """Emmanuelle Helly"""
__docformat__ = 'plaintext'

from binascii import a2b_base64
import mimetypes

class PlominoBuilder(object):
    """
    create all elements in the correct database from a dict 
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
        """
        viewId = self.plominoDatabase.invokeFactory(viewInfos['type'], 
                                                    id=viewInfos['id'])
        #print 'creating view:', viewId
        if viewId is not None:
            obj = self.plominoDatabase.getView(viewId)
            obj.setTitle(viewInfos['title'])
            obj.setSelectionFormula(viewInfos['SelectionFormula'])
            obj.setFormFormula(viewInfos['FormFormula'])
            
            # Create the columns
            for columnInfos in viewInfos['columns']:
                self.createColumn(columnInfos, self.plominoDatabase.getView(viewId))

    def createColumn(self, columnInfos, container):
        """
        Create column in the database

        @param dict columnInfos : 
        @param dict viewId : 
        @return string :
        """
        columnId = container.invokeFactory(columnInfos['type'], 
                                           id=columnInfos['id'])
        #print 'creating column:', columnId
        if columnId is not None:
            obj = container.getColumn(columnId)
            obj.setTitle(columnInfos['title'])
            obj.setFormula(columnInfos['formula'])
            obj.setPosition(columnInfos['position'])
            obj.at_post_create_script()

    def createDoc(self, docInfos):
        """
        Create document in the database

        @param dict docInfos : 
        @return string :
        """
        pass

    def createItem(self, itemInfos, container):
        """
        Create document in the database

        @param dict itemInfos : 
        @return string :
        """
        pass

    def createAgent(self, agentInfos):
        """
        Create agent in the database

        @param dict agentInfos : 
        @return string :
        """
        agentId = self.plominoDatabase.invokeFactory(agentInfos['type'], 
                                                     id=agentInfos['id'])
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