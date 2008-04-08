<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- ======================================================== -->

  <xsl:template match="and|or">
    <xsl:param name="curr-test"/>

    <xsl:variable name="p1">
      <xsl:apply-templates select="*[1]">
        <xsl:with-param name="curr-test" select="$curr-test"/>
      </xsl:apply-templates>
    </xsl:variable>

    <xsl:variable name="p2">
      <xsl:apply-templates select="*[2]">
        <xsl:with-param name="curr-test" select="$curr-test"/>
      </xsl:apply-templates>
    </xsl:variable>

    <xsl:choose>
      <xsl:when test="self::node()[name()='and']">
        <xsl:value-of select="$p1='true' and $p2='true'"/>
      </xsl:when>
      <xsl:when test="self::node()[name()='or']">
        <xsl:value-of select="$p1='true' or $p2='true'"/>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="cmp">
    <xsl:param name="curr-test"/>
    <xsl:variable name="id" select="@ref"/>

    <xsl:choose>
      <xsl:when test="not($curr-test/r[@id=$id])">***Error: <xsl:value-of select="$id"/>
      result not found in test <xsl:value-of select="$curr-test/@id"/>!
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="compare">
          <xsl:with-param name="ref" select="$curr-test/r[@id=$id]"/>
          <xsl:with-param name="val" select="@val"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template name="compare">
    <xsl:param name="ref"/>
    <xsl:param name="val"/>

    <xsl:choose>
      <xsl:when test="@op='eq'"><xsl:value-of select="$ref = $val"/></xsl:when>
      <xsl:when test="@op='ne'"><xsl:value-of select="$ref != $val"/></xsl:when>

      <xsl:when test="@op='lt'"><xsl:value-of select="$ref &lt; $val"/></xsl:when>
      <xsl:when test="@op='le'"><xsl:value-of select="$ref &lt;= $val"/></xsl:when>

      <xsl:when test="@op='gt'"><xsl:value-of select="$ref > $val"/></xsl:when>
      <xsl:when test="@op='ge'"><xsl:value-of select="$ref >= $val"/></xsl:when>
    </xsl:choose>
  </xsl:template>

</xsl:transform>
