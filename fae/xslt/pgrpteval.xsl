<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- output -->
  <xsl:output encoding="UTF-8" indent="yes" method="html"/>
  <xsl:strip-space elements="*"/>

  <!-- url parameters -->
  <xsl:param name="id"/>
  <xsl:param name="section"/>

  <!-- lookup parameters -->
  <xsl:param name="testid"/>
  <xsl:param name="eval"/>

  <xsl:variable name="class" select="concat('reports-', $eval)"/>
  <xsl:variable name="prefix">/report/<xsl:value-of select="$id"/>/page/</xsl:variable>

  <xsl:key name="page-info-lookup" match="/results/pages/page-info" use="@id"/>

  <!-- ======================================================== -->
  <xsl:template match="/">
    <h4><xsl:call-template name="get-title"/></h4>
    <ul class="{$class}">
      <xsl:choose>
        <xsl:when test="$eval='fail'">
          <xsl:for-each select="results/tests//test-pages[@id=$testid]/page-test[@eval='fail' or @eval='fail-null']">
            <xsl:call-template name="page-test"/>
          </xsl:for-each>
        </xsl:when>
        <xsl:when test="$eval='warn'">
          <xsl:for-each select="results/tests//test-pages[@id=$testid]/page-test[@eval='warn' or @eval='warn-null']">
            <xsl:call-template name="page-test"/>
          </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
          <xsl:for-each select="results/tests//test-pages[@id=$testid]/page-test[@eval=$eval]">
            <xsl:call-template name="page-test"/>
          </xsl:for-each>
        </xsl:otherwise>
      </xsl:choose>
    </ul>
  </xsl:template>

  <!-- ======================================================== -->
  <xsl:template name="page-test">
    <xsl:variable name="idx">
      <xsl:choose>
        <xsl:when test="position()=1">0</xsl:when>
        <xsl:otherwise>-1</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <li><a title="Page Report: {@id}" tabindex="{$idx}" href="{$prefix}{@id}/{$section}/"><span>(<xsl:value-of select="@id"/>)</span><xsl:text disable-output-escaping="yes">&amp;nbsp;</xsl:text><xsl:value-of select="key('page-info-lookup', @id)/name"/></a></li>
  </xsl:template>

  <!-- ======================================================== -->
  <xsl:template name="get-title">
    <xsl:variable name="prefix">
      <xsl:choose>
        <xsl:when test="$eval='pass'">Pass</xsl:when>
        <xsl:when test="$eval='warn'">Warn</xsl:when>
        <xsl:when test="$eval='fail'">Fail</xsl:when>
        <xsl:when test="$eval='disc'">N/A</xsl:when>
      </xsl:choose>
    </xsl:variable>
    <xsl:value-of select="concat($prefix, ': Page Reports')"/>
  </xsl:template>

</xsl:transform>
