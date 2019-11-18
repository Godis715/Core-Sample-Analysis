import os
import sys
import time
import ftplib

BASE_DIR_CLIENT = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_FILES_BY_NAME = {'.env', 'db.sqlite3'}
EXCLUDE_FILES_BY_PATH = {}

EXCLUDE_FOLDERS_BY_NAME = {'venv', 'tests', '__pycache__', '.idea'}
EXCLUDE_FOLDERS_BY_PATH = {f'{BASE_DIR_CLIENT}/mainService/mainService/static/core_sample'}

ftp = ftplib.FTP()




def server_isDir(obj_server, move_by_path_server=None):
	if move_by_path_server is not None:
		ftp.cwd(move_by_path_server)

	try:
		ftp.cwd(obj_server)
		ftp.cwd('..')
		isDir =  True
	except ftplib.error_perm:
		isDir =  False

	if move_by_path_server is not None:
		folders = filter(lambda x: x != '', move_by_path_server.split('/'))
		for folder in folders:
			ftp.cwd('..')
	
	return isDir

def server_isFile(obj_server, move_by_path_server=None):
	return not server_isDir(obj_server, move_by_path_server)


def remove_file(file_server, move_by_path_server=None):
	if move_by_path_server is not None:
		ftp.cwd(move_by_path_server)
	print(f">> Remove '{ftp.pwd()}/{file_server}'")
	ftp.delete(file_server)

	if move_by_path_server is not None:
		folders = filter(lambda x: x != '', move_by_path_server.split('/'))
		for folder in folders:
			ftp.cwd('..')

def remove_folder(folder_server, move_by_path_server=None):
	if move_by_path_server is not None:
		ftp.cwd(move_by_path_server)
	print(f"> Remove '{ftp.pwd()}/{folder_server}'")
	ftp.cwd(folder_server)
	for obj_folder_server in ftp.nlst():
		if server_isFile(obj_server=obj_folder_server):
			remove_file(file_server=obj_folder_server)
		else:
			remove_folder(folder_server=obj_folder_server)
	ftp.cwd('..')

	ftp.rmd(folder_server)

	if move_by_path_server is not None:
		folders = filter(lambda x: x != '', move_by_path_server.split('/'))
		for folder in folders:
			ftp.cwd('..')

	
sizeWritten = 0
def send_file(file_server, path_file_client):
	totalSize = os.path.getsize(path_file_client)
	blocksize = totalSize // 10

	def handle(block):
		global sizeWritten
		sizeWritten += blocksize
		if sizeWritten < totalSize:
			percentComplete = sizeWritten / totalSize
		else:
			percentComplete = 1

		print('\b' * (len(path_file_client) + 22), end='')
		print(f"> Send '{path_file_client}': {round(percentComplete * 100, 2)}%  ", end='')
		sys.stdout.flush()

	ftp.storbinary(cmd=f"stor {file_server}", fp=open(path_file_client,'rb'), callback=handle,blocksize=blocksize)
	print('')

def _get_filter_content_client(path_client):
	# Фильтрация папок по имени
	content_client_filter_1 = list(set(os.listdir(path_client)) - (EXCLUDE_FILES_BY_NAME | EXCLUDE_FOLDERS_BY_NAME))

	# Фильтрация папок по пути
	content_client_filter_1_with_path = set(f'{path_client}/{obj_client}' for obj_client in content_client_filter_1)
	content_on_folder_client_filter_2 = content_client_filter_1_with_path - (EXCLUDE_FOLDERS_BY_PATH | EXCLUDE_FOLDERS_BY_PATH)

	# Результат
	content_on_folder_client = list(path_obj_folder_client.rsplit('/', 1)[1] for path_obj_folder_client in content_on_folder_client_filter_2)
	return content_on_folder_client

def send_folder_content(folder_server, path_folder_client):
	# Переходим на сервере в папку, куда загружается контент
	ftp.cwd(folder_server)

	# Контент на загрузку
	content_on_folder_client = _get_filter_content_client(path_folder_client)
	
	# Лишний контент на сервере
	content_on_folder_server = ftp.nlst()
	remove_content_on_server = list((ftp.pwd(), obj_server) for obj_server in list(set(content_on_folder_server) - set(content_on_folder_client)))

	# Загружаем файлы
	files_on_folder_client = list(filter(lambda x: os.path.isfile(f'{path_folder_client}/{x}'), content_on_folder_client))
	for file_on_folder_client in files_on_folder_client:
		send_file(
			file_server=file_on_folder_client,
			path_file_client=f'{path_folder_client}/{file_on_folder_client}')

	# Создаём папки на сервере и загружаем туда контент из соответсвующих папок на клиенте
	folders_on_folder_client = list(filter(lambda x: os.path.isdir(f'{path_folder_client}/{x}'), content_on_folder_client))
	for folder_on_folder_client in folders_on_folder_client:
		if folder_on_folder_client not in content_on_folder_server:
			ftp.mkd(folder_on_folder_client)
		remove_content_on_server += send_folder_content(
			folder_server=folder_on_folder_client, 
			path_folder_client=f'{path_folder_client}/{folder_on_folder_client}')

	ftp.cwd('..')
	return remove_content_on_server



if __name__ == '__main__':

	print('Connect to FTP-server ...')
	print('>', ftp.connect('46.149.233.52', 30))

	print('')

	print('Login in FTP-server ...')
	ftp.login(os.environ['FTP_USER'], os.environ['FTP_PASSWORD'])

	ftp.set_debuglevel(2)
	# ftp.set_pasv(False)
	print(ftp.nlst())

	# print('')

	# print('Send mainService on server')
	# ftp.cwd(f'./mainService-site')
	# if 'mainService-test' not in ftp.nlst():
	# 	ftp.mkd('mainService-test')
	# remove_content_on_server = send_folder_content(
	# 	folder_server='mainService-test',
	# 	path_folder_client=f'{BASE_DIR_CLIENT}/mainService')
	# ftp.cwd('..')

	# print('')

	# print('Send analysisService on server')
	# ftp.cwd(f'./analysisService-site')
	# if 'analysisService-test' not in ftp.nlst():
	# 	ftp.mkd('analysisService-test')
	# remove_content_on_server += send_folder_content(
	# 	folder_server='analysisService-test',
	# 	path_folder_client=f'{BASE_DIR_CLIENT}/analysisService')
	# ftp.cwd('..')

	# print('')

	# print('Remove needless files and folders')
	# for remove_obj_on_server in remove_content_on_server:
	# 	if server_isDir(remove_obj_on_server[1], remove_obj_on_server[0]):
	# 		remove_folder(remove_obj_on_server[1], remove_obj_on_server[0])
	# 	else:
	# 		remove_file(remove_obj_on_server[1], remove_obj_on_server[0])
	
	# print('')

	ftp.quit()
	print('Success!')
