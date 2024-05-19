'''
List the files and dirs

By @hopkeinst
'''

# Imports
import os
import humanize
from typing import TextIO

file_name = ''
dir_name = ''
cnt_files = 0
cnt_dirs = 0
cnt_links = 0
cnt_others = 0
extensions_text = ['.txt', '.csv', '.doc', '.docx']

def init_vars() -> None:
	'''
	Initialize variables for the script to run correctly

	Args:
		None

	Returns:
		None
	'''
	global file_name, dir_name, cnt_files, cnt_dirs, cnt_links, cnt_others
	print('Insert output file name (text): ', end='')
	file_name = input()
	get_extension = False
	for ext in extensions_text:
		if ext in file_name:
			get_extension = True
			break
	if get_extension == True:
		file_name = file_name.rsplit('.', 1)[0]
	file_name += '.txt'
	print('Enter the name of the directory to examine [absolute or relative]: ', end='')
	dir_name = input()
	cnt_files = 0
	cnt_dirs = 0
	cnt_links = 0
	cnt_others = 0

def get_size(path: str) -> int:
	'''
	Obtain the size of the file or directory specified by the path, in KBs

	Args:
		path (str): Path, as a string, of the directory or file to obtain its size

	Returns:
		Retrieved size, in KBs, is an integer
	'''
	if os.path.isfile(path):
		return os.path.getsize(path)
	total_size = 0
	for element in os.listdir(path):
		element_path = os.path.join(path, element)
		total_size += get_size(element_path)
	return total_size

def to_list_dirs(path_dir: str, sequence: list = [], lvl: int = 0) -> None:
	'''
	Serves to list all elements within a path. 
	It displays from the root element and goes towards the children and the children of the children, and so on. 
	It displays the results on the screen and in the output file. 
	If it's a directory, it looks inside and so on. It forms the inheritance tree.
	
	Args:
		path_dir (str): The path to evaluate
		sequence (list): A list used to know whether to draw the lines of the tree or not
		lvl (int): The depth level of the element

	Returns:
		None
	'''
	global cnt_dirs, cnt_files, cnt_links, cnt_others
	if lvl != 0:
		print('─ ' + os.path.basename(path_dir) + ' (' + str(humanize.naturalsize(get_size(path_dir), format='%.3f')) + ')')
		file_output.write('─ ' + os.path.basename(path_dir) + ' (' + str(humanize.naturalsize(get_size(path_dir), format='%.3f')) + ')\n')
	else:
		print(os.path.basename(path_dir) + ' (' + str(humanize.naturalsize(get_size(path_dir), format='%.3f')) + ')')
		file_output.write(os.path.basename(path_dir) + ' (' + str(humanize.naturalsize(get_size(path_dir), format='%.3f')) + ')\n')
	elements = sorted(os.listdir(path_dir))
	len_elements = len(elements)
	cnt_elements = 0
	for element in elements:
		index_me = 0
		next = False
		if lvl > 0:
			dir_parent = path_dir.rsplit('/', 1)[0]
			me = path_dir.rsplit('/', 1)[1]
			index_me = (sorted(os.listdir(dir_parent))).index(me)
			if (index_me + 1) != len(os.listdir(dir_parent)):
				next = True
			if len(sequence) > lvl:
				sequence = sequence[:lvl]
			elif len(sequence) == 0:
				sequence = [int(next)]
			elif len(sequence) < lvl:
				sequence.append(int(next))
		path_element = os.path.join(path_dir, element)
		cnt_elements += 1
		for i in range(lvl):
			print('  ', end='')
			file_output.write('  ')
			if lvl > 0:
				if sequence[i] == 0:
					print(' ', end='')
					file_output.write(' ')
				else:
					print('│', end='')
					file_output.write('│')
		print('  ', end='')
		file_output.write('  ')
		if cnt_elements == len_elements:
			print('└', end='')
			file_output.write('└')
		else: 
			print('├', end='')
			file_output.write('├')
		if os.path.isdir(path_element):
			cnt_dirs += 1
			to_list_dirs(path_dir = path_element, sequence = sequence, lvl = (lvl + 1))
		else:
			print('─ ' + element + ' (' + str(humanize.naturalsize(get_size(path_element), format='%.3f')) + ')')
			file_output.write('─ ' + element + ' (' + str(humanize.naturalsize(get_size(path_element), format='%.3f')) + ')\n')
			if os.path.isfile(path_element) :
				cnt_files += 1
			elif os.path.islink(path_element) :
				cnt_links += 1
			else:
				cnt_others += 1

if __name__ == "__main__":
	init_vars()
	print('=' * 50)
	print('File name output: ' + file_name)
	print('Dir to examine: ' + dir_name)
	print('=' * 50)
	print('{:^50s}'.format('DETAILS'))
	print('=' * 50)
	with open(file_name, 'w', encoding='utf-16') as file_output:
		to_list_dirs(path_dir = dir_name, sequence = [])
		file_output.write('\n')
		print('\n', '=' * 50, sep = '')
		for i in range(50):
			file_output.write('=')
		file_output.write('\nTotal elements: ' + str(cnt_dirs + cnt_files + cnt_links + cnt_others) + ' \n')
		print('Total elements: ' + str(cnt_dirs + cnt_files + cnt_links + cnt_others))
		print('=' * 50)
		for i in range(50):
			file_output.write('=')
		file_output.write('\nTotal dirs: ' + str(cnt_dirs) + ' \n')
		file_output.write('Total files: ' + str(cnt_files) + ' \n')
		file_output.write('Total links: ' + str(cnt_links) + ' \n')
		file_output.write('Total others: ' + str(cnt_others) + ' \n')
		for i in range(50):
			file_output.write('=')
		file_output.close()

		print('Total dirs: ' + str(cnt_dirs))
		print('Total files: ' + str(cnt_files))
		print('Total links: ' + str(cnt_links))
		print('Total others: ' + str(cnt_others))
		print('=' * 50)
		print('Generated file with details: ' + file_name)
