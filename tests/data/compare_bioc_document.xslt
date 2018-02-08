<!-- This xslt compares bioc documents at the document level-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output omit-xml-declaration="yes"/>

    <xsl:variable name="training-file" select="'Official_submission.xml'"/>

    <xsl:variable name="ref-doc" select="document($training-file)"/>

<xsl:template match="node() | @*">

    <xsl:apply-templates select="@*|node()"/>
</xsl:template>

    <xsl:template match="collection">


        <tr>
            <td>Document count </td>
            <td> <xsl:value-of select="count($ref-doc//document)"/>
            </td>

            <td> <xsl:value-of select="count(//document)"/>
            </td>

        </tr>
        <tr>
            <td>Relation count </td>
            <td> <xsl:value-of select="count($ref-doc//relation)"/>
            </td>
            <td> <xsl:value-of select="count(//relation)"/>
            </td>
        </tr>

        <tr>
            <xsl:variable name="arg_collection" select="/collection"></xsl:variable>
            <td>Documents in ref  matching arg  </td>
            <td> <xsl:value-of select="count($ref-doc/collection/document[id/text() = $arg_collection/document/id/text()])"/>
            </td>
             <td>
                <xsl:for-each select="$ref-doc/collection/document">
                    <xsl:choose>
                        <xsl:when test="id/text()=$arg_collection/document/id/text()"></xsl:when>

                        <xsl:otherwise >
                           <xsl:value-of select= "id/text()"/> ;
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>

            </td>
        </tr>

        <tr>
            <xsl:variable name="arg_collection" select="/collection"></xsl:variable>
            <td>Documents in arg  matching ref  </td>
            <td> <xsl:value-of select="count($arg_collection/document[id/text() = $ref-doc/collection/document/id/text()])"/>
            </td>
            <td>
                <xsl:for-each select="$arg_collection/document">
                    <xsl:choose>
                        <xsl:when test="id/text()=$ref-doc/collection/document/id/text()"></xsl:when>

                        <xsl:otherwise >
                            id/text() ;
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>
            </td>
        </tr>

    </xsl:template>



</xsl:stylesheet>