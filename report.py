from word_file import WordFile
from engine import Engine
import xml.etree.ElementTree as etree
from io import BytesIO


wf = WordFile('template.docx')
engine = Engine() 
data = [
{
    'type': 'table',
    'content': {
    	'header':['姓名','年龄','职业'],
        'data': [[1,2,3]]
    }
}, 
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

