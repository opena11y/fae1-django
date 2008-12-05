<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:include href="context_header.xsl"/>

  <!-- output -->
  <xsl:output
      encoding="UTF-8"
      indent="yes"
      omit-xml-declaration="yes"
      method="xml"/>

  <xsl:strip-space elements="*"/>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">
    <ul>
      <xsl:for-each select="testdoc/section/category/best-practice">
        <xsl:sort select="@new" order="descending"/>
        <xsl:apply-templates select="."/>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="best-practice">
    <li>
      <xsl:apply-templates select="ancestor::category/name"/><!--
      <xsl:value-of select="@new"/> (<xsl:value-of select="@ref"/>): <xsl:apply-templates select="name"/>-->
    </li>
  </xsl:template>

</xsl:transform>
