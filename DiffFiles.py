import re
import sys

STRIPPING_REGEX = r'[A-Za-z].+'

def strip_it(line):
	test = re.findall(STRIPPING_REGEX, line)
	if test:
		return test[0]

def main():
	file_names = sys.argv[-2:]

	if len(file_names) > 2:
		print 'Too many files'
		exit(-1)
	elif len(file_names) < 2:
		print 'Too few files'
		exit(-2)
	elif filter(lambda x: '.' not in x, file_names):
		print 'Need to have file extensions for both files'
		exit(-3)

	with open(file_names[0], 'r') as f, open(file_names[1], 'r') as g:
		first_file = filter(lambda x: x and x != '\n', f.readlines())
		second_file = filter(lambda x: x and x != '\n', g.readlines())
	
	for line in reversed(first_file):
		if line in second_file:
			del first_file[first_file.index(line)]
			del second_file[second_file.index(line)]

	with open(file_names[0].replace('.', '_diffs.'), 'w') as f, open(file_names[1].replace('.', '_diffs.'), 'w') as g:
		f.writelines(map(lambda x: x + '\n', first_file))
		g.writelines(map(lambda x: x + '\n', second_file))


if __name__ == '__main__':
	main()