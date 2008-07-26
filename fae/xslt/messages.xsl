<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:preserve-space elements="msg"/>

  <xsl:variable name="messages" select="document('../xml/messages.xml')/messages"/>
  <xsl:key name="msg-lookup" match="message" use="@id"/>

  <xsl:variable name="debug" select="false()"/>

  <!-- ======================================================== -->

  <xsl:template match="messages">
    <xsl:param name="curr-test"/>

    <xsl:apply-templates select="key('msg-lookup', $curr-test/@id)">
      <xsl:with-param name="curr-test" select="$curr-test"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="message">
    <xsl:param name="curr-test"/>

    <xsl:variable name="eval" select="$curr-test/@eval"/>

    <li class="{$eval}">
      <xsl:call-template name="test-eval">
        <xsl:with-param name="eval" select="$eval"/>
      </xsl:call-template>

      <xsl:if test="$debug"><xsl:value-of select="@id"/>:<xsl:text> </xsl:text></xsl:if>
      <xsl:choose>
        <xsl:when test="$eval='disc'">
          <xsl:apply-templates select="msg[@id='disc']">
            <xsl:with-param name="curr-test" select="$curr-test"/>
          </xsl:apply-templates>
        </xsl:when>

        <xsl:otherwise><!-- $eval must have value of pass, warn, warn-null, fail or fail-null -->
          <xsl:choose>
            <xsl:when test="child::msg[@id=$eval]">
              <xsl:apply-templates select="msg[@id=$eval]">
                <xsl:with-param name="curr-test" select="$curr-test"/>
              </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="msg[@id='default']">
                <xsl:with-param name="curr-test" select="$curr-test"/>
              </xsl:apply-templates>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
    </li>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template name="test-eval">
    <xsl:param name="eval"/>

    <span class="eval">
      <xsl:choose>
        <xsl:when test="$eval='pass'">Pass</xsl:when>
        <xsl:when test="$eval='warn'">Warning</xsl:when>
        <xsl:when test="$eval='warn-null'">Warning</xsl:when>
        <xsl:when test="$eval='fail'">Fail</xsl:when>
        <xsl:when test="$eval='fail-null'">Fail</xsl:when>
        <xsl:when test="$eval='disc'">N/A</xsl:when>
      </xsl:choose>
    </span>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="msg">
    <xsl:param name="curr-test"/>

    <xsl:if test="string-length(.)">: </xsl:if>
    <xsl:apply-templates>
      <xsl:with-param name="curr-test" select="$curr-test"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- ======================================================== -->

  <xsl:template match="ins">
    <xsl:param name="curr-test"/>
    <xsl:variable name="ref" select="@ref"/>
    <xsl:variable name="val" select="$curr-test/r[@id=$ref]"/>

    <xsl:if test="not($curr-test/r[@id=$ref])">
      <span class="notFound"><xsl:value-of select="$ref"/> not found in <xsl:value-of select="$curr-test/@id"/>!</span>
    </xsl:if>
    <xsl:value-of select="$val"/>
    <xsl:if test="child::s and child::p">
      <xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$val=1"><xsl:apply-templates select="s"/></xsl:when>
        <xsl:otherwise><xsl:apply-templates select="p"/></xsl:otherwise>
      </xsl:choose>
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
