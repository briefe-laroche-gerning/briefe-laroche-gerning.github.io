from lxml import etree

for i in range(1, 26):
    xml = etree.parse(f"brief{i}_tei.xml")
    xsl = etree.parse("transform_text.xsl")

    transform = etree.XSLT(xsl)
    html = transform(xml)

    open(f"brief{i}.html","w",encoding="utf-8").write(str(html))


for i in range(1, 26):
    xml = etree.parse(f"brief{i}_tei.xml")
    xsl = etree.parse("transform_tei_header.xsl")

    transform = etree.XSLT(xsl)
    json = transform(xml)

    open(f"brief{i}.json","w",encoding="utf-8").write(str(json))