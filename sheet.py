from wordx.word_file import WordFile
from jinja2 import Template


def render_template(tpl, data):
    lib = {
        'enumerate': enumerate,
        'len': len,
        'isinstance': isinstance,
        'tuple': tuple
    }
    return Template(tpl).render(**data, **lib)


class Sheet(WordFile):
    """简易文档生成(配套使用标准模板文件)"""
    def __init__(self, tpl_path):
        super().__init__(tpl_path)

    def render_header(self, data):
        """页眉渲染"""
        header_xml = render_template(self.get_res_str('header.xml'), data)
        self.replace('word/header.xml', header_xml)

    def render_footer(self, data):
        """页脚渲染"""
        footer_xml = render_template(self.get_res_str('footer.xml'), data)
        self.replace('word/footer.xml', footer_xml)

    def render_document(self, data):
        """文档渲染"""
        document_xml = render_template(self.get_res_str('document.xml'), data)
        self.replace('word/document.xml', document_xml)

    def render(self, data):
        self.render_header(data)
        self.render_footer(data)
        self.render_document(data)
        return self
