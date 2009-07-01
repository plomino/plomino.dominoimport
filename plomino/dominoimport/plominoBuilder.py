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
        #print 'creating form:', formId
        if formId is not None:
            form = self.plominoDatabase.getForm(formId)
            form.setTitle(formInfos['title'])
            form.setFormLayout(formInfos['formLayout'])
            #self.importInsertedFiles(form, self.context.getForm(formId))

            # Create the fields
            for fieldInfos in formInfos['fields']:
                self.createField(fieldInfos, form)
            
            form.at_post_create_script()
            self.plominoDatabase.getIndex().refresh()

    def createField(self, fieldInfos, container):
        """
        Create field in the database

        @param dict fieldInfos : 
        @param plomino object container : 
        @return string :
        """
        fieldId = container.invokeFactory(fieldInfos['type'], 
                                           id=fieldInfos['id'])
        #print 'creating field:', fieldId
        
        if fieldId is not None:
            field = container.getFormField(fieldId)
            field.setTitle(fieldInfos['title'])
            field.setFieldType(fieldInfos['FieldType'])
            field.setFieldMode(fieldInfos['FieldMode'])
            field.setFormula(fieldInfos['formula'])
            field.setValidationFormula(fieldInfos['ValidationFormula'])

            adapt=field.getSettings()
            for key in fieldInfos['settings'].keys():
                v = fieldInfos['settings'][key]
                if v is not None:
                    setattr(adapt, key, v)

            field.at_post_create_script()
            self.plominoDatabase.getIndex().refresh()

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
            view = self.plominoDatabase.getView(viewId)
            view.setTitle(viewInfos['title'])
            view.setSelectionFormula(viewInfos['SelectionFormula'])
            view.setFormFormula(viewInfos['FormFormula'])
            
            # Create the columns
            for columnInfos in viewInfos['columns']:
                self.createColumn(columnInfos, view)
            
            view.at_post_create_script()
            self.plominoDatabase.getIndex().refresh()

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
            column = container.getColumn(columnId)
            column.setTitle(columnInfos['title'])
            column.setFormula(columnInfos['formula'])
            column.setPosition(columnInfos['position'])
            column.at_post_create_script()

    def createDoc(self, docInfos):
        """
        Create document in the database

        @param dict docInfos : 
        @return string :
        """
        #print 'creating doc:', docInfos['id']
        if docInfos['id'] != '':
            newDocId = self.plominoDatabase.invokeFactory(docInfos['type'], 
                                                    id=docInfos['id'])
            newDoc = self.plominoDatabase.getDocument(docInfos['id'])
        else:
            newDoc = self.plominoDatabase.createDocument()
            
        if newDoc is not None:
            if self.plominoDatabase.getForm(docInfos['form']) is not None:
                newDoc.setItem('Form', docInfos['form'])

                # TODO: create a default form if form does not exist ? in a later version
                # REM: doc is not saved if not associated with a existing form
                
                # Set the items of this document
                for itemInfos in docInfos['items']:
                    newDoc.setItem(itemInfos['name'], itemInfos['value'])
                    # TODO: check the value before set ?
                    #self.createItem(itemInfos, newDoc)

                # Add the files inserted in the document
                if docInfos['files'] != []:
                    if not hasattr(newDoc.getForm(), 'imported_files'):
                        fieldId = newDoc.getForm().invokeFactory('PlominoField', 
                                                                 id='imported_files',
                                                                 title='Imported Files',
                                                                 FieldType='ATTACHMENT')
                        newDoc.getForm().setFormLayout(newDoc.getForm().getFormLayout() + \
                                            '<p>Imported files: <span class="plominoFieldClass">imported_files</span></p>')
                    for fileInfos in docInfos['files']:
                        newDoc.setfile(a2b_base64(str(fileInfos['content'])), fileInfos['name'])

                newDoc.save()

            else:
                raise Exception

        self.plominoDatabase.getIndex().refresh()

#    def createItem(self, itemInfos, container):
#        """
#        Create document in the database
#        
#        !!!!!!! Not used in this version !!!!!!!!
#        
#        @param dict itemInfos : 
#        @return string :
#        """
#        
#        pass

    def createAgent(self, agentInfos):
        """
        Create agent in the database

        @param dict agentInfos : 
        @return string :
        """
        agentId = self.plominoDatabase.invokeFactory(agentInfos['type'], 
                                                     id=agentInfos['id'])
        #print 'creating agent:', agentId
        
        if agentId is not None:
            agent = getattr(self.plominoDatabase, agentId)
            agent.setContent(agentInfos['content'])
            agent.setScheduled(agentInfos['scheduled'])
            agent.at_post_create_script()

    def createResource(self, resourceInfos):
        """
        Add files into the database "resources" folder
        @param dict resourceInfos : 
        @return string :
        """
        #print 'creating resource in database:', resourceInfos['name'] 
        
        if not(hasattr(self.plominoDatabase, resourceInfos['name'])):
            self.plominoDatabase.resources.manage_addFile(resourceInfos['name'])
        obj = getattr(self.plominoDatabase.resources, resourceInfos['name'])
        #print self.plominoDatabase.resources._objects
        obj.update_data(resourceInfos['content'].decode('base64'), content_type=resourceInfos['type'])

#    def createElementInDatabase(self, elementInfos):
#        """
#
#        @param dict elementInfos : 
#        @return  :
#        """
#        elementId = None
#        
#        try:
#            elementId=self.plominoDatabase.invokeFactory(elementInfos['type'], 
#                                              id=elementInfos['id'])
#    
#        except ImportDXLException, e:
#            logger.info('Error during import ' + elementInfos['type'] + ': ' + str(type(e)) + " - " + str(e))
#            print str(type(e)) + " - " + str(e)
#            
#        except Exception, e:
#            logger.info('Error during import ' + elementInfos['type'] + ': ' + str(type(e)) + " - " + str(e))
#            print str(type(e)) + " - " + str(e)
#        
#        return elementId
#
#    def addFileInDocument(self, fileInfos):
#        """
#
#        @param dict fileInfos : 
#        @return  :
#        """
#        pass
#
#    def addFileToResources(self, fileInfos):
#        """
#
#        @param dict fileInfos : 
#        @return  :
#        """
#        pass