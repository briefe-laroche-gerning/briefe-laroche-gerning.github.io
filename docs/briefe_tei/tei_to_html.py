from lxml import etree

xml = etree.parse("brief1_tei.xml")
xsl = etree.parse("transform.xsl")

transform = etree.XSLT(xsl)
html = transform(xml)

open("brief1.html","w",encoding="utf-8").write(str(html))