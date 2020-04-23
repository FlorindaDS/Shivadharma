<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>

<!--<xsl:template match="*/text()[normalize-space()]">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>

<xsl:template match="*/text()[not(normalize-space())]" />
-->

<xsl:template match="/">
<body>
<link rel="stylesheet" href="style_wrap.css"/>
       <xsl:apply-templates/>
<br/><br/><br/><br/>
</body>
</xsl:template>




<xsl:template match="TEXT">
	<xsl:apply-templates />
</xsl:template>    

<xsl:template match="PTEXT">
<!-- <font size="3" color="black"> -->
 &#160;&#160;&#160;<ptext><xsl:apply-templates /></ptext>
<!--</font>-->
</xsl:template>    


<xsl:template match="mainwrap">
<div class="tooltip-wrap"> 
<!-- <font size="3" color="black"> -->
	<versewrap><p><xsl:apply-templates /></p></versewrap>
<!--</font>-->
</div>
</xsl:template>    


<xsl:template match="apparatuswrap">
<div class="tooltip-content"> 
<!-- <font size="3" color="black"> -->
	<p><xsl:apply-templates /></p>
<!--</font>-->
</div>
</xsl:template>    


<xsl:template match="APP">
 <app>      <p><xsl:apply-templates /></p></app>

</xsl:template>    



<xsl:template match="COLO">
  <xsl:copy>
<font size="3" color="blue"> 
	<xsl:apply-templates />
	<br/>
</font>
  </xsl:copy>
</xsl:template>  
  
<xsl:template match="node()|@*">
  <xsl:copy>
   <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
 </xsl:template>

<xsl:template match="link">
  <xsl:copy>
	--><xsl:apply-templates />
  </xsl:copy>
</xsl:template>    

    


<xsl:template match="TITLE">
<span style="font-weight:bold;">
<font size="6" color="black">
	<xsl:apply-templates />&#160;
	<br/>
</font>
</span>
</xsl:template>    

<xsl:template match="CHAPTER">
<!--<span style="font-weight:bold;">
<font size="4" color="black">-->
<h1>[<xsl:apply-templates/>]</h1>
<!--</font>
</span>-->
</xsl:template>    

<xsl:template match="SUBCHAPTER">
<!--<span style="font-weight:bold">
<font size="3" color="grey">-->
<h2>[<xsl:apply-templates/>]</h2>
<!--</font>
</span>-->
</xsl:template>    



<xsl:template match="PVAR">
       <pvar><p><xsl:apply-templates /></p></pvar>
</xsl:template>    


<xsl:template match="PARAL">
	 <paral><p><xsl:apply-templates /></p></paral>
</xsl:template>    


<xsl:template match="TR">
    <p><trs>"<xsl:apply-templates />"</trs></p>
</xsl:template>    

<xsl:template match="NOTE">
   <p><note>Note: <xsl:apply-templates /></note></p>
</xsl:template>    


<xsl:template match="SKT">
<!--<details open="yes">-->
	<i><xsl:apply-templates /></i>
</xsl:template>    


<xsl:template match="LEM">
<lem><xsl:apply-templates /></lem> 
] 
</xsl:template>    

<xsl:template match="ms">
<ms><xsl:apply-templates /></ms> 
</xsl:template>    

<xsl:template match="corr">
<corr><xsl:apply-templates /></corr> 
</xsl:template>    


<xsl:template match="vsnum">
<vsnum><xsl:apply-templates /></vsnum>
</xsl:template>    

<xsl:template match="NEWCHAPTER">
<br/><br/><br/><xsl:apply-templates />
</xsl:template>    

<xsl:template match="uvaca">
<xsl:apply-templates />
</xsl:template>    


</xsl:stylesheet>
