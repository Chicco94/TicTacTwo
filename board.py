from random import choice
from consts import *

class Board():
	def __init__(self):
		self.board = [0 for x in range(9)]
		self.current_player = PLAYER_1
		self.last_move = None


	def _value_to_char(self,value):
		if value == 0: return ' '
		if value == 1: return '|'
		if value == 2: return '--'
		if value == 3: return '+'
		raise ValueError
	

	def check_win(self):
		# vittoria orrizontale
		if sum(self.board[0:3])==9: return True
		if sum(self.board[3:6])==9: return True
		if sum(self.board[6:9])==9: return True
		
		# vittoria verticale
		if self.board[0]+self.board[3]+self.board[6]==9: return True
		if self.board[1]+self.board[4]+self.board[7]==9: return True
		if self.board[2]+self.board[5]+self.board[8]==9: return True
		
		# vittoria obliqua
		if self.board[0]+self.board[4]+self.board[8]==9: return True
		if self.board[2]+self.board[4]+self.board[6]==9: return True
		return False
	

	def available_moves(self,forced_player=None,forced_last_move=None):
		player = forced_player if forced_player else self.current_player
		last_move = forced_last_move if forced_last_move else self.last_move
		moves = []
		for index,cell in enumerate(self.board):
			if index == last_move: continue
			if cell == 0: moves.append(index)
			elif cell==1 and player == PLAYER_2: moves.append(index)
			elif cell==2 and player == PLAYER_1: moves.append(index)
		assert len(moves)>0
		return moves




	def apply_move(self,cell,forced_player=None)->bool:
		player = forced_player if forced_player else self.current_player
		if cell not in self.available_moves(forced_player):
			return False
		self.last_move = cell
		self.board[cell] += 1 if player == PLAYER_1 else 2
		return True
	
	def revert_move(self,cell,forced_player=None)->bool:
		player = forced_player if forced_player else self.current_player
		self.board[cell] -= 1 if player == PLAYER_1 else 2
		return True


	def ai_move(self,forced_player=None,forced_last_move=None)->int:
		player = forced_player if forced_player else self.current_player
		last_move = forced_last_move if forced_last_move else self.last_move
		best_score = MIN
		best_move = -1
		moves = self.available_moves(player,last_move)
		for move in moves:
			self.apply_move(move)
			score = self.minmax(0,False,not player,move)
			self.revert_move(move)

			if score > best_score:
				best_score= score
				best_move = move

		self.apply_move(best_move)
		print(best_move)
		return best_move


	def get_board_value(self,player,last_move=-1)->int:
		value = 0
		# if I can win in one move
		moves = self.available_moves(player,last_move)
		for move in moves:
			self.apply_move(move,player)
			if self.check_win(): value = MAX
			self.revert_move(move)
			
		# if opponent can win in one move
		moves = self.available_moves(not player,last_move)
		for move in moves:
			self.apply_move(move,not player)
			if self.check_win(): value = MIN
			self.revert_move(move,not player)
		return value
	
	def minmax(self,depth,isMax,player,last_move,max_depth=5):
		if depth>=max_depth:
			return 0
		score = self.get_board_value(player,last_move)
		if score == MAX: return score
		if score == MIN: return score

		if isMax:
			best = MIN
			moves = self.available_moves(player,last_move)
			for move in moves:
				self.apply_move(move,player)
				best = max(best,self.minmax(depth+1,not isMax,not player,move))
				self.revert_move(move,player)
			return best
		else:
			best = MAX
			moves = self.available_moves(player,last_move)
			for move in moves:
				self.apply_move(move,player)
				best = min(best,self.minmax(depth+1,not isMax,not player,move))
				self.revert_move(move,player)
			return best