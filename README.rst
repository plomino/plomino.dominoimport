Introduction
============

Allows to import Lotus Notes Domino databases (design + documents) into
Plomino.

How to use it
-------------

* Export your Lotus Notes database as DXL (Domino XML Language).
* ``plomino.dominoimport`` adds a new "DXL import" tab on your Plomino
  databases. Select this tab, and upload your DXL file.

Features
--------

* Forms and their fields, views and their columns are all imported.
* Field settings are imported for most field types.
* Documents are imported with their attached files.
* Formulas and Lotus scripts are imported as comments. They must be manually
  translated into Plomino formulas.
