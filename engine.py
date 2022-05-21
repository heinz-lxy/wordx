from jinja2 import Environment, FileSystemLoader
from os import path

class Engine(object):
    """模板渲染引擎"""
    def __init__(self):
        PATH = path.dirname(path.abspath(__file__))
        self.env = Environment(
            autoescape=False,
            loader=FileSystemLoader('templates'),
            trim_blocks=False)

    def render_template(self, template_xml, **kwargs):
        """渲染模板"""
        return self.env.get_template(template_xml).render(**kwargs)

    def render(self, template_xml, data):
        """渲染模板"""
        return self.render_template(template_xml, data = data, isinstance=isinstance, tuple=tuple)

if __name__ == '__main__':
    from word_file import WordFile

    engine = Engine() 
    data = [{
        'type': 'table',
        'content': {
            'table_data': [[1,2,3]]
        }
    }]
    rst = engine.render('base/template.xml',data=data)
    grammer_map = {
        r'($': '{%',
        r'$)': '%}',
        r'((': '{{',
        r'))': '}}',
    }
    rst = rst.replace('($', '{%')
    rst = rst.replace('$)', '%}')
    rst = rst.replace('((', '{{')
    rst = rst.replace('))', '}}')
    wf = WordFile('templates/template.docx')
    wf.replace('word/document.xml',rst)
    wf.save('123.docx')
        # print()
    print('_____________')
    print(rst)