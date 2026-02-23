<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- ===== Rekursives Template zum Escapen von " ===== -->
  <xsl:template name="escape-quotes">
    <xsl:param name="text"/>
    <xsl:choose>
      <xsl:when test="contains($text, '&quot;')">
        <xsl:value-of select="substring-before($text, '&quot;')"/>
        <xsl:text>\&quot;</xsl:text>
        <xsl:call-template name="escape-quotes">
          <xsl:with-param name="text" select="substring-after($text, '&quot;')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ===== Haupttemplate ===== -->
  <xsl:template match="/tei:TEI">
{
  "title": "<xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title)"/>",
  "date": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:correspAction[@type='sent']/tei:date)"/>",

  "sender": {
    "name": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:correspAction[@type='sent']/tei:persName)"/>",
    "gnd": "<xsl:value-of select="tei:teiHeader//tei:correspAction[@type='sent']/tei:persName/@ref"/>",
    "place": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:correspAction[@type='sent']/tei:placeName)"/>",
    "placeGnd": "<xsl:value-of select="tei:teiHeader//tei:correspAction[@type='sent']/tei:placeName/@ref"/>"
  },

  "recipient": {
    "name": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:correspAction[@type='received']/tei:persName)"/>",
    "gnd": "<xsl:value-of select="tei:teiHeader//tei:correspAction[@type='received']/tei:persName/@ref"/>",
    "place": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:correspAction[@type='received']/tei:placeName)"/>",
    "placeGnd": "<xsl:value-of select="tei:teiHeader//tei:correspAction[@type='received']/tei:placeName/@ref"/>"
  },

  "identifier": {
    "institution": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:msIdentifier/tei:institution)"/>",
    "signature": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:idno[@type='signatur'])"/>"
  },

  "object": {
    "type": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:objectDesc/tei:ab[@type='type'])"/>",
    "subtype": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:objectDesc/tei:ab[@type='subtype'])"/>",
    "note": "<xsl:value-of select="normalize-space(tei:teiHeader//tei:objectDesc/tei:ab[@type='note'])"/>"
  },

  "keywords": [
    <xsl:for-each select="tei:teiHeader//tei:textClass/tei:keywords/tei:term">
      {
        "label": "<xsl:value-of select="normalize-space(.)"/>"
      }<xsl:if test="position() != last()">,</xsl:if>
    </xsl:for-each>
  ]
}
  </xsl:template>

</xsl:stylesheet>
