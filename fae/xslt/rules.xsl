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
    <xsl:apply-templates select="testdoc/section"/>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="section">
    <h2><xsl:apply-templates select="name"/></h2>

    <xsl:apply-templates select="category"/>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="category">
    <xsl:if test="descendant::page">
      <h3>
        <xsl:apply-templates select="name"/>
        <xsl:apply-templates select="link">
          <xsl:with-param name="name" select="name"/>
        </xsl:apply-templates>
      </h3>

      <ul>
        <xsl:apply-templates select="best-practice"/>
      </ul>
    </xsl:if>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="best-practice">
    <li>
      <xsl:call-template name="new-rule"/>
      <xsl:apply-templates select="rule"/>
      <xsl:if test="info"><blockquote class="ruleinfo"><xsl:apply-templates select="info"/></blockquote></xsl:if>
    </li>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="elem">
    <code class="elem"><xsl:apply-templates/></code>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="attr">
    <code class="attr"><xsl:apply-templates/></code>
  </xsl:template>

</xsl:transform>
