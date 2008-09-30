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
    <xsl:variable name="count" select="count(/results/meta/urls/url)"/>

    <h1>List of URLs</h1>

    <xsl:call-template name="context-header">
      <xsl:with-param name="display-urls" select="false()"/>
    </xsl:call-template>

    <xsl:for-each select="/results/meta/urls/url">
      <div title="{concat('URL: ', position(), ' of ', $count)}"><xsl:apply-templates/></div>
    </xsl:for-each>

  </xsl:template>

</xsl:transform>
