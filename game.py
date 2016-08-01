#!/usr/bin/env python3
"""
      (0,0) . . . o . . . . . . . . . (12,0)        . . . o . . . . . . . . .
           . . . o o . . . . . . . .                . . . o o . . . . . . . .
          . . . o o o . . . . . . .                 . . . o o o . . . . . . .
         o o o o o o o o o o . . .                  o o o o o o o o o o . . .
        . o o o o o o o o o . . .                   . o o o o o o o o o . . .
       . . o o o o o o o o . . .                    . . o o o o o o o o . . .
      . . . o o o o o o o . . .                     . . . o o o o o o o . . .
     . . . o o o o o o o o . .                      . . . o o o o o o o o . .
    . . . o o o o o o o o o .                       . . . o o o o o o o o o .
   . . . o o o o o o o o o o                        . . . o o o o o o o o o o
  . . . . . . . o o o . . .                         . . . . . . . o o o . . .
 . . . . . . . . o o . . .                          . . . . . . . . o o . . .
. . . . . . . . . o . . . (12,12)                   . . . . . . . . . o . . .
"""

import termios, sys

def getitem(arr,idx,*rest):
	if len(rest)==0:
		return arr[idx]
	return getitem(arr[idx],*rest)

def setitem(arr,val,idx,*rest):
	if len(rest)==0:
		arr[idx]=val
		return
	setitem(arr[idx],val,*rest)


class Board:
	def __init__(self,n,np):
		self.N=n
		self.NP=np
		self.boardh=4*self.N-3
		self.arr=[[-1]*self.boardh for _ in range(self.boardh)]
		self.loopboard(
			lambda _: None,
			lambda x,y: setitem(self.arr,0,y,self.jof(x,y)),
			lambda _: None)
		self.initplayers()
	
	def jof(self,x,y):
		if y<self.N-1: return x+self.N-1
		if y<2*self.N-1: return x+y-self.N+1
		if y<3*self.N-2: return x+self.N-1
		return x+y-self.N+1

	def indentofy(self,y):
		if y<self.N-1: return 3*self.N-2-y
		if y<2*self.N-1: return 2+y-self.N
		if y<3*self.N-2: return 3*self.N-2-y
		return y-self.N+2
	
	def xofxy(self,x,y):
		return self.indentofy(y)+2*x

	def widthofy(self,y):
		if y>2*self.N-2: y=4*self.N-4-y
		if y<self.N-1: return y+1
		return 4*self.N-3-y

	def loopboard(self,linestartfn,cellfn,lineendfn):
		for i in range(self.N-1):
			if linestartfn(i): return
			for j in range(i+1):
				if cellfn(j,i): return
			if lineendfn(i): return
		for i in range(self.N):
			if linestartfn(i+self.N-1): return
			for j in range(i,3*self.N-2):
				if cellfn(j-i,i+self.N-1): return
			if lineendfn(i+self.N-1): return
		for i in range(1,self.N):
			if linestartfn(i+2*self.N-2): return
			for j in range(self.N-1,3*self.N-2+i):
				if cellfn(j-self.N+1,i+2*self.N-2): return
			if lineendfn(i+2*self.N-2): return
		for i in range(1,self.N):
			if linestartfn(i+3*self.N-3): return
			for j in range(i,self.N):
				if cellfn(j-i,i+3*self.N-3): return
			if lineendfn(i+3*self.N-3): return

	def loopboardprint(self,cellfn):
		self.loopboard(
			lambda y: print(" "*self.indentofy(y),end=""),
			cellfn,
			lambda y: print())

	def draw(self,status=""):
		charsupply=lambda i,j: " .123"[self.arr[i][j]+1]
		self.loopboardprint(lambda x,y: print(charsupply(y,self.jof(x,y)),end=" "))
		decorate(self,status)

	def initplayers(self):
		if self.NP<1: return
		self.loopboard(
			lambda _: None,
			lambda x,y: True
			            if y>=self.N
			            else setitem(self.arr,1,y,self.jof(x,y))
			            if y<self.N-1 or self.N-1<=x<=2*self.N-2
			            else y>=self.N,
			lambda _: None)
		if self.NP<2: return
		self.loopboard(
			lambda _: None,
			lambda x,y: setitem(self.arr,2,y,self.jof(x,y))
			            if 2*self.N-2<=y<=3*self.N-3 and x>=2*self.N-2
			            else None,
			lambda _: None)
		if self.NP<3: return
		self.loopboard(
			lambda _: None,
			lambda x,y: setitem(self.arr,3,y,self.jof(x,y))
			            if 2*self.N-2<=y<=3*self.N-3 and x<=y-2*self.N+2
			            else None,
			lambda _: None)


def decorate(b,status):
	""" Assumes being on the line below the board """
	output("\x1B[G\x1B[{0}A\x1B[{1}C\x1B7".format(4*b.N-3,3*b.N-2))
	statusx=6*b.N+2
	output("\x1B[{0}G".format(statusx))
	for line in status.strip().split("\n"):
		output(line)
		output("\x1B[{0}G\x1B[B".format(statusx))
	output("\x1B8")

def getmove(b,player):
	x=y=0
	px=b.xofxy(0,0)
	py=0
	while True:
		c=sys.stdin.read(1)
		if c=="h": x=x-1 if x>0 else x
		elif c=="j": y=y+1 if y<b.boardh-1 else y
		elif c=="k": y=y-1 if y>0 else y
		elif c=="l": x=x+1 if x<b.widthofy(y)-1 else x
		elif c=="\x0C":
			output("\x1B[{0}B\r".format(b.boardh-y+1))
			b.draw()
			x=y=0
			px=b.xofxy(0,0)
			py=0
			continue
		elif c=="\n":
			if b.arr[py][b.jof(px,py)]!=player:
				output("\x07")
				continue
			break
		else: continue
		if x>=b.widthofy(y): x=b.widthofy(y)-1
		px2=b.xofxy(x,y)
		py2=y
		if px<px2: output("\x1B[{0}C".format(px2-px))
		elif px>px2: output("\x1B[{0}D".format(px-px2))
		px=px2
		if py<py2: output("\x1B[{0}B".format(py2-py))
		elif py>py2: output("\x1B[{0}A".format(py-py2))
		py=py2
	return px, py


def output(*args):
	print(*args,end="")
	sys.stdout.flush()

def main():
	tioorig=termios.tcgetattr(sys.stdin)
	tio=termios.tcgetattr(sys.stdin)
	tio[3]&=~(termios.ECHO|termios.ECHOE|termios.ECHOKE|termios.ECHOCTL|termios.ECHONL|termios.ICANON|termios.IEXTEN)
	tio[6][termios.VMIN]=1
	tio[6][termios.VTIME]=0
	termios.tcsetattr(sys.stdin,termios.TCSAFLUSH,tio)

	nplayers=2
	b=Board(4,nplayers)
	player=1
	while True:
		b.draw("status:\n- dingen\n- meer dingen")
		mv=getmove(b,player)
		player=player%nplayers+1
	
	termios.tcsetattr(sys.stdin,termios.TCSAFLUSH,tioorig)

if __name__=="__main__":
	main()
