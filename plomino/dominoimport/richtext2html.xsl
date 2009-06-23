<?xml version="1.0" encoding="UTF-16"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:dxl="http://www.lotus.com/dxl">
<xsl:output method="xml" version="1.0" omit-xml-declaration="no" indent="yes" media-type="text/html"/>

<xsl:template match="/">
<xsl:apply-templates select="dxl:richtext"/>

</xsl:template>
</xsl:stylesheet>
