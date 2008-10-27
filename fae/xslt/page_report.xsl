<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:include href="messages.xsl"/>
  <xsl:include href="context_header.xsl"/>

  <!-- output -->
  <xsl:output
      encoding="UTF-8"
      indent="yes"
      omit-xml-declaration="yes"
      method="xml"/>

  <xsl:strip-space elements="*"/>

  <xsl:param name="id"/><!-- not used -->
  <xsl:param name="pc"/>
  <xsl:param name="section"/>
  <xsl:param name="pid"/>
  <xsl:param name="title"/>
  <xsl:param name="nodata"/>

  <xsl:variable name="url" select="/results/pages/page-info[@id=$pid]/name"/>
  <xsl:variable name="testdoc" select="document('../xml/testdoc.xml')/testdoc"/>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">
    <xsl:variable name="page" select="/results/page[@id=$pid]"/>

    <h1><xsl:value-of select="$title"/></h1>

    <xsl:call-template name="context-header">
      <xsl:with-param name="url" select="/results/pages/page-info[@id=$pid]/name"/>
      <xsl:with-param name="page-title" select="/results/pages/page-info[@id=$pid]/title"/>
    </xsl:call-template>

    <xsl:apply-templates select="$testdoc//section[@id=$section]">
      <xsl:with-param name="page" select="$page"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="section">
    <xsl:param name="page"/>

    <h2><xsl:apply-templates select="name"/></h2>

    <xsl:apply-templates select="category">
      <xsl:with-param name="page" select="$page"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="category">
    <xsl:param name="page"/>

    <xsl:if test="descendant::page">
      <h3 id="{@id}">
        <xsl:apply-templates select="name"/>
        <xsl:apply-templates select="link">
          <xsl:with-param name="name" select="name"/>
        </xsl:apply-templates>
      </h3>

      <ul>
        <xsl:apply-templates select="best-practice">
          <xsl:with-param name="page" select="$page"/>
        </xsl:apply-templates>
      </ul>
    </xsl:if>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="best-practice">
    <xsl:param name="page"/>

    <xsl:if test="child::page">
      <li>
        <xsl:call-template name="new-rule"/>
        <xsl:apply-templates select="rule"/>
      </li>
      <!-- TO DO: display info element as well -->

      <xsl:for-each select="page">
        <xsl:variable name="id" select="@id"/>

        <xsl:choose>
          <xsl:when test="$page/test[@id=$id]">
            <xsl:apply-templates select="$messages">
              <xsl:with-param name="curr-test" select="$page/test[@id=$id]"/>
            </xsl:apply-templates>
          </xsl:when>
          <xsl:otherwise>
            <div style="margin-bottom: 1em"><xsl:value-of select="$nodata"/></div>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
    </xsl:if>
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
