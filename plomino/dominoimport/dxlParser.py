# -*- coding: utf-8 -*-
#
# File: dxlParser.py
#
# GNU General Public License (GPL)
#

"""
Created on 22 June 2009

@author: Emmanuelle Helly

File DxlConfig.py is required
"""

__author__ = """Emmanuelle Helly"""
__docformat__ = 'plaintext'

from xml.dom.minidom import parse, getDOMImplementation

import re
p_for_id = re.compile('^[A-Za-z0-9][A-Za-z0-9_. ]+$')
p_for_title = re.compile('^[A-Za-z0-9][A-Za-z0-9_. ]+$')

from dxlConfig import *

import logging
logger = logging.getLogger('Plomino')

class DXLParser(object):
    """
    parser used to transform dxl element to mapping object
    (not implemented yet)
    """

    """ ATTRIBUTES
    forms  (private)
    views  (private)
    docs  (private)
    resources  (private)
    """
    
    forms = []
    views = []
    docs = []
    resources = []
    agents = []
    
    def __init__(self):
        """
        Initialize parser
        """

    def getForms(self):
        return self.forms

    def getViews(self):
        return self.views

    def getDocs(self):
        return self.docs

    def getResources(self):
        return self.resources
        
    def getAgents(self):
        return self.agents
        
    def parseDXLFile(self, file):
        """
        Parse dxl file and set resources, forms, views, and agents sequences
        """
        dxlFileContent = None
        try:
            dxlFileContent = parse(file)
#        except TypeErrormismatched, e:
#            print str(TypeError) + str(e)
        except Exception, e:
            logger.info(str(type(e)) + " - " + str(e))
            #print str(type(e)) + " - " + str(e)
        
        if dxlFileContent is not None:
            self.extractResourcesFromDXL(dxlFileContent)
            self.extractForms(dxlFileContent)
            self.extractViews(dxlFileContent)
            self.extractDocs(dxlFileContent)
            self.extractAgents(dxlFileContent)

    def extractResourcesFromDXL(self, dxlFileContent):
        """
        Extract file resources from the DXL parsed file
        """

        # Get all the image resources of the DXL file
        fileNodes = dxlFileContent.getElementsByTagName("imageresource")
        print 'extracting resource ...'

        for fileElement in fileNodes:
            file = {}
            file['name'] = fileElement.getAttribute('name')

            # Get the file content from jpeg or else node 
            child = fileElement.firstChild
            while child is not None:
                if child.nodeName in DOMINO_IMAGE_FORMAT:
                    file['content'] = child.firstChild.nodeValue
                if child.nodeName == 'item' and child.getAttribute('name') == '$MimeType':
                    file['type'] = child.getElementsByTagName('text')[0].firstChild.nodeValue

                child = child.nextSibling
            
            print file['name'], file['type']
            
            self.resources.append(file)
    
    def extractForms(self, dxlFileContent):
        """
        Extract forms from the DXL parsed file
        """
        
        print 'extracting forms ...'
        forms = dxlFileContent.getElementsByTagName("form") + dxlFileContent.getElementsByTagName("subform")

        for form in forms:
            dico = {}
            dico['type'] = 'PlominoForm'
            dico['id'], dico['title'] = self.getIdTitleAttributes(form)
            
            # set the layout from "body" element
            dico['formLayout'] = self.richtextToHtml(form.getElementsByTagName("body")[0])
            
            # import all the fields included in this form
            dico['fields'] = self.extractFields(form)
            
            # self.extractInsertedFiles(form)
            self.forms.append(dico)

    def extractFields(self, dxlFileContent):
        """
        Extract fields from the DXL parsed file
        """
        
        extractedFields = []
        print 'extracting fields ...'
        fields = dxlFileContent.getElementsByTagName("field")
        
        for field in fields:
            dico = {}
            settings = {}
            dico['type'] = 'PlominoField'
            dico['id'], dico['title'] = self.getIdTitleAttributes(field)

            # Field types ----
            # set the fieldType from the dict in dxlConfig.py    
            if field.getAttribute('type') in FIELD_TYPES:
                dico['FieldType'] = FIELD_TYPES[field.getAttribute('type')]
            else:
                dico['FieldType'] = 'TEXT'
            
            # import the field settings ----
            # - Text field
            if dico['FieldType'] == 'TEXT':
                # widget
                if field.getAttribute("multiline"):
                    settings['widget'] = 'TEXTAREA'
                else:
                    settings['widget'] = 'TEXT'
    
            # - Number field
            if dico['FieldType'] == 'NUMBER':
                settings['type'] = 'FLOAT' # to avoid loosing information from dxl file 
    
                    
            # - Selection field
            if dico['FieldType'] == 'SELECTION':
                # widget
                if field.getElementsByTagName("keywords")[0].getAttribute("ui") in FIELD_TYPES_ATTR:
                    settings['widget'] = FIELD_TYPES_ATTR[field.getElementsByTagName("keywords")[0].getAttribute('ui')]
                else:
                    settings['widget'] = 'SELECT'
                
                # list of items
                if field.getElementsByTagName("textlist")[0].getElementsByTagName("text") is not None:
                    selectionList = []
                    for entry in field.getElementsByTagName("textlist")[0].getElementsByTagName("text"):
                        selectionList.append(entry.firstChild.nodeValue)
                    
                    settings['selectionlist'] = selectionList
                    
                else:
                    settings['selectionlist'] = ['Selection list not set']
                # TODO: tester lorsque les paramètres n'existent pas
                
            # - Name field
            if dico['FieldType'] == 'NAME':
                # type
                if field.getAttribute("allowmultivalues"):
                    settings['type'] = 'MULTI'
                    # separator
    #                if field.getAttribute("listinputseparators") in FIELD_TYPES_ATTR:
    #                    settings['separator'] = FIELD_TYPES_ATTR[field.getAttribute("listinputseparators")]
    #                else:
    #                    settings['separator'] = ''
    
                else:
                    settings['type'] = 'SINGLE'

            dico['settings'] = settings

            # Field mode ----
            if field.getAttribute('kind') in FIELD_MODES:
                dico['FieldMode'] = FIELD_MODES[field.getAttribute('kind')]
            else:            
                dico['FieldMode'] = 'EDITABLE'

            extractedFields.append(dico)

        return extractedFields
        
    def extractViews(self, dxlFileContent):
        """
        Extract views from the DXL parsed file
        """
        
        #print 'extracting views ...'
        views = dxlFileContent.getElementsByTagName("view")

        for view in views:
            dico = {}
            dico['type'] = 'PlominoView'
            dico['id'], dico['title'] = self.getIdTitleAttributes(view)

            # get the Form and SelectionFormula attribute
            codeView = dxlFileContent.getElementsByTagName('code')[0]
            if codeView.getAttribute('event') == 'selection':
                if codeView.getElementsByTagName('formula')[0].firstChild.nodeValue == '@All':
                    dico['SelectionFormula'] = 'True'
                else:
                    dico['SelectionFormula'] = '#'#, codeView.getElementsByTagName('formula')[0].firstChild.nodeValue
            
            dico['FormFormula'] = '#'

            # import all the columns included in this view
            dico['columns'] = []
            dico['columns'] = self.extractColumns(view)
            
            self.views.append(dico)
        
    def extractColumns(self, dxlFileContent):
        """
        Extract columns from the DXL parsed file
        """
        extractedCols = []
        position = 1
        #print 'extracting columns ...'
         
        columns = dxlFileContent.getElementsByTagName('column')
        
        for column in columns:
            dico = {}
            dico['type'] = 'PlominoColumn'
            dico['id'] = column.getAttribute('itemname')
            dico['title'] = column.getElementsByTagName("columnheader")[0].getAttribute('title')
            dico['position'] = position
            position += 1
            
            # get the Formula attribute for this column
            if column.getElementsByTagName('code') != []:
                codeColumns = column.getElementsByTagName('code')[0]
                if codeColumns.getAttribute('event') == 'value':
                    dico['formula'] ='plominoDocument.' + \
                                    codeColumns.getElementsByTagName('formula')[0].firstChild.nodeValue
            else:
                dico['formula'] ='plominoDocument.' + dico['id']
                
                # TODO: cherche si la formule matche avec un field connu
                # utiliser les regex pourrait être un bon moyen
                # comment récupérer les champs field ? 
                # par self.getFields ou vérifier que self.getField(attValue) existe ?
                # mais comment récupérer les bon form sans perdre de temps à tout parcourir ?
            
            extractedCols.append(dico)
            
        return extractedCols

    def extractDocs(self, dxlFileContent):
        """
        Extract docs from the DXL parsed file
        """
        
        #print 'extracting docs ...'
        
        docs = dxlFileContent.getElementsByTagName("document")

        for doc in docs:
            dico = {}
            dico['type'] = 'PlominoDocument'
            dico['id'], dico['title'] = self.getIdTitleAttributes(doc)
            dico['form'] = doc.getAttribute('form')
            # import all the items included in this doc
            
            dico['items'] = []
            dico['items'] = self.extractItems(doc)
            
            self.docs.append(dico)

    def extractItems(self, dxlFileContent):
        """
        Extract items from the DXL parsed file
        """
        #print 'extracting items ...'
        extractedItems = []
        items = dxlFileContent.getElementsByTagName("item")
        
        for item in items:
            dico = {}
            # Get item type
            if item.hasChildNodes():
                # REM: getting first node element could be in a class derivating of minidom ...
                child = item.firstChild
                while child is not None and child.nodeType is not child.ELEMENT_NODE:
                    child = child.nextSibling

                if child is not None:
                    dico['type'] = child.nodeName
        
            # Get item name
            if item.nodeType is item.ELEMENT_NODE and item.hasAttribute('name'):
                dico['name'] = item.getAttribute('name')

            if dico['type'] in FIELD_TYPES:
                
                # number ----
                if dico['type'] == 'number':
                    dico['value'] = child.firstChild.nodeValue
                
                # text ----
                elif dico['type'] == 'text':
                    # there may be some break tag, so get content recursively
                    dico['value'] = ''
                    subchild = child.firstChild
                    while subchild is not None:
                        if subchild.nodeName == 'break':
                            dico['value'] += '<br />'
                        elif subchild.nodeName == '#text':
                            dico['value'] += str(subchild.data).replace('\n', '')
        
                        subchild = subchild.nextSibling

                # richtext ----
                elif dico['type'] == 'richtext':
                    dico['value'] = '#'

                # else ----
                else:
                    dico['value'] = '#'

            #print dico
            extractedItems.append(dico)

        return extractedItems
    
    def extractAgents(self, dxlFileContent):
        """
        Extract agents from the DXL parsed file
        """
        
        print 'extracting agents ...'

        agents = dxlFileContent.getElementsByTagName("agent")

        for agent in agents:
            dico = {}
            dico['type'] = 'PlominoAgent'
            dico['id'], dico['title'] = self.getIdTitleAttributes(agent)
            print dico['id']
            self.agents.append(dico)

    def getIdTitleAttributes(self, dxlFileContent):
        """
        Get the Id and the Title from a DXLFileContent
        @return tuple :
        """
        # check if the data match the correct pattern
        if p_for_id.match(dxlFileContent.getAttribute('name')) is not None:
            id = str(dxlFileContent.getAttribute('name')).replace(' ', '_')
        elif p_for_id.match(dxlFileContent.getElementsByTagName('noteinfo')[0].getAttribute('unid')) is not None:
            id = str(dxlFileContent.getElementsByTagName('noteinfo')[0].getAttribute('unid')).replace(' ', '_')
        else:
            id = ''
        
        if p_for_title.match(dxlFileContent.getAttribute('name')) is not None:
            title = dxlFileContent.getAttribute('name')
        else:
            title = ''
            
        return (id, title)

    def richtext2Html(self, dxlFileContent):
        """
        transform a richtext element from dxl to html, using an xsl stylesheet
        @return string :
        """
        return ''

    def richtextToHtml(self, node, formId=None, deep_header=1, gettext=True):
        """
        transform a richtext in a html (String)
        @return string :
        """
        html_content = ''
        list = "none"
        defId = 0
        child = node.firstChild
        
        # parcourt tous les enfants de node, et réapplique la méthode selont les cas
        while child is not None:
            name = child.nodeName            
            
            # TODO: Récupérer les paramètres de l'élément pour choisir les styles ? later version
            
            if gettext and name == '#text':
                html_content += unicode(child.data).replace('\n', '')
            
            # links to attach files ----
            elif name == 'attachmentref' or name == 'objectref':
                filename = child.getAttribute('name')
                if child.getAttribute('description') in DOMINO_MIME_TYPES:
                    filename += '.' + DOMINO_MIME_TYPES[child.getAttribute('description')]
                html_content += '<a href="getfile?filename=' + filename + '">' + filename + '</a>'
            
            elif name == 'picture':
                html_content += self.richtextToHtml(child, formId, deep_header)

            elif name == 'imageref':
                filename = child.getAttribute('name')
                html_content += '<img src="resources/' + filename + '" />'
                
                
            elif name == 'jpeg':
                filename = 'image'
                if formId is not None:
                    html_content += '<img src="resources/' + filename + '" />'
                else:
                    html_content += '<img src="getfile?filename=' + filename + '" />'

            # To get the lists ----
            # REM: c'est une sacrée usine à gaz, on devrait utiliser les xls si on veut aller plus loin
            elif name == 'pardef':
                #defId = child.getAttribute('id')
                if child.hasAttribute('list'):
                    defId = child.getAttribute('id')
                    list = child.getAttribute('list')
                    if list == 'bullet':
                        html_content += '<ul>'
                    elif list == 'number':
                        html_content += '<ol>'
                else:
                    if list == 'bullet':
                        html_content += '</ul>'
                    elif list == 'number':
                        html_content += '</ol>'

                    list = "none"

            elif name == 'par':
                if child.hasAttribute('def') and child.getAttribute('def') != defId:
                    if list == 'bullet':
                        html_content += '</ul><p>' + self.richtextToHtml(child, formId, deep_header) + '</p>'
                    elif list == 'number':
                        html_content += '</ol><p>' + self.richtextToHtml(child, formId, deep_header) + '</p>'
                    elif list == 'none':
                        html_content += '<p>' + self.richtextToHtml(child, formId, deep_header) + '</p>'

                    list = "none"
                    
                elif list != "none": 
                    html_content += '<li>' + self.richtextToHtml(child, formId, deep_header) + '</li>'
                else:
                    html_content += '<p>' + self.richtextToHtml(child, formId, deep_header) + '</p>'

            # tags known in dxlConfig.py ----
            elif name in RICHTEXT_STYLES:
                
                # balise ouvrante et attributs
                html_content += '<' + RICHTEXT_STYLES[name]["balise"]
                
                if "att_class" in RICHTEXT_STYLES[name]:
                    html_content += ' class="' + RICHTEXT_STYLES[name]["att_class"]
                if "att_name" in RICHTEXT_STYLES[name]:
                    html_content += ' name="' + child.getAttribute(RICHTEXT_STYLES[name]["att_name"]) + '"'
                if "att_alt" in RICHTEXT_STYLES[name]:
                    html_content += ' alt="' + child.getAttribute(RICHTEXT_STYLES[name]["att_alt"]) + '"'
                if "att_src" in RICHTEXT_STYLES[name]:
                    html_content += ' src="' + child.getAttribute(RICHTEXT_STYLES[name]["att_href"]) + '"'
                if "att_href" in RICHTEXT_STYLES[name]:
                    html_content += ' href="' + child.getAttribute(RICHTEXT_STYLES[name]["att_src"]) + '"'
                
                if "end_tag" in RICHTEXT_STYLES[name] and not RICHTEXT_STYLES[name]["end_tag"]:
                    html_content += ' />'
                else:
                    html_content += '>'
                
                # contenu
                if "content" in RICHTEXT_STYLES[name]:
                    html_content += child.getAttribute(RICHTEXT_STYLES[name]["content"])
                
                # elements fils ?
                if "redo" in RICHTEXT_STYLES[name] and RICHTEXT_STYLES[name]["redo"]:
                    html_content += self.richtextToHtml(child, formId, deep_header)
                
                if "end_tag" in RICHTEXT_STYLES[name] and not RICHTEXT_STYLES[name]["end_tag"]:
                    html_content += ''
                else:
                    html_content += '</' + RICHTEXT_STYLES[name]["balise"] + '>'
                    
            # section ----
#            elif name == 'section':
#                deep_header += 1
#                html_content += self.richtextToHtml(child, deep_header)
#                
            elif name == 'sectiontitle':
                deep_header += 1
                html_content += '<h' + str(deep_header) + '>' + self.richtextToHtml(child, formId, deep_header) + '</h' + str(deep_header) + '>'
            
            # field ----
            elif name == 'field':
#                self.importField(child, formId)
                html_content += '<span class="plominoFieldClass">' + child.getAttribute('name') + '</span>'
            
            # subform ----
            elif name == 'subform' or name == 'subformref':
                 html_content += '<span class="plominoSubformClass">' + child.getAttribute('name') + '</span>'
            
            # TODO: check if subform is included, subformref references to a form in the file
            # REM: in Plomino, subform is allways out of a form, and a referece is made to it in the formlayout.

            elif name == 'run':
                if child.getAttribute('html'):
                    html_content += child.toxml()
                else:
                    html_content += self.richtextToHtml(child, formId, deep_header)

            
            else:
                html_content += self.richtextToHtml(child, formId, deep_header)

            child = child.nextSibling
            
        return html_content

