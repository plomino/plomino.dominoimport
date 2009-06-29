# -*- coding: utf-8 -*-
#
# File: importer.py
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

from zope.interface import Interface, implements

from interfaces import IDominoImporter

from exceptions import ImportDXLException
from dxlParser import DXLParser
from plominoBuilder import PlominoBuilder


import logging
logger = logging.getLogger('Plomino')

class DominoImporter(object):
    """
    Class used to import a DXL file from Domino to Plomino
    """
    implements(IDominoImporter)
    
    
    def __init__(self, context):
        """Initialize adapter."""
        self.context = context
        
    def processImportDXL(self, fileToImport):
        """
        Process import of the file
        """
        results = {'resources': [0, 0], 'agents': [0, 0], 'forms': [0, 0], 'views': [0, 0], 'docs': [0, 0]}

        # Parse the DXL file ----
        myDxlParser = DXLParser()
        myDxlParser.parseDXLFile(fileToImport)
        
#        print 'file parsed'
#        print len(myDxlParser.getResources()), 'resources'
#        print len(myDxlParser.getAgents()), 'agents'
#        print len(myDxlParser.getForms()), 'forms'
#        print len(myDxlParser.getViews()), 'views'
#        print len(myDxlParser.getDocs()), 'docs'

        # Create the elements in the Plomino database ----
        myPlominoBuilder = PlominoBuilder(self.context)

        # create resources
        for resource in myDxlParser.getResources():
            try:
                myPlominoBuilder.createResource(resource)
                results['resources'][0] += 1
            except Exception, inst:
                results['resources'][1] += 1
                #print type(inst), inst

        # create forms
        for form in myDxlParser.getForms():
            try:
                myPlominoBuilder.createForm(form)
                results['forms'][0] += 1
            except Exception, inst:
                results['forms'][1] += 1
                print type(inst), inst

        # create views
        for view in myDxlParser.getViews():
            try:
                myPlominoBuilder.createView(view)
                results['views'][0] += 1
            except Exception, inst:
                results['views'][1] += 1
                print type(inst), inst

        # create docs
        for doc in myDxlParser.getDocs():
            try:
                myPlominoBuilder.createDoc(doc)
                results['docs'][0] += 1
            except Exception, inst:
                results['docs'][1] += 1
                print type(inst), inst
        
        # create agents
        for agent in myDxlParser.getAgents():
            try:
                myPlominoBuilder.createAgent(agent)
                results['agents'][0] += 1
            except Exception, inst:
                results['agents'][1] += 1
                print type(inst), inst
        
        self.context.getIndex().refresh()
        print results
        
        return results
    
        # Erreurs possibles
        
#        Import du fichier
#Erreur XML
#fichier non conforme à la DTD
#Database vide ?
#La database Plomino doit-elle être vide ?
#Création des forms
#Sur les field et sur le layout.
#Création des Views
#Warning ou alert: le form indiqué dans la views ne correspond pas à un form existant
#Warning ou alert: la formula indiquée dans la column ne correspond pas à un field existant
#Création de Documents
#Warning: le form indiqué ne correspond pas à un form existant

    