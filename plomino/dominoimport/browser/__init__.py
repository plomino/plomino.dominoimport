#
from Products.CMFPlomino.interfaces import IPlominoDatabase

class isPlominoDatabase(object):
    
    def __call__(self):
        return IPlominoDatabase.providedBy(self.context)