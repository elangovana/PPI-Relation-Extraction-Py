<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output omit-xml-declaration="yes"/>
    <xsl:variable name="newline" select="'&#xa;'"/>
    <xsl:variable name="tab" select="'&#x9;'"/>


    <xsl:template match="/">

        <xsl:for-each select="collection/document">
            <xsl:variable name="docID" select="id/text()"></xsl:variable>
            <xsl:variable name="titlePassage" select="passage[infon[@key='type']/text() ='title']"></xsl:variable>
            <xsl:variable name="abstractPassage" select="passage[infon[@key='type']/text() ='abstract']"></xsl:variable>

            <!--Get Title & abtract content -->
            <xsl:value-of
                    select="concat($docID, '|t|', $titlePassage/text/text(),$newline)"></xsl:value-of>
            <xsl:value-of
                    select="concat($docID, '|a|',  $abstractPassage/text/text(),$newline)"></xsl:value-of>


            <!--Loop thr  annotations-->
            <xsl:for-each select="passage">
                <xsl:for-each select="annotation">
                    <xsl:value-of
                            select="concat($docID, $tab,  location/@offset, $tab, location/@offset +location/@length, $tab,  text/text(), $tab, infon[@key='type']/text(), $tab,infon[( @key)='NCBI GENE']/text(),$newline )"></xsl:value-of>
                </xsl:for-each>
            </xsl:for-each>


            <xsl:value-of select="$newline"/>
        </xsl:for-each>
    </xsl:template>


</xsl:stylesheet>