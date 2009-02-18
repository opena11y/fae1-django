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
  <xsl:param name="pc"/>
  <xsl:param name="pid"/>
  <xsl:param name="title"/>

  <xsl:variable name="results" select="/"/>
  <xsl:variable name="testdoc" select="document('../xml/testdoc.xml')/testdoc"/>
  <xsl:variable name="link-prefix" select="$testdoc/link-base[@tgt='bp']/@href"/>

  <xsl:variable name="tblcap-summary">Evaluation Results by Best Practices Main Category</xsl:variable>
  <xsl:variable name="tblsum-summary">Aggregated rules evaluation results by HTML Best Practices main categories.</xsl:variable>

  <xsl:variable name="tblcap-detail">Evaluation Results by Best Practices Subcategory</xsl:variable>
  <xsl:variable name="tblsum-detail">Aggregated rules evaluation results by HTML Best Practices subcategories.</xsl:variable>

  <xsl:variable name="intro-legend">Status values are based on aggregated evaluation results of Pass, Warn or N/A, as defined in the following table.</xsl:variable>
  <xsl:variable name="tblsum-legend">Definitions of Status values, which are assigned to Best Practices main categories in the first Evaluation Results table above.</xsl:variable>

  <xsl:key name="section-lookup" match="tests/section" use="@id"/>
  <xsl:key name="category-lookup" match="tests/section/category" use="@id"/>

  <!-- ======================================================== -->
  <!-- root template -->

  <xsl:template match="/">

    <xsl:variable name="type">
      <xsl:choose>
        <xsl:when test="number($pc) &gt; 1">sitewide</xsl:when>
        <xsl:otherwise>page</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:variable name="pageid">
      <xsl:choose>
        <xsl:when test="string-length($pid)">
          <xsl:value-of select="$pid"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:choose>
            <xsl:when test="$type='page'">
              <xsl:value-of select="1"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="''"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <h1><xsl:value-of select="$title"/></h1>

    <xsl:call-template name="context-header"/>

    <table cellpadding="0" cellspacing="0" class="summary" summary="{$tblsum-summary}">
      <caption style="padding-top: 1em"><xsl:value-of select="$tblcap-summary"/></caption>
      <tr>
        <th id="t1c0" class="category">Category</th>
        <th id="t1c1" class="status">Status <sup><a href="#status">1</a></sup></th>
        <th id="t1c2" class="pass"><span class="pct">%</span> Pass</th>
        <th id="t1c3" class="warn"><span class="pct">%</span> Warn</th>
        <th id="t1c4" class="fail"><span class="pct">%</span> Fail</th>
      </tr>

      <xsl:for-each select="$testdoc/section">
        <xsl:variable name="skey" select="@id"/>
        <xsl:variable name="sid" select="concat('t1s', position())"/>
        <tr>
          <xsl:if test="position() mod 2 = 0">
            <xsl:attribute name="class">highlight</xsl:attribute>
          </xsl:if>
          <th id="{$sid}">
            <xsl:choose>
              <xsl:when test="$type='page'">
                <a href="/report/{$id}/{$type}/{$pageid}/{$skey}/"><xsl:apply-templates select="name"/></a>
              </xsl:when>
              <xsl:otherwise>
                <a href="/report/{$id}/{$type}/{$skey}/"><xsl:apply-templates select="name"/></a>
              </xsl:otherwise>
            </xsl:choose>
          </th>

          <xsl:for-each select="$results/results">
            <xsl:variable name="rsec" select="key('section-lookup', $skey)"/>
            <xsl:variable name="total" select="count($rsec//page-test[not(@eval='disc')])"/>

            <xsl:variable name="pass" select="count($rsec//page-test[@eval='pass'])"/>
            <xsl:variable name="warn" select="count($rsec//page-test[@eval='warn'])"/>
            <xsl:variable name="warn-null" select="count($rsec//page-test[@eval='warn-null'])"/>
            <xsl:variable name="fail" select="count($rsec//page-test[@eval='fail'])"/>
            <xsl:variable name="fail-null" select="count($rsec//page-test[@eval='fail-null'])"/>

            <td headers="{$sid} t1c1" class="status">
              <xsl:call-template name="get-status">
                <xsl:with-param name="pass" select="$pass"/>
                <xsl:with-param name="warn" select="$warn + $warn-null"/>
                <xsl:with-param name="total" select="$total"/>
              </xsl:call-template>
            </td>
            <td headers="{$sid} t1c2" class="pct">
              <xsl:call-template name="get-pct">
                <xsl:with-param name="count" select="$pass"/>
                <xsl:with-param name="total" select="$total"/>
              </xsl:call-template>
            </td>
            <td headers="{$sid} t1c3" class="pct">
              <xsl:call-template name="get-pct">
                <xsl:with-param name="count" select="$warn + $warn-null"/>
                <xsl:with-param name="total" select="$total"/>
              </xsl:call-template>
            </td>
            <td headers="{$sid} t1c4" class="pct">
              <xsl:call-template name="get-pct">
                <xsl:with-param name="count" select="$fail + $fail-null"/>
                <xsl:with-param name="total" select="$total"/>
              </xsl:call-template>
            </td>
          </xsl:for-each>
        </tr>
      </xsl:for-each>
    </table>

    <table cellpadding="0" cellspacing="0" class="summary" summary="{$tblsum-detail}">
      <caption style="padding-top: 1.5em"><xsl:value-of select="$tblcap-detail"/></caption>
      <tr>
        <th id="t2c0" class="category">Category/Subcategory</th>
        <th id="t2c1" class="pass"><span class="pct">%</span> Pass</th>
        <th id="t2c2" class="warn"><span class="pct">%</span> Warn</th>
        <th id="t2c3" class="fail"><span class="pct">%</span> Fail</th>
        <th id="t2c4" class="disc"><span class="pct">%</span><xsl:text> </xsl:text><abbr title="Not Applicable">N/A</abbr></th>
      </tr>

      <xsl:for-each select="$testdoc/section">
        <xsl:variable name="skey" select="@id"/>
        <xsl:variable name="sid" select="concat('t2s', position())"/>
        <tr>
          <th id="{$sid}" class="section" colspan="5"><xsl:apply-templates select="name"/></th>
        </tr>
        <xsl:for-each select="category">
          <xsl:variable name="ckey" select="@id"/>
          <xsl:variable name="cid" select="concat($sid, 'r', position())"/>
          <tr>
            <xsl:if test="position() mod 2 = 1">
              <xsl:attribute name="class">highlight</xsl:attribute>
            </xsl:if>
            <th id="{$cid}" class="row-header">
            <xsl:choose>
              <xsl:when test="$type='page'">
                <a href="/report/{$id}/{$type}/{$pageid}/{$skey}/#{$ckey}"><xsl:apply-templates select="name"/></a>
              </xsl:when>
              <xsl:otherwise>
                <a href="/report/{$id}/{$type}/{$skey}/#{$ckey}"><xsl:apply-templates select="name"/></a>
              </xsl:otherwise>
            </xsl:choose>
            </th>

            <xsl:for-each select="$results/results">
              <xsl:variable name="rcat" select="key('category-lookup', $ckey)"/>
              <xsl:variable name="total" select="count($rcat//page-test)"/>

              <xsl:variable name="pass" select="count($rcat//page-test[@eval='pass'])"/>
              <xsl:variable name="warn" select="count($rcat//page-test[@eval='warn'])"/>
              <xsl:variable name="warn-null" select="count($rcat//page-test[@eval='warn-null'])"/>
              <xsl:variable name="fail" select="count($rcat//page-test[@eval='fail'])"/>
              <xsl:variable name="fail-null" select="count($rcat//page-test[@eval='fail-null'])"/>
              <xsl:variable name="disc" select="count($rcat//page-test[@eval='disc'])"/>

              <td headers="{$sid} {$cid} t2c1" class="pct">
                <xsl:call-template name="get-pct">
                  <xsl:with-param name="count" select="$pass"/>
                  <xsl:with-param name="total" select="$total"/>
                </xsl:call-template>
              </td>
              <td headers="{$sid} {$cid} t2c2" class="pct">
                <xsl:call-template name="get-pct">
                  <xsl:with-param name="count" select="$warn + $warn-null"/>
                  <xsl:with-param name="total" select="$total"/>
                </xsl:call-template>
              </td>
              <td headers="{$sid} {$cid} t2c3" class="pct">
                <xsl:call-template name="get-pct">
                  <xsl:with-param name="count" select="$fail + $fail-null"/>
                  <xsl:with-param name="total" select="$total"/>
                </xsl:call-template>
              </td>
              <td headers="{$sid} {$cid} t2c4" class="pct">
                <xsl:call-template name="get-pct">
                  <xsl:with-param name="count" select="$disc"/>
                  <xsl:with-param name="total" select="$total"/>
                </xsl:call-template>
              </td>
            </xsl:for-each>
          </tr>
        </xsl:for-each>
      </xsl:for-each>
    </table>

    <div id="legend">
      <br/>
      <a name="status"/>
      <xsl:call-template name="display-legend"/>
    </div>

  </xsl:template>

  <!-- ======================================================== -->
  <xsl:template name="display-legend">
    <p><sup>1</sup> <strong>Status Value Definitions</strong></p>

    <div style="margin-top: -1em; margin-bottom: 1em;"><xsl:value-of select="$intro-legend"/></div>

    <table class="legend" cellpadding="0" cellspacing="0" summary="{$tblsum-legend}">
      <thead>
        <tr class="highlight">
          <th>Value</th><th class="pct">Percent</th><th class="eval">Result</th>
        </tr>
      </thead>
      <tr>
        <td class="stat-1">Complete</td><td class="pct">100</td><td class="eval">Pass</td>
      </tr>
      <tr class="highlight">
        <td class="stat-2">Almost Complete</td><td class="pct">95&#8211;100</td><td class="eval">Pass + Warn</td>
      </tr>
      <tr>
        <td class="stat-3">Partially Implemented</td><td class="pct">40&#8211;94</td><td class="eval">Pass + Warn</td>
      </tr>
      <tr class="highlight">
        <td class="stat-4">Not Implemented</td><td class="pct">0&#8211;39</td><td class="eval">Pass + Warn</td>
      </tr>
      <tr>
        <td class="stat-0">Not Applicable</td><td class="pct">100</td><td class="eval">N/A</td>
      </tr>
    </table>
  </xsl:template>

  <!-- ======================================================== -->
  <xsl:template name="get-pct">
    <xsl:param name="count"/>
    <xsl:param name="total"/>

    <xsl:choose>
      <xsl:when test="$count=0 or $total=0">0</xsl:when>
      <xsl:otherwise>
        <xsl:choose>
          <xsl:when test="$count=$total">100</xsl:when>
          <xsl:otherwise>
            <xsl:variable name="pct" select="floor(100 * $count div $total)"/>
            <xsl:choose>
              <xsl:when test="$pct=0">1</xsl:when>
              <xsl:otherwise><xsl:value-of select="$pct"/></xsl:otherwise>
            </xsl:choose>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->
  <xsl:template name="get-status">
    <xsl:param name="pass"/>
    <xsl:param name="warn"/>
    <xsl:param name="total"/>

    <span>
    <xsl:choose>
      <xsl:when test="$total=0"><xsl:attribute name="class">stat-0</xsl:attribute>Not Applicable</xsl:when>
      <xsl:otherwise>
        <xsl:variable name="pct" select="round(($pass + $warn) div $total * 100)"/>
        <xsl:choose>
          <xsl:when test="$pass = $total"><xsl:attribute name="class">stat-1</xsl:attribute>Complete</xsl:when>
          <xsl:when test="$pct &gt;= 95"><xsl:attribute name="class">stat-2</xsl:attribute>Almost Complete</xsl:when>
          <xsl:when test="$pct &lt; 95 and $pct &gt;= 40"><xsl:attribute name="class">stat-3</xsl:attribute>Partially Implemented</xsl:when>
          <xsl:when test="$pct &lt; 40"><xsl:attribute name="class">stat-4</xsl:attribute>Not Implemented</xsl:when>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
    </span>
  </xsl:template>

</xsl:transform>
