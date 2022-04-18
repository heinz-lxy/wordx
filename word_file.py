import sys
from wordx.fake_zip import FakeZip
from lxml import etree
from lxml.builder import E
from io import BytesIO
import random
# from os import startfile


class WordFile(FakeZip):
	"""word文件管理"""
	def __init__(self, file_path):
		"""初始化
		wf = WordFile('template/template.docx')
		"""
		super().__init__(file_path)

	def show(self):
	    """ 打开word"""
	    # startfile(self.file_path)

	def get_document(self):
		"""获取document文件
		wf.get_document()
		"""
		return self.get('word/document.xml')

	def get_res_list(self):
		"""获取资源文件列表
		wf.get_res_list()
		"""
		tmp = []
		for filename, content in self.dict.items():
			if filename == 'word/document.xml':
				continue
			elif filename.startswith('word') and filename.endswith('xml'):
				tmp.append(filename)
			elif filename.startswith('word/media'):
				tmp.append(filename)
		return tmp

	def get_res(self, res):
		"""获取资源文件"""
		return self.get('word/%s' % res)

	def get_res_str(self, res):
		"""获取资源文件字符串"""
		return self.get_res(res).decode()

	def save_res_str(self, res, path):
		"""获取资源文件字符串"""
		data = self.get_res(res)
		with open(path, 'wb') as f:
			f.write(data)

	def get_rels(self, res):
		"""获取资源映射
		wf.get_rels('header1.xml')
		"""
		return self.get('word/_rels/%s.rels' % res) 

	def get_doc_rels(self):
		"""获取document资源映射
		wf.get_doc_rels()
		"""
		return self.get_rels('document.xml')

	def add_rels(self, res_name, rels):
		"""添加资源映射
		rels = [{
			'id': '1',
			'type': 'image',
			'target': 'media/haha.jpg'
		}]
		"""
		rels_path = 'word/_rels/%s.rels' % res_name
		res_rels = self.get_rels(res_name)
		
		if res_rels:  # append
			tree = etree.fromstring(res_rels)
			for rel in rels:
				ele = E.Relationship(Id=rel['id'],Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/%s'%rel['type'], Target=rel['target'])
				tree.append(ele)
			self.replace(rels_path, etree.tostring(tree))
		else:
			res_rels = self.make_rels(rels)
			self.add(rels_path, res_rels)
		return self

	def add_doc_rels(self, rels):
		"""添加document.xml映射
		"""
		return self.add_rels('document.xml', rels)

	def add_footer(self, footer_data, footer_rels=None):
		"""添加footer
		data = {
	
		}
		"""
		# 添加footer资源文件
		footer_file = '%s.xml' % random.randint(1000,9999)
		footer_path = 'word/%s' % footer_file
		self.add(footer_path, footer_data)
		# 注册footer资源文件
		self.reg_res([{'path': '/'+footer_path,'type': 'footer'}])
		# 添加footer映射
		if footer_rels:
			self.add_rels(footer_file, footer_rels)
		return footer_file

	def add_header(self, header_data, header_rels=None):
		"""添加header
		data = {
	
		}
		"""
		# 添加header资源文件
		header_file = '%s.xml' % random.randint(1000,9999)
		header_path = 'word/%s' % header_file
		self.add(header_path, header_data)
		# 注册header资源文件
		self.reg_res([{'path': '/'+header_path,'type': 'header'}])
		# 添加header映射
		if header_rels:
			self.add_rels(header_file, header_rels)
		return header_file	

	def make_rels(self, data):
		"""生成资源映射
		data  = [
			{
				'Id': '1',
				'Type': 'image',
				'Target': 'media/1.jpeg'
			}
		]
		"""
		template = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
		<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>"""
		tree = etree.fromstring(template)
		for item in data:
			ele =  E.Relationship(Id=item['id'], Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/%s'%item['type'], Target=item['target'])
			tree.append(ele)
		return etree.tostring(tree)

	def reg_res(self, res_list):
		"""注册资源文件
		res_list = [
			{
				'path': '/word/header1.xml',
				'type': 'header'

			}
		]
		wf.reg_res(res_list)
		"""
		types = self.get('[Content_Types].xml')
		types_tree = etree.fromstring(types)
		for res in res_list:
			path = res['path']
			content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml' % res['type'] 
			type_ele = E.Override(PartName = path, ContentType = content_type)
			types_tree.append(type_ele)
		types = etree.tostring(types_tree)
		self.replace('[Content_Types].xml', types)
		return self
	
	def make_mask_rels(self):
		"""重新分配资源id和文件名防止合并冲突
		wf.mask_mask_rels()	  # [{'id', ... 'id_': ... 'target_'}]
		"""
		rels = self.get_doc_rels()
		rels_tree = etree.fromstring(rels)
		tmp = []
		for rel_ele in rels_tree:
			type_ = rel_ele.attrib['Type']   # 与系统变量type重名加_
			pass_list = ['endnotes', 'theme', 'setting', 'styles', 'fontTable', 'footnotes', 'webSettings']
			flag = False
			for item in pass_list:
				if item in  type_:
					flag = True
					break
			if flag:
				continue
			random_int = random.randint(1000, 9999)
			target = rel_ele.attrib['Target']
			# media/5585.png
			target_ = ((target.split('/')[0] +'/') if '/' in target else '') + str(random_int) + '.' + target.split('.')[-1]
			img_formats = ['png', 'jpg', 'gif']   # 图片格式除jpeg外会报错
			for img_format in img_formats:
				if img_format in target_:
					target_ = target_.replace(img_format, 'jpeg') 
			tmp.append({
				'id': rel_ele.attrib['Id'],
				'type': type_,
				'target': target,
				'id_': 'rId%s' % random_int,
				'target_': target_,
			})
		return tmp

	
	def merge_mask_rels(self, rels):
		"""合并映射
		rels = wf1.mask_rels()
		rst = wf2.merge_mask_rels(rels)
		"""
		doc_rel = self.get_doc_rels()
		doc_rel_tree = etree.parse(BytesIO(doc_rel))
		root = doc_rel_tree.getroot()
		for rel in rels:
			rel_ele = E.Relationship(Id=rel['id_'], Type=rel['type'], Target=rel['target_'])
			root.append(rel_ele)
		return etree.tostring(root)

	def merge(self, wf):
		"""合并文档
		wf1 = WordFile('cover.docx')
		wf2 = WordFile('catalog.docx')
		rst = wf1.merge(wf2)
		"""
		# 合并资源文件
		wf_rels = wf.make_mask_rels()
		for rels in wf_rels:
			filename = 'word/' + rels['target']
			content = wf.get(filename)
			filename_ = 'word/' + rels['target_']
			self.add(filename_, content)
		# 合并资源映射
		new_rels = self.merge_mask_rels(wf_rels)
		self.replace('word/_rels/document.xml.rels', new_rels)
		# 替换资源id
		document2 = wf.get_document().decode()
		for rels in wf_rels:
			document2 = document2.replace(rels['id'], rels['id_'])
		wf = WordFile(wf.replace('word/document.xml', document2))
		# 合并document
		document1 = self.get_document()
		document2 = wf.get_document()
		etree1 = etree.fromstring(document1)
		etree2 = etree.fromstring(document2)
		etree1_body = etree1[0]
		etree2_body = etree2[0]
		sect_pr = etree1_body[-1]
		etree1_body.remove(sect_pr)
		for element in etree2_body:
			etree1_body.append(element)
		self.replace('word/document.xml', etree.tostring(etree1).decode())


if __name__ == '__main__':
	wf1 = WordFile('template.docx')
	# wf2 = WordFile('catalog.docx')
	# wf1.merge(wf2)
	# wf.add('haha','123')
	# print(wf)
	# rst = wf1.merge(wf2)
	# print(wf.file_path)




