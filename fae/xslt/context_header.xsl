<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- ======================================================== -->

  <xsl:template name="context-header">
    <xsl:param name="url"/>
    <xsl:param name="page-title"/>
    <xsl:param name="link" select="false()"/>
    <xsl:param name="display-urls" select="true()"/>

    <xsl:variable name="title" select="/results/meta/title"/>
    <xsl:variable name="default-report-title" select="'Untitled Report'"/>

    <xsl:variable name="depth">
      <xsl:choose>
        <xsl:when test="/results/meta/depth = 0">Top-level</xsl:when>
        <xsl:when test="/results/meta/depth = 1">2nd-level</xsl:when>
        <xsl:when test="/results/meta/depth = 2">3rd-level</xsl:when>
        <xsl:otherwise>Unspecified</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:variable name="span" select="number(/results/meta/span) = 1"/>

    <div id="context">
      <table cellpadding="0" cellspacing="0">
        <tr>
          <xsl:choose>
            <xsl:when test="$title='Unspecified' or $title='No Title' or string-length($title)=0">
              <td class="context-1">Report Title: <xsl:value-of select="$default-report-title"/></td>
            </xsl:when>
            <xsl:otherwise>
              <td class="context-1">Report Title: <strong><xsl:value-of select="$title"/></strong></td>
            </xsl:otherwise>
          </xsl:choose>
          <td class="context-2">Date: <xsl:value-of select="/results/meta/date"/></td>
        </tr>

        <xsl:if test="number(/results/meta/pg-count) &gt; 1">
          <tr>
            <td class="context-1">Pages: <xsl:value-of select="/results/meta/pg-count"/>
            <xsl:if test="$span"><span class="context">Span: Next-level subdomains</span></xsl:if></td>
            <td class="context-2">Depth: <xsl:value-of select="$depth"/></td>
          </tr>
        </xsl:if>

        <xsl:if test="$display-urls">
          <tr>
            <td colspan="2">
              <xsl:choose>
                <xsl:when test="string-length($url)">
                  URL:<xsl:text> </xsl:text>
                  <xsl:call-template name="format-url">
                    <xsl:with-param name="url" select="$url"/>
                    <xsl:with-param name="link" select="$link"/>
                  </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:choose>
                    <xsl:when test="count(/results/meta/urls/url) &gt; 1">
                      <xsl:call-template name="get-urls"/>
                    </xsl:when>
                    <xsl:otherwise>
                      URL:<xsl:text> </xsl:text>
                      <xsl:call-template name="format-url">
                        <xsl:with-param name="url" select="/results/meta/urls/url[1]"/>
                        <xsl:with-param name="link" select="$link"/>
                      </xsl:call-template>
                    </xsl:otherwise>
                  </xsl:choose>
                </xsl:otherwise>
              </xsl:choose>
            </td>
          </tr>
        </xsl:if>

        <xsl:if test="string-length($page-title)">
          <tr>
            <td colspan="2">Page Title: <xsl:value-of select="$page-title"/></td>
          </tr>
        </xsl:if>
      </table>
    </div>
  </xsl:template>

  <!-- ======================================================== -->

  <!-- get-urls -->
  <xsl:template name="get-urls">
    <xsl:variable name="max-urls" select="5"/>
    <xsl:variable name="count" select="count(/results/meta/urls/url)"/>
    <xsl:variable name="href">/report/<xsl:value-of select="$id"/>/urls/</xsl:variable>

    URLs:
    <xsl:choose>
      <xsl:when test="$count &gt; $max-urls">
        <ul class="urls">
          <xsl:for-each select="/results/meta/urls/url[position() &lt;= $max-urls]">
            <li>
              <xsl:call-template name="format-url">
                <xsl:with-param name="url" select="."/>
              </xsl:call-template>
            </li>
          </xsl:for-each>
        </ul>
        Note: First <xsl:value-of select="$max-urls"/> of <xsl:value-of select="$count"/> URLs displayed. <a href="{$href}">View All URLs</a>
      </xsl:when>
      <xsl:otherwise>
        <ul class="urls">
          <xsl:call-template name="all-urls"/>
        </ul>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->

  <!-- all-urls -->
  <xsl:template name="all-urls">
    <xsl:for-each select="/results/meta/urls/url">
      <li>
        <xsl:call-template name="format-url">
          <xsl:with-param name="url" select="."/>
        </xsl:call-template>
      </li>
    </xsl:for-each>
  </xsl:template>

  <!-- ======================================================== -->

  <!-- format-url -->
  <xsl:template name="format-url">
    <xsl:param name="url"/>
    <xsl:param name="link" select="false()"/>

    <xsl:variable name="prefix">
      <xsl:choose>
        <xsl:when test="starts-with($url, 'http')"/>
        <xsl:otherwise>//</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:choose>
      <xsl:when test="$link">
        <a class="external">
          <xsl:attribute name="href">
            <xsl:value-of select="concat($prefix, $url)"/>
          </xsl:attribute>
          <xsl:call-template name="add-line-breaks">
            <xsl:with-param name="str" select="$url"/>
          </xsl:call-template>
          <span> (external link)</span>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="add-line-breaks">
          <xsl:with-param name="str" select="$url"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->

  <!-- add-line-breaks -->
  <xsl:template name="add-line-breaks">
    <xsl:param name="str"/>
    <xsl:param name="max-length" select="72"/>

    <xsl:choose>
      <xsl:when test="string-length($str) &gt; $max-length">
        <xsl:value-of select="substring($str, 1, $max-length)"/><br/>
        <xsl:call-template name="add-line-breaks">
          <xsl:with-param name="str"><xsl:value-of select="substring($str, $max-length + 1)"/></xsl:with-param>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="$str"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="link">
    <xsl:param name="name"/>
    <xsl:variable name="prefix" select="//link-base[@tgt='bp']/@href"/>
    <a class="external best-practices" href="{concat($prefix, @href)}" title="Best Practices: {$name}">Best Practices<span> (opens in a new window)</span></a>
  </xsl:template>

</xsl:transform>
