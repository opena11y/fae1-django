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

  <xsl:param name="id"/>
  <xsl:param name="section"/>
  <xsl:param name="pid"/>
  <xsl:param name="ruleset"/>
  <xsl:param name="title"/>

  <xsl:variable name="prefix">/report/<xsl:value-of select="$id"/>/page/</xsl:variable>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">
    <xsl:variable name="pg-count" select="/results/meta/pg-count"/>

    <h1><xsl:value-of select="$title"/></h1>

    <xsl:call-template name="context-header">
      <xsl:with-param name="ruleset-current" select="$ruleset"/>
    </xsl:call-template>

    <ol title="List of Pages">
      <xsl:for-each select="/results/pages/page-info">
        <xsl:variable name="href" select="concat($prefix, @id, '/', $section, '/')"/>
        <li><xsl:if test="@id = $pid"><xsl:attribute name="class">menu-highlight</xsl:attribute></xsl:if><a href="{$href}" title="{title}"><xsl:apply-templates select="name"/></a></li>
      </xsl:for-each>
    </ol>
  </xsl:template>

</xsl:transform>
