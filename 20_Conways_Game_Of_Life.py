'''
MIT License

Copyright (c) 2020 Georg Thurner

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
'''

#20 Conway’s Game of life (1000 points) Prepare a script running a simulation of the “Conway’s Game of life” for 1000 steps on a board N × N initially filled randomly with a probability p and for a number of steps M . The variables N , p and M are provided by the user. Use periodic boundary conditions. The output should be an animated GIF. Prepare a script providing also two animated GIFs for the Gosper glider gun and the Simkin glider gun on a board N × N for a number of steps M .

import numpy as np
import time
import itertools
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from progress.bar import IncrementalBar
from PIL import Image

class InputError(Exception):
	'''
	Additional exception that can be raised to hint at wrong input.
	Takes and returns expression(where the Error occurs) and message.
	'''
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message


class Conways_Game_Of_Life:
	'''
	Conways game of life.
	Object consists of a board saved as numpy array 
	Initialisation can either be done via 2d arraylike input as start_conf or via a given boardsize
	If boardsize is given and p_life is given, cells life with this probability, if not initialised with zeros 
	'''	
	def __init__(self,boardsize = None, start_conf = None, p_life = None):
		if boardsize == None and start_conf == None:
			raise InputError("__init__","Expect either a tuple for boardsize or a 2dim arraylike for start_conf")
		elif boardsize != None and start_conf != None:
			raise InputError("__init__","Expect only either boardsize or start_conf")
		elif boardsize != None:
			self.height = boardsize[0]
			self.length = boardsize[1]
			if p_life != None:
				board = []
				for i in  range(self.height * self.length):
					board.append(np.random.choice(2,p = [1-p_life,p_life]))
				self.board = np.array(board).reshape((self.height,self.length))
			else:
				self.board = np.zeros(shape = [self.height,self.length],dtype='int')
		else:
			self.board = np.array(start_conf)
			self.height = self.board.shape[0]
			self.length = self.board.shape[1]

	def __str__(self):
		return(np.array_str(self.board))
	

	def evolution_step(self):
		'''Computes the next evoulutionstep an returns it'''

		#Returns matrix where for each index all eigth corresponding neighbourcells are added up at the given index
		added_ngbh = sum(np.roll(np.roll(self.board,i,0),j,1) for i,j in itertools.product((-1,0,1),(-1,0,1)) if(i != 0 or j != 0))
		#Use bitwise operation to return elementwise 0 and 1 
		return (self.board & (added_ngbh == 2)) | (added_ngbh == 3)


	def create_gif(self, steps, milsec_per_frame = 50, gif_name = 'ConwaysGameOfLife', dpi = 80):
		'''	
		Creates a gif with x steps from the given start setup

		milsec_per_frame: time each step is displayed in milliseconds; defaults to 50
		gif_name: sets the name of the outputfile; defaults to 'ConwaysGameOfLife'
		dpi: "Clear"; defaults to 80
		'''
		
		original_board = self.board
		bar = IncrementalBar('Processing: '+gif_name, max=steps+1, suffix= '%(percent)d%%')

		def update(i):
			self.board = self.evolution_step()
			img.set_data(self.board)
			ax.set_axis_off()
			bar.next()

		fig, ax = plt.subplots()
		img = ax.imshow(self.board,cmap = "Greys")
		anim = animation.FuncAnimation(fig, update, frames=np.arange(0, steps), interval=milsec_per_frame)
		anim.save( (gif_name +'.gif'), dpi=dpi, writer='imagemagick')
		plt.close()
		bar.finish()
		self.board = original_board


	def insert_construct(self,construct, coord):
		'''
		Inserts a given 2d array like construct at the given coord(tuple)
		starting counting by 0 (coord refer to the left upper entry)
		'''

		#One could catch "thousnds" of possible errors or rely on an intelligent User(only 0 and 1 in matrix right sizes etc)"
		construct = np.array(construct) #e.g. prevent indexing errors if list of list were given
		self.board[np.ix_(range(coord[0],construct.shape[0]+coord[0]), range(coord[1],construct.shape[1]+coord[1]))] = construct
		


gosper_glidergun = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],[1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

simkin_glidergun = [[1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]]

glider_death = [[1,1,0,0],[1,0,0,0],[0,1,1,1],[0,0,0,1]]



rand_game_of_life = Conways_Game_Of_Life(boardsize = (100,100), p_life = 0.6)
rand_game_of_life.create_gif(100,milsec_per_frame = 10)
glidergun1 = Conways_Game_Of_Life(boardsize = (100,100))
glidergun1.insert_construct(gosper_glidergun,(0,0))
glidergun1.insert_construct(glider_death,(80,93))
glidergun1.create_gif(2000, gif_name = "gosper_glidergun")
glidergun2 = Conways_Game_Of_Life(boardsize = (100,100))
glidergun2.insert_construct(simkin_glidergun,(20,20))
glidergun2.create_gif(1000,gif_name = "simkin_glidergun",milsec_per_frame = 20)

