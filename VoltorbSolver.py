# Ordered top to bottom
right_row = [(4, 1), (6, 1), (2, 3), (9, 1), (4, 2)]

# Ordered left to right
bottom_row = [(5, 2), (6, 0), (4, 2), (5, 2), (5, 2)]

class Space:
	@staticmethod
	def IsEmpty():
		return True

	@staticmethod
	def IsBomb():
		return False

	@staticmethod
	def IsCoin():
		return False

	@staticmethod
	def GetVal():
		return 0

class Bomb(Space):
	@staticmethod
	def IsEmpty():
		return False

	@staticmethod
	def IsBomb():
		return True

class Coin(Space):
	def __init__(self, val):
		self.point_value = val

	@staticmethod
	def IsEmpty():
		return False

	@staticmethod
	def IsCoin():
		return True

	def GetVal(self):
		return self.point_value

class Board:
	def __init__(self, dim, right, bottom):
		self.dim = dim
		self.num_rows = len(right)
		self.num_cols = len(bottom)
		if self.dim != self.num_rows or self.dim != self.num_cols:
			print "Invalid board"
		self.board = [Space()] * (self.num_rows * self.num_cols)
		self.row_info = right
		self.col_info = bottom

	def __str__(self):
		for i in range(self.num_rows):
			row = self.get_row(i)


	def get_col_number(self, num):
		return num % self.num_cols

	def get_row_number(self, num):
		return int(num / self.num_cols)

	def get_col(self, num):
		ret = []
		for i in range(self.num_rows):
			ret.append(self.board[i * self.num_cols + num])
		return ret

	def get_row(self, num):
		return self.board[num * self.num_cols:(num+1) * self.num_cols]

	def get_relevent_info(self, num):
		return self.row_info[self.get_row_number(num)], self.col_info[self.get_col_number(num)]

	@staticmethod
	def total_points(data_set):
		return sum(map(lambda x: x.GetVal(), data_set))

	@staticmethod
	def total_bombs(data_set):
		return sum(map(lambda x: x.IsBomb(), data_set))

	# Test against is a (num_points, num_bombs)
	def validate_set(self, data_set, test_against, must_equal=False):
		if len(data_set) != self.dim:
			print "Got bad data set"
			return False
		num_points = Board.total_points(data_set)
		num_bombs = Board.total_bombs(
			data_set)
		if must_equal:
			return num_points == test_against[0] and num_bombs == test_against[1]
		else:
			return num_points <= test_against[0] and num_bombs <= test_against[1]

	def is_valid(self, must_equal=True):
		for i in range(self.dim):
			if not self.validate_set(self.get_row(i), self.row_info[i], must_equal):
				return False
			if not self.validate_set(self.get_col(i), self.col_info[i], must_equal):
				return False
		return True

test_num = 1
def test(actual, expected):
	global test_num
	if actual == expected:
		print 'Test {0} passed'.format(test_num)
	else:
		print 'Test {0} failed'.format(test_num)
		print 'Expected {1}, got {0}'.format(actual, expected)
	test_num += 1

test_board = Board(2, [(3, 1), (2, 1)], [(3, 1), (2, 1)])
test(len(test_board.get_row(0)), 2)
test(test_board.get_row(0)[0].IsEmpty(), True)
test(test_board.validate_set([Coin(3), Bomb()], (3, 1)), True)
test(test_board.validate_set([Bomb(), Bomb()], (3, 1)), False)
test(test_board.validate_set([Coin(3), Coin(1)], (3, 1)), False)
test(test_board.is_valid(), False)
test_board.board = [Coin(3), Bomb(),
					Bomb(),  Coin(2)]
test(test_board.validate_set(test_board.get_row(0), test_board.row_info[0]), True)
test(test_board.is_valid(), True)
test(test_board.get_relevent_info(2), ((2, 1), (3, 1)))
test(test_board.get_relevent_info(3), ((2, 1), (2, 1)))

# -1 indicates a bomb
# 0 indicates an unsolved space
def solve_volt(right, bottom, board, posn=0):
	if posn >= len(board) and board.is_valid():
		print str(board)
		return True
	elif posn >= len(board):
		return False
	# Try a bomb

	# Try a list of values

	pass