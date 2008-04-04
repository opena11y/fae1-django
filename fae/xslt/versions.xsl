<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

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
    <xsl:apply-templates select="versions/version"/>
  </xsl:template>

  <xsl:template match="versions/title">
    <h2><xsl:apply-templates/></h2>
  </xsl:template>

  <xsl:template match="version">
    <p>
      <xsl:apply-templates select="title"/>
      <xsl:apply-templates select="date"/>
    </p>

    <ol>
      <xsl:apply-templates select="item"/>
    </ol>
  </xsl:template>

  <xsl:template match="version/title">
    <strong><xsl:apply-templates/></strong>
  </xsl:template>

  <xsl:template match="version/date">
    <xsl:text> (</xsl:text><xsl:apply-templates/>)
  </xsl:template>

  <xsl:template match="list">
    <ul>
      <xsl:apply-templates match="item"/>
    </ul>
  </xsl:template>

  <xsl:template match="item">
    <li><xsl:apply-templates/></li>
  </xsl:template>

  <xsl:template match="note"/>

</xsl:transform>
