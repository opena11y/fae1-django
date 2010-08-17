<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- Notes:
  1. top-level param: all-page-results

  By default, only the result elements with eval types "warn" and "fail"
  list all pages with those values. The other result eval types ("pass" and
  "disc") check the stylesheet parameter all-page-results, which is set to
  false() by default, to determine whether to list all pages with those
  values. To see all pages listed for all result eval types, call this
  stylesheet with param all-page-results set to a true value such as 1.

  2. page-info template and redundancy param

  The page-info template can be toggled to output empty page elements
  that only contain an @id cross reference to page elements in the pages
  container. By default the template param named redundancy is set to true(),
  which causes it to output page elements that contain the page name as well.
  To see only the empty page elements, call the template with the redundancy
  param set to false().
  -->

  <!-- output -->
  <xsl:output encoding="UTF-8" indent="yes" method="xml"/>

  <!-- stylesheet parameters -->
  <xsl:param name="all-page-results" select="false()"/>

  <!-- top-level variables -->
  <xsl:key name="url-lookup" match="/results/pages/page-info" use="@id"/>
  <xsl:variable name="pg-count" select="/results/meta/pg-count"/>

  <xsl:variable name="testdoc" select="document('../xml/testdoc.xml')/testdoc"/>
  <xsl:key name="rule-lookup" match="section/category/best-practice" use="@ref"/>

  <!-- ================================================================ -->
  <!-- root template -->
  <xsl:template match="/">
    <fae-evaluation>
      <xsl:copy-of select="results/meta"/>
      <pages>
        <xsl:for-each select="results/pages/page-info">
          <page id="{@id}"><xsl:apply-templates select="name"/></page>
        </xsl:for-each>
      </pages>
      <results>
        <xsl:for-each select="results/tests/section/category/test-pages">
          <!--xsl:sort select="@id"/-->
          <xsl:variable name="id" select="substring(@id, 1, string-length(@id) - 1)"/>
          <rule id="{$id}">
            <xsl:for-each select="$testdoc">
              <desc><xsl:value-of select="key('rule-lookup', $id)/rule"/></desc>
            </xsl:for-each>
            <result eval="pass" cnt="{count(page-test[@eval='pass'])}">
              <!-- conditionally list pass results -->
              <xsl:if test="$all-page-results">
                <xsl:for-each select="page-test[@eval='pass']">
                  <xsl:call-template name="page-info"/>
                </xsl:for-each>
              </xsl:if>
            </result>
            <result eval="warn" cnt="{count(page-test[@eval='warn' or @eval='warn-null'])}">
              <xsl:for-each select="page-test[@eval='warn' or @eval='warn-null']">
                <xsl:call-template name="page-info"/>
              </xsl:for-each>
            </result>
            <result eval="fail" cnt="{count(page-test[@eval='fail' or @eval='fail-null'])}">
              <xsl:for-each select="page-test[@eval='fail' or @eval='fail-null']">
                <xsl:call-template name="page-info"/>
              </xsl:for-each>
            </result>
            <result eval="disc" cnt="{count(page-test[@eval='disc'])}">
              <!-- conditionally list disc results -->
              <xsl:if test="$all-page-results">
                <xsl:for-each select="page-test[@eval='disc']">
                  <xsl:call-template name="page-info"/>
                </xsl:for-each>
              </xsl:if>
            </result>
          </rule>
        </xsl:for-each>
      </results>
    </fae-evaluation>
  </xsl:template>

  <!-- ================================================================ -->
  <xsl:template name="page-info">
    <xsl:param name="redundancy" select="true()"/>

    <xsl:choose>
      <xsl:when test="$redundancy">
        <page id="{@id}"><xsl:value-of select="key('url-lookup', @id)/name"/></page>
      </xsl:when>
      <xsl:otherwise>
        <page id="{@id}"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:transform>
