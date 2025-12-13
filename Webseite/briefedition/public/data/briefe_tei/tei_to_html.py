from lxml import etree

for i in range(1, 26):
    xml = etree.parse(f"brief{i}_tei.xml")
    xsl = etree.parse("transform.xsl")

    transform = etree.XSLT(xsl)
    html = transform(xml)

    open(f"brief{i}.html","w",encoding="utf-8").write(str(html))