<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output omit-xml-declaration="yes"/>

    <xsl:variable name="relation-file" select="'PMtask_Relations_TrainingSet_noannotation_Gnormplus_out.xml'"/>

    <xsl:variable name="relation-doc" select="document($relation-file)"/>
    <xsl:variable name="triagRelavantDocs"
                  select="//document[infon[@key='relevant']/text()='yes']"></xsl:variable>
    <xsl:variable name="triagIrrelavantDocs"
                  select="//document[infon[@key='relevant']/text()='no']"></xsl:variable>




    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates  select="node()|@*" />
        </xsl:copy>
    </xsl:template>




    <xsl:template match="passage">
        <passage>

            <xsl:apply-templates select="node()|@*"></xsl:apply-templates>
            <xsl:variable name="docid" select="../id/text()" ></xsl:variable>
            <xsl:variable name="offset" select="offset/text()" ></xsl:variable>


            <!--../id/text()-->

            <xsl:variable  name="newannotations" select="$relation-doc/collection/document[id/text() = $docid ]/passage[offset/text() = $offset]/annotation"></xsl:variable>

            <xsl:for-each select="$newannotations">
                <annotation>
                    <xsl:attribute name="id">
                        <xsl:value-of select="concat('gnorm', @id)"/>
                    </xsl:attribute>
                    <xsl:apply-templates select="node()"></xsl:apply-templates>

                </annotation>
            </xsl:for-each>

        </passage>
        <!--<xsl:copy-of select="$relation-doc/collection/document[id/text()=../id/text()]/passage[offset/text()=./offset/text()]/annotation"></xsl:copy-of>-->
    </xsl:template>

    <xsl:template match="annotation"></xsl:template>


    <!--<xsl:template match="annotation[infon[@key='type']/text()='Gene']">-->

    <!--<xsl:variable name="geneName" select="text/text()"/>-->
    <!--<xsl:variable name="docId" select="../../id"/>-->
    <!--<xsl:value-of select="'*********'"/>-->
    <!--&lt;!&ndash;<xsl:value-of select="$docId"/>&ndash;&gt;-->
    <!--&lt;!&ndash;<xsl:value-of select="$geneName"/>&ndash;&gt;-->
    <!--<br/>-->
    <!--<xsl:value-of select="$training-doc//document[id=$docId]//annotation[infon[@key='type']/text()='Gene'][text/text()=$geneName]/text/text()"/>-->
    <!--&lt;!&ndash;<xsl:value-of select="$training-doc//document[id=$docId]//annotation[infon[infon[@key='type']/text()='Gene']/text/text()=$geneName]"/>&ndash;&gt;-->


    <!--</xsl:template>-->

</xsl:stylesheet>