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

  <xsl:param name="id"/>
  <xsl:param name="pc"/>
  <xsl:param name="section"/>
  <xsl:param name="pid"/><!-- not used -->
  <xsl:param name="ruleset"/>
  <xsl:param name="title"/>
  <xsl:param name="nodata"/>

  <xsl:variable name="results" select="/results"/>
  <xsl:variable name="testdoc" select="document('../xml/testdoc.xml')/testdoc"/>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">
    <xsl:variable name="site" select="/results/site"/>

    <h1><xsl:value-of select="$title"/></h1>

    <xsl:call-template name="context-header">
      <xsl:with-param name="ruleset-current" select="$ruleset"/>
    </xsl:call-template>

    <script type="text/javascript">
      var idArray = <xsl:call-template name="get-testids"/>;
    </script>

    <xsl:apply-templates select="$testdoc//section[@id=$section]">
      <xsl:with-param name="site" select="$site"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="section">
    <xsl:param name="site"/>

    <h2><xsl:apply-templates select="name"/></h2>

    <xsl:apply-templates select="category">
      <xsl:with-param name="site" select="$site"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="category">
    <xsl:param name="site"/>

    <xsl:if test="descendant::page">
      <h3 id="{@id}">
        <xsl:apply-templates select="name"/>
        <xsl:apply-templates select="link[@tgt='bp']">
          <xsl:with-param name="name" select="name"/>
        </xsl:apply-templates>
      </h3>

      <ul>
        <xsl:apply-templates select="best-practice">
          <xsl:with-param name="site" select="$site"/>
        </xsl:apply-templates>
      </ul>
    </xsl:if>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="best-practice">
    <xsl:param name="page"/>

    <xsl:if test="child::page">
      <xsl:variable name="testid" select="concat(@ref, 'p')"/>
      <xsl:variable name="test-pages" select="$results/tests//test-pages[@id=$testid and not(preceding::test-pages[@id=$testid])]"/>

      <xsl:variable name="pass" select="count($test-pages/page-test[@eval='pass'])"/>
      <xsl:variable name="warn" select="count($test-pages/page-test[@eval='warn' or @eval='warn-null'])"/>
      <xsl:variable name="fail" select="count($test-pages/page-test[@eval='fail' or @eval='fail-null'])"/>
      <xsl:variable name="disc" select="count($test-pages/page-test[@eval='disc'])"/>

      <li>
        <xsl:call-template name="new-rule"/>
        <xsl:apply-templates select="rule"/>

        <xsl:choose>
          <xsl:when test="$test-pages">
            <ul class="results">
              <xsl:if test="$fail &gt; 0">
                <li class="fail"><a href="javascript:divMap['{@ref}'].show('fail')">Fail: <xsl:value-of select="$fail"/> page<xsl:if test="$fail &gt; 1">s</xsl:if></a></li>
              </xsl:if>
              <xsl:if test="$warn &gt; 0">
                <li class="warn"><a href="javascript:divMap['{@ref}'].show('warn')">Warn: <xsl:value-of select="$warn"/> page<xsl:if test="$warn &gt; 1">s</xsl:if></a></li>
              </xsl:if>
              <xsl:if test="$pass &gt; 0">
                <li class="pass"><a href="javascript:divMap['{@ref}'].show('pass')">Pass: <xsl:value-of select="$pass"/> page<xsl:if test="$pass &gt; 1">s</xsl:if></a></li>
              </xsl:if>
              <xsl:if test="$disc &gt; 0">
                <li class="disc"><a href="javascript:divMap['{@ref}'].show('disc')">N/A: <xsl:value-of select="$disc"/> page<xsl:if test="$disc &gt; 1">s</xsl:if></a></li>
              </xsl:if>
              <li><a id="{@ref}a" class="hideList" href="javascript:divMap['{@ref}'].hide()">Hide list</a></li>
            </ul>
            <div id="{@ref}" class="listContainer">
              <xsl:comment><xsl:value-of select="@ref"/> results go here</xsl:comment>
            </div>
          </xsl:when>
          <xsl:otherwise>
            <div style="margin-bottom: 1em"><xsl:value-of select="$nodata"/></div>
          </xsl:otherwise>
        </xsl:choose>
      </li>
    </xsl:if>

  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template name="get-testids">
    <xsl:text>[</xsl:text><xsl:for-each select="$testdoc/section[@id=$section]//best-practice[child::page]"><xsl:if test="position() &gt; 1"><xsl:text>,</xsl:text></xsl:if><xsl:text>'</xsl:text><xsl:value-of select="@ref"/><xsl:text>'</xsl:text></xsl:for-each><xsl:text>]</xsl:text>
  </xsl:template>

</xsl:transform>
