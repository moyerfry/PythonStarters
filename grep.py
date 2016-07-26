import os
import re
import argparse

# Report depth is how many layers down to report. So a depth of 0 just tells you what settings are used
# in all the files in start_dir. A setting of 1 would tell you what settings are used in each sub dir
# of the start_dir
name_filter = r'.+.cs'
dir_filter = r''
print_to_console = True
print_to_file = 'C:/Users/david.frymoyer/Desktop/CcuSettingsUses.txt'
base_dir_is_solution_folder = True


def get_occurances(lines, regex_to_match):
	found_occurances = []
	for line in lines:
		matches = re.findall(regex_to_match, line)
		if matches:
			found_occurances.extend(matches)
	return found_occurances


def find_occurances(file_name, regex_to_match):
	with open(file_name, 'r') as open_file:
		return get_occurances(open_file.readlines(), regex_to_match)


def is_good_filter(str_line):
	return 'Save' not in str_line


def format(str_setting):
	return str_setting.split('.')[-1]


def main():
	parser = argparse.ArgumentParser(description="This is essentially a Python equivalent of grep")
	parser.add_argument("-d","--depth", dest='depth', help="The granularity to report with", type=int, default=-1)
	parser.add_argument("rest", nargs="*")
	parser.add_argument("-R", action="store_true", dest='recurse', default=False)
	parser.add_argument("-P", action="store_true", dest="perl", default=False)
	parser.add_argument("-t", dest='test', action="store_true", default=False)
	args = parser.parse_args()
	if args.test:
		test_num = 1
		def test_func(actual, expected):
			if actual == expected:
				print 'Test {0} passed'.format(test_num)
			else:
				print 'Test {0} failed'.format(test_num)
		test_func(get_occurances(['Bad line', 'Good line'], r'Good'), ['Good'])
	else:
		report_depth = args.depth
		if len(args.rest) < 1:
			print 'Please enter a pattern to search for'
		elif len(args.rest) >= 1:
			if args.perl:
				test = lambda x: re.match(args.rest[0], x)
			else:
				test = lambda x: args.rest[0] in x
			if len(args.rest) > 1:
				start_dir = args.rest[1]
			else:
				start_dir = '.'

		out_dict = {}
		current_key = ''
		# Account for absolute/relative directories
		actual_report_depth = report_depth + start_dir.count('/') + start_dir.count('\\')
		for current_dir, sub_dirs, files in os.walk(start_dir):
			if current_dir.count('/') + current_dir.count('\\') == actual_report_depth:
				current_key = current_dir
				out_dict[current_key] = []
			for item in filter(test, files):
				for new_occurance in find_occurances(current_dir+'/'+item, match_str):
					if current_key and new_occurance not in out_dict[current_key] and is_good_filter(new_occurance):
						out_dict[current_key].append(new_occurance)
		if print_to_console:
			for key in out_dict.keys():
				print 'Key is: ' + key
				for item in out_dict[key]:
					print item
		if print_to_file:
			to_print = []
			for key in out_dict.keys():
				ending = key.split('/')[-1].split('\\')[-1]
				if base_dir_is_solution_folder:
					to_print.append('Project is ' + ending + '\n')
				to_print.extend(map(lambda x: format(x), out_dict[key]))
				to_print.append('\n')
			with open(print_to_file, 'w') as print_file:
				print_file.writelines(map(lambda x: x + '\n', to_print))

if __name__ == '__main__':
	main()