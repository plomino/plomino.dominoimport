# -*- coding: utf-8 -*-
#
# File: manager.py
#
# GNU General Public License (GPL)
#

__author__ = """"""
__docformat__ = 'plaintext'

from Products.Five import BrowserView

from plomino.dominoimport.exceptions import ImportDXLException
from plomino.dominoimport.interfaces import IDominoImporter

from Products.CMFPlomino.config import MSG_SEPARATOR

import logging
logger = logging.getLogger('Plomino')

class DominoImportManager(BrowserView):
    """ allow to manage domino file import
    """
    
    def __init__(self, context, request):
        """Initialize browserview"""
        self.context = context
        self.request = request

    def manageImportDXL(self):
        """
        DXL importation form manager: if file ok, call parseDXL() (ou bien processImportDXL(REQUEST))
        """            
        # init
        importer=IDominoImporter(self.context)
        
        infoMsg = ''
        error = False
        
        # get file name
        fileToImport = self.request.get('filename', None)
    
        (formResult, viewResult, docsResult) = importer.processImportDXL(fileToImport)
        
        if formResult != (0, 0):
            infoMsg = infoMsg + 'Forms imported: ' + \
            str(formResult[0]) + ' succeeded, ' + \
            str(formResult[1]) + ' failed.' + MSG_SEPARATOR

        if viewResult != (0, 0):
            infoMsg = infoMsg + 'Views imported: ' +  \
            str(viewResult[0]) + ' succeeded, ' +  \
            str(viewResult[1]) + ' failed.' + MSG_SEPARATOR
        
        if docsResult != (0, 0):
            infoMsg = infoMsg + 'Documents imported: ' +  \
            str(docsResult[0]) + ' succeeded, ' +  \
            str(docsResult[1]) + ' failed.' + MSG_SEPARATOR
            
#            except ImportDXLException, e:            
#                infoMsg = infoMsg + 'error while importing : %s' % (e) + MSG_SEPARATOR 
#                error = True

#        except Exception, e:
#            infoMsg = 'file required : %s' % (e) + MSG_SEPARATOR 
#            logger.info(e)
#            error = True

        logger.info(infoMsg)

        #write message
        self.context.writeMessageOnPage(infoMsg, self.request, '', error)
        
        #redirect
        self.request.RESPONSE.redirect(self.context.absolute_url()+'/dominoimport')
