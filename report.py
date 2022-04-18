from word_file import WordFile
from template import Template 
import xml.etree.ElementTree as etree
# from lxml import etree
# from lxml.builder import E
from io import BytesIO


wf = WordFile('template.docx')
engine = Template() 
data = [
{
    'type': 'table',
    'content': {
    	'header':['姓名','年龄','职业'],
        'data': [[1,2,3]]
    }
}, 
{
	'type': 'paragraph',
	'content': '123'
}, 
{
	'type': 'paragraph',
	'content': '今天天气好晴朗'
}
]
rst = engine.render('base/template.xml',data=data)
print(rst)

wf.replace('word/document.xml',rst)
wf.save('123.docx')
# wf.show()


# doc = wf.get_document()
# tree = etree.parse(BytesIO(doc))
# # print(tree)
# print(etree.tostring(tree.getroot(), encoding='utf8', method='xml'))
# # body = tree.find('w:body')
# # print(body)

