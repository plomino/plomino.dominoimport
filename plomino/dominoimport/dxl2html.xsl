<?xml version="1.0" encoding="UTF-16"?>
<!--
Document : dxl2html.xsl
Created on : 4. Oktober 2002, 09:23
Author : IMTUE
Description:
Purpose of transformation follows.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:dxl="http://www.lotus.com/dxl">
<xsl:output method="xml" version="1.0" omit-xml-declaration="no" indent="yes" media-type="text/html"/>
<!-- template rule matching source root element -->
<xsl:template match="/">
<xsl:apply-templates select="dxl:document"/>
</xsl:template>
<xsl:template match="dxl:document">
<html>
<head>
<title>Domino Dokument</title>
</head>
<body>
<xsl:apply-templates select="dxl:noteinfo"/>
<table cellpadding="0" cellspacing="0" border="1" bordercolor="black">
<xsl:for-each select="dxl:item">
<tr>
<td>
<xsl:value-of select="@name"/>
</td>
<td>
<xsl:choose>
<xsl:when test="@name = 'Body'">
<xsl:apply-templates select="dxl:richtext"/>
</xsl:when>
<xsl:otherwise>
<xsl:value-of select="."/>
</xsl:otherwise>
</xsl:choose>
</td>
</tr>
</xsl:for-each>
</table>
</body>
</html>
</xsl:template>
<!-- Process the "noteinfo" element -->
<xsl:template match="dxl:noteinfo">
DocumentID: <xsl:value-of select="@noteid"/>
<br/>
</xsl:template>
<!-- Process "richtext" elements -->
<xsl:template match="dxl:richtext">
<xsl:for-each select="*">
<xsl:call-template name="richtext.block"/>
</xsl:for-each>
</xsl:template>
<xsl:template name="richtext.block">
<xsl:choose>
<xsl:when test="name()='par'">
<p>
<xsl:for-each select="text()|*">
<xsl:choose>
<xsl:when test="name()">
<xsl:call-template name="richtext.inline"/>
</xsl:when>
<xsl:otherwise>
<xsl:value-of select="."/>
</xsl:otherwise>
</xsl:choose>
</xsl:for-each>
</p>
</xsl:when>
<xsl:when test="name()='pardef'"/>
<xsl:when test="name()='table'"/>
<xsl:when test="name()='subformref'"/>
<xsl:when test="name()='section'"/>
<xsl:when test="name()='block'"/>
</xsl:choose>
</xsl:template>
<xsl:template name="richtext.inline">
<xsl:call-template name="richtext.nonhot.inline"/>
<xsl:call-template name="richtext.hot.inline"/>
</xsl:template>
<xsl:template name="richtext.nonhot.inline">
<xsl:choose>
<xsl:when test="name()='run'"/>
<xsl:when test="name()='break'">
<br/>
</xsl:when>
<xsl:when test="name()='field'"/>
<xsl:when test="name()='sharedfieldref'"/>
<xsl:when test="name()='picture'"/>
<xsl:when test="name()='horizrule'"/>
<xsl:when test="name()='anchor'"/>
</xsl:choose>
</xsl:template>
<xsl:template name="richtext.hot.inline">
<xsl:choose>
<xsl:when test="name() = 'attachmentref'"/>
<xsl:when test="name() = 'attachmentref'"/>
<xsl:when test="name() = 'attachmentref'"/>
<xsl:otherwise>
<xsl:call-template name="richtext.links"/>
</xsl:otherwise>
</xsl:choose>
</xsl:template>
<xsl:template name="richtext.links">
<xsl:choose>
<xsl:when test="name() = 'doclink'"/>
<xsl:when test="name() = 'viewlink'"/>
<xsl:when test="name() = 'databaselink'"/>
<xsl:when test="name() = 'urllink'"/>
<xsl:when test="name() = 'namedelementlink'"/>
</xsl:choose>
</xsl:template>
</xsl:stylesheet>
