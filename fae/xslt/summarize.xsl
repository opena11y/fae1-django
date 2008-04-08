<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- output -->
  <xsl:output
      encoding="UTF-8"
      indent="yes"
      omit-xml-declaration="no"
      method="xml"/>

  <xsl:strip-space elements="*"/>

  <xsl:variable name="results" select="/"/>
  <xsl:variable name="testdoc" select="document('../xml/testdoc.xml')/testdoc"/>

  <xsl:key name="test-lookup" match="page/test" use="@id"/>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">
    <results>
      <xsl:copy-of select="results/*"/>

      <tests>
        <xsl:for-each select="$testdoc/section">
          <section id="{@id}">
            <xsl:apply-templates select="category"/>
          </section>
        </xsl:for-each>
      </tests>
    </results>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="category">
    <category id="{@id}">
      <xsl:for-each select="best-practice/page">
        <xsl:variable name="testid" select="@id"/>
        <test-pages id="{$testid}">
          <!--
              The key function only works within the document associated with
              the context node. To switch the context from testdoc to results,
              use xsl:for-each on the $results document element.
          -->
          <xsl:for-each select="$results/results">
            <xsl:for-each select="key('test-lookup', $testid)">
              <xsl:variable name="pageid" select="parent::page/@id"/>
              <page-test id="{$pageid}" eval="{@eval}"/>
            </xsl:for-each>
          </xsl:for-each>
        </test-pages>
      </xsl:for-each>
    </category>
  </xsl:template>

</xsl:transform>
