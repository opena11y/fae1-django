<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:include href="compare.xsl"/>

  <!-- output -->
  <xsl:output
      encoding="UTF-8"
      indent="yes"
      omit-xml-declaration="no"
      method="xml"/>

  <xsl:strip-space elements="*"/>

  <xsl:variable name="criteria" select="document('../xml/criteria.xml')/criteria"/>

  <xsl:key name="eval-lookup" match="eval" use="@id"/>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">
    <results>
      <xsl:apply-templates select="results/meta"/>
      <xsl:apply-templates select="results/page">
        <xsl:sort select="url"/>
      </xsl:apply-templates>
      <site>
        <xsl:apply-templates select="results/site"/>
      </site>
      <pages>
        <xsl:for-each select="results/page">
          <xsl:sort select="url"/>
          <xsl:element name="page-info">
            <xsl:attribute name="id"><xsl:value-of select="position()"/></xsl:attribute>
            <xsl:element name="name">
              <xsl:value-of select="url"/>
            </xsl:element>
            <xsl:element name="title">
              <xsl:value-of select="title"/>
            </xsl:element>
          </xsl:element>
        </xsl:for-each>
      </pages>
    </results>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="meta">
    <meta>
      <xsl:copy-of select="*"/>
      <xsl:element name="pg-count">
        <xsl:value-of select="count(/results/page)"/>
      </xsl:element>
    </meta>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="page">
    <page id="{position()}">
      <xsl:apply-templates select="test"/>
      <xsl:copy-of select="timestamp"/>
    </page>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="test">
    <xsl:apply-templates select="$criteria">
      <xsl:with-param name="curr-test" select="."/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="criteria">
    <xsl:param name="curr-test"/>

    <xsl:variable name="eval" select="key('eval-lookup', $curr-test/@id)"/>

    <xsl:choose>
      <xsl:when test="not ($eval)">
        <xsl:comment>*** eval not found: <xsl:value-of select="$curr-test/@id"/> ***</xsl:comment>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="$eval">
          <xsl:with-param name="curr-test" select="$curr-test"/>
        </xsl:apply-templates>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="eval">
    <xsl:param name="curr-test"/>

    <xsl:variable name="eval">

      <xsl:variable name="disc">
        <xsl:apply-templates select="disc">
          <xsl:with-param name="curr-test" select="$curr-test"/>
        </xsl:apply-templates>
      </xsl:variable>

      <xsl:choose>
        <xsl:when test="$disc='true'">disc</xsl:when>
        <xsl:otherwise>

          <xsl:variable name="null">
            <xsl:apply-templates select="null">
              <xsl:with-param name="curr-test" select="$curr-test"/>
            </xsl:apply-templates>
          </xsl:variable>

          <xsl:variable name="pass">
            <xsl:apply-templates select="pass">
              <xsl:with-param name="curr-test" select="$curr-test"/>
            </xsl:apply-templates>
          </xsl:variable>

          <xsl:variable name="warn">
            <xsl:apply-templates select="warn">
              <xsl:with-param name="curr-test" select="$curr-test"/>
            </xsl:apply-templates>
          </xsl:variable>

          <xsl:choose>
            <xsl:when test="$null='true'">null</xsl:when>
            <xsl:when test="$pass='true'">pass</xsl:when>
            <xsl:when test="$warn='true'">warn</xsl:when>
            <xsl:otherwise>fail</xsl:otherwise>
          </xsl:choose>

        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <test id="{@id}">
      <xsl:attribute name="eval"><xsl:value-of select="$eval"/></xsl:attribute>
      <xsl:copy-of select="$curr-test/*"/>
    </test>

  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="pass|warn|null|disc">
    <xsl:param name="curr-test"/>

    <xsl:apply-templates>
      <xsl:with-param name="curr-test" select="$curr-test"/>
    </xsl:apply-templates>
  </xsl:template>

</xsl:transform>
