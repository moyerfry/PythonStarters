import os
import argparse
import re

def get_parsed_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--dir", help="The directory to run analysis on", type=str, default='.')
	return parser.parse_args()

def partition(test, items):
	trues = []
	falses = []
	for item in items:
		if test(item):
			trues.append(item)
		else:
			falses.append(item)
	return trues, falses

# Returns a list of tuples of (dir_name, file_name)
def get_files(path, depth=0):
	files_here, dirs_here = partition(lambda x: os.path.isfile(path + '/' + x), os.listdir(path))
	# Negative numbers force recursion
	if depth != 0:
		for directory in dirs_here:
			files_here.extend(get_files(path + '/' + directory, depth - 1))
	return map(lambda x: (path + '/' + x[0], x[1]), map(lambda x: ('', x), files_here))


def main():
	parsed_args = get_parsed_args()
	working_directory = parsed_args.dir[:-1] if parsed_args.dir[-1] in ['/', '\\'] else parsed_args.dir
	files_to_search = get_files(working_directory)
	all_includes = []
	for file_desc in files_to_search:
		with open(file_desc[0] + '/' + file_desc[1], 'r') as f:
			includes = filter(lambda x: re.match(r'#include.+', x), f.readlines())
		all_includes.extend(filter(lambda x: x not in all_includes, includes))
	filtered_includes = filter(lambda x: re.findall(r'".+"', x), all_includes)
	just_names = map(lambda x: x[1], files_to_search)
	filtered_includes = filter(lambda x: x not in just_names, map(lambda x: re.findall(r'".+"', x)[0][1:-1], filtered_includes))
	for item in files_to_search:
		print item
	print '\n'
	for item in filtered_includes:
		print item
	pass

if __name__ == '__main__':
	main()