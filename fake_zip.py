from zipfile import ZipFile
import os

class FakeZip(object):
	"""伪Zip对象，只作文件内容存储
	解决Zip无法直接替换文件问题
	"""
	def __init__(self, file_path):
		self.dict = {}
		self.file_path = file_path
		zip = ZipFile(file_path)
		for fileinfo in zip.infolist():
			file_data = zip.open(fileinfo).read()
			self.dict[fileinfo.filename] = file_data

	def get(self, filename):
		"""获取文件内容
		fz.get('haha.txt')
		"""
		if filename in self.dict:
			return self.dict[filename]
		else:
			return None

	def replace(self, filename, content):
		"""替换文件内容
		fz.replace('haha.txt', '567')
		"""
		self.dict[filename] = content
		return self

	def add(self, filename, content):
		"""添加文件
		fz.add('haha.txt', 'haha')"""
		self.dict[filename] = content
		return self

	def save(self, path):
		empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		with open(path, 'wb') as zip:
			zip.write(empty_zip_data)
		z = ZipFile(path, 'w')
		for k, v in self.dict.items():
			z.writestr(k, v)
		return path

	def save_and_open(self, path):
		os.startfile(self.save(path))



if __name__ == '__main__':
	fz = FakeZip('haha.zip')
	fz.replace('haha.txt', '567')
	print(fz.get('haha.txt'))




