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

from xml.dom.minidom import parse, getDOMImplementation

import re
p_for_id = re.compile('^[A-Za-z0-9][A-Za-z0-9_.]+$')
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

    def extractResourcesFromDXL(self, dxlFileContent):
        """
        Extract file ressource from the DXL parsed file
        """
        
        file = {}
        
        # Get all the image resources of the DXL file
        fileNodes = dxlFileContent.getElementsByTagName("imageresource")
        print 'extract resource'

        for fileElement in fileNodes:
            file['name'] = fileElement.getAttribute('name')

            # Get the file content from jpeg or else node 
            child = fileElement.firstChild
            while child is not None:
                if child.nodeName in DOMINO_IMAGE_FORMAT:
                    file['content'] = child.firstChild.nodeValue
                if child.nodeName == 'item' and child.getAttribute('name') == '$MimeType':
                    file['type'] = child.getElementsByTagName('text')[0].firstChild.nodeValue

                child = child.nextSibling
            
            self.resources.append(file)

        for r in self.resources:
            print r['name']
        
        
    def getIdTitleAttributes(self):
        """
        Get the Id and the Title from a DXLFileContent
        @return tuple :
        """
        # check if the data match the correct pattern
        if p_for_id.match(dxlFileContent.getAttribute('name')) is not None:
            id = dxlFileContent.getAttribute('name')
        elif p_for_id.match(dxlFileContent.getElementsByTagName('noteinfo')[0].getAttribute('unid')) is not None:
            id = dxlFileContent.getElementsByTagName('noteinfo')[0].getAttribute('unid')
        else:
            id = ''
        
        if p_for_title.match(dxlFileContent.getAttribute('name')) is not None:
            title = dxlFileContent.getAttribute('name')
        else:
            title = ''
            
        return (id, title)

    def richtext2Html(self):
        """
        transform a richtext element from dxl to html, using an xsl stylesheet
        @return string :
        """
        pass

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

