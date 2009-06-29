RICHTEXT_STYLES = {"anchor": {"balise":"a", "att_name": "name"},
                     "par" : {"balise":"p", "redo": True},
                     "block": {"balise":"div", "redo": True},
                     "span": {"balise":"span", "redo": True},
                     "table": {"balise":"table", "redo": True},
                     "tablerow": {"balise":"tr", "redo": True},
                     "tablecell": {"balise":"td", "redo": True},
                     "break": {"balise": "br", "end_tag": False},
                     "horizrule": {"balise": "hr", "end_tag": False},
                     "picture": {"balise": "img", "att_alt": "alttext", "end_tag": False},
                     "attachmentref": {"balise": "a", "att_href": "name"}
#                     "field": {"balise": "span", "att_class":"plominoFieldClass", "content": "name"},
#                     "subform": {"balise": "span", "att_class":"plominoSubformClass", "content": "name"},
#                     "subformref": {"balise": "span", "att_class":"plominoSubformClass", "content": "name"}
#                     "nom_element_DXL": {"balise": "balise_html_correspondante", "att_class":"nom_classe", "att_name":"nom_attribut DXL à récupérer", "content":"nom_attribut DXL à récupérer"}
}
#                     "sectiontitle": ["h2"],

# LIMIT_SIZE_FOR_DISCREET = 14
# idée de structure du dict pour prendre en compte
# "%richtext": [balise, {class}
# "par": ["p", {"normal": "", "discreet": "discreet"} 

FIELD_TYPES = {"text": "TEXT",
                  "password": "TEXT",
                  "number": "NUMBER",
                  "datetime": "DATETIME",
                  "richtext": "RICHTEXT",
                  "richtextlite": "RICHTEXT",
                  "names": "NAME",
                  "authors": "NAME",
                  "readers": "NAME",
                  "keyword": "SELECTION",
                  }

FIELD_TYPES_ATTR = {"combobox": "SELECT",
                    "listbox": "MULTISELECT",
                    "dialoglist": "MULTISELECT",
                    "checkbox": "CHECKBOX",
                    "radiobutton": "RADIO",
                    # separator
                    "comma": ","}

# <!ENTITY % field.types "
#text | ok
#number | ok
#datetime | ok
#richtext | ok
#keyword | ok
#names | ok
#authors | ok
#readers | ok
#password | ok
#formula | => champs computed de type texte -> à faire
#timezone | NA
#richtextlite | ok -> richtext
#color NA ">

FIELD_MODES = {"editable": "EDITABLE",
                 "computed": "COMPUTED",
                 "computedfordisplay": "DISPLAY",
                 "computedwhencomposed": "CREATION"}

DOMINO_MIME_TYPES = {"Adobe Acrobat Document": "pdf",
             "XML Document": "xml",
             "xmlfile": "xml",
             "AcroExch.Document": "pdf",
             "htmlfile": "html"
             }

DOMINO_IMAGE_FORMAT = ['jpeg', 'gif', 'cfg']

DOMINO_CODE_TYPE = ['lotusscritp', 'formula', 'lotusscript', 'javaproject', 'simpleaction', 'javascript']