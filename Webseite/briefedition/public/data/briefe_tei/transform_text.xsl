<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  version="1.0">
  
  <!-- output: html -->
  <xsl:output method="html" />
  
  <!-- Basis: nur Elemente innerhalb von <body> verarbeiten-->
  <xsl:template match="/">
    <div class="tei-document">
      <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
    </div>
  </xsl:template>
  
  
  <!-- einfacher Text -->
  <xsl:template match="text()">
    <xsl:value-of select="."/>
  </xsl:template>
  
  
  <!-- Abschnitte / Paragraphen -->
  <xsl:template match="tei:body">
    <div class="tei-body">
      <xsl:apply-templates/>
    </div>
  </xsl:template>
  
  <xsl:template match="tei:div">
    <div>
      <xsl:attribute name="class">
        <xsl:choose>
          <!-- äußerste div (keine tei:div-Vorfahren) -->
          <xsl:when test="not(ancestor::tei:div)">
            tei-div
          </xsl:when>
          <!-- alle inneren -->
          <xsl:otherwise>
            page
          </xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>

      <xsl:apply-templates/>
    </div>
  </xsl:template>
  
  <!-- Zeilenumbrüche -->
  <xsl:template match="tei:lb">
    <br/>
  </xsl:template>
  
  
  <!-- Hervorhebungen mit <hi>-->
  
  <!-- underline / double underline -->
  <xsl:template match="tei:hi[@rend='underline']">
    <span>
      <xsl:attribute name="class">
        <xsl:choose>
          <xsl:when test="@n='1'">underline</xsl:when>
          <xsl:when test="@n='2'">double-underline</xsl:when>
          <xsl:otherwise>underline</xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>
      <xsl:apply-templates/>
    </span>
  </xsl:template>
  
  <!-- latintype -->
  <xsl:template match="tei:hi[@rend='latintype']">
    <span class="latintype">
      <xsl:apply-templates/>
    </span>
  </xsl:template>
  
  <!-- sup -->
  <xsl:template match="tei:hi[@rend='sup']">
    <sup>
      <xsl:apply-templates/>
    </sup>
  </xsl:template>
  
  <!-- unclear (nicht entzifferte Stellen) -->
  <xsl:template match="tei:unclear">
    <span class="unclear">
      <xsl:apply-templates/>
    </span>
  </xsl:template>
  
  <!-- Annotation des Empfängers -->
  <xsl:template match="tei:note[@type='annotation']">
    <span class="recipient-note">
      <xsl:apply-templates/>
    </span>
  </xsl:template>
  
  <!-- Verse -->

  <!-- Strophe (lg) -->
  <xsl:template match="lg">
    <div class="stanza">
      <xsl:apply-templates/>
    </div>
  </xsl:template>
  
  <!-- Einzelne Verszeile (l) -->
  <xsl:template match="l">
    <div class="line">
      <xsl:apply-templates/>
    </div>
  </xsl:template>


  <!-- Registereinträge: Personen / Orte / Werke -->
  
  <!-- Person -->
  <!-- Hilfstemplate (Werte von key und ref zu array umwandeln) -->
  
  <xsl:template name="json-array">
    <xsl:param name="list"/> <!-- z.B. "person1 person2" -->
    <xsl:param name="first" select="'true'"/> <!-- Flag, ob erstes Element -->
    
    <xsl:choose>
      
      <!-- Fall 1: Liste enthält noch weitere Werte -->
      <xsl:when test="contains($list, ' ')">
        <xsl:variable name="head" select="substring-before($list, ' ')"/>
        <xsl:variable name="tail" select="substring-after($list, ' ')"/>
        
        <!-- Komma nur, wenn nicht erstes Element -->
        <xsl:if test="$first != 'true'">
          <xsl:text>,</xsl:text>
        </xsl:if>
        
        <xsl:text>"</xsl:text><xsl:value-of select="$head"/><xsl:text>"</xsl:text>
        
        <!-- rekursiver Aufruf -->
        <xsl:call-template name="json-array">
          <xsl:with-param name="list" select="$tail"/>
          <xsl:with-param name="first" select="'false'"/>
        </xsl:call-template>
      </xsl:when>
      
      <!-- Fall 2: letztes Element -->
      <xsl:otherwise>
        <xsl:if test="$first != 'true'">
          <xsl:text>,</xsl:text>
        </xsl:if>
        <xsl:text>"</xsl:text><xsl:value-of select="$list"/><xsl:text>"</xsl:text>
      </xsl:otherwise>
      
    </xsl:choose>
  </xsl:template>
  
  <!-- persName -->
  
  <xsl:template match="tei:persName">
    <span>
      
      <!-- class-Attribut zusammenbauen -->
      <xsl:attribute name="class">
        <xsl:text>entity person</xsl:text>
        
        <!-- Unsicherheitsgrad als CSS-Klasse -->
        <xsl:if test="@cert">
          <xsl:text> cert-</xsl:text>
          <xsl:value-of select="@cert"/>
        </xsl:if>
      </xsl:attribute>
      
      <!-- JSON-Array mit Personen-IDs -->
      <xsl:attribute name="data-keys">
        <xsl:text>[</xsl:text>
        
        <!-- Wenn ref vorhanden ist → Tokenize -->
        <xsl:choose>
          <xsl:when test="@ref">
            <xsl:call-template name="json-array">
              <xsl:with-param name="list" select="@ref"/>
            </xsl:call-template>
          </xsl:when>
          
          <!-- Wenn key vorhanden ist → Einzelelement -->
          <xsl:when test="@key">
            <xsl:text>"</xsl:text>
            <xsl:value-of select="@key"/>
            <xsl:text>"</xsl:text>
          </xsl:when>
          
          <!-- Falls weder noch → leeres Array -->
          <xsl:otherwise/>
        </xsl:choose>
        
        <xsl:text>]</xsl:text>
      </xsl:attribute>
      
      <!-- Inhalt (Name im Text) -->
      <xsl:apply-templates/>
      
    </span>
  </xsl:template>

  <!-- Ort -->
  <xsl:template match="tei:placeName">
    <span class="entity place" data-key="{@key}">
      <xsl:apply-templates/>
    </span>
  </xsl:template>
  
  <!-- Werk -->
  <xsl:template match="tei:name[@type='work']">
  <span>
    
    <!-- class -->
    <xsl:attribute name="class">
      <xsl:text>entity work</xsl:text>
    </xsl:attribute>

    <!-- JSON-Array mit Werk-IDs -->
    <xsl:attribute name="data-keys">
      <xsl:text>[</xsl:text>

      <xsl:choose>
        
        <!-- Mehrfach-Referenz über @ref -->
        <xsl:when test="@ref">
          <xsl:call-template name="json-array">
            <xsl:with-param name="list" select="@ref"/>
          </xsl:call-template>
        </xsl:when>
        
        <!-- Einzelwert über @key -->
        <xsl:when test="@key">
          <xsl:text>"</xsl:text>
          <xsl:value-of select="@key"/>
          <xsl:text>"</xsl:text>
        </xsl:when>
        
        <!-- weder noch → leeres Array -->
        <xsl:otherwise/>
        
      </xsl:choose>

      <xsl:text>]</xsl:text>
    </xsl:attribute>

    <!-- Textinhalt -->
    <xsl:apply-templates/>

  </span>
  </xsl:template>
  
  
  <!-- Fallback für sonstige Elemente -->
  <xsl:template match="tei:*">
    <div class="{local-name()}">
      <xsl:apply-templates/>
    </div>
  </xsl:template>
  
</xsl:stylesheet>
