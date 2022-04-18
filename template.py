from jinja2 import Environment, FileSystemLoader
from os import path

class Template(object):
    """模板系统"""
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
    engine = Template() 
    data = [{
        'type': 'table',
        'content': {
            'table_data': [[1,2,3]]
        }
    }]
    rst = engine.render('base/template.xml',data=data)
    print(rst)