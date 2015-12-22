from collections import deque
import copy, time

timer, pagesize=0, 2
timeout=None
processlist=None
opt_page_seq=[]
pmem, smem=None, None
Readyqueue=None

class BarebonesPage(list):		
	def __init__(self, instruction):
		super(BarebonesPage, self).append(instruction)
		self.ts=time.time()
		self.fifots=self.ts
	def updateTS(self):
		self.ts=time.time()

class BarebonesMemory(dict):  	
	def __init__(self, maxsize):
		self.maxsize=maxsize
	def add(self, page, instruction): 
		if page not in self.keys():
			self[page]=BarebonesPage(instruction)
		else: self[page].append(instruction)
	def swap(self, other, page1, page2): 
		if page1==page2:	
			self[page1]=copy.deepcopy(other[page1])
			del other[page2]
		else: 
			if hasattr(self[page1], "modified") and self[page1].modified==1:
				self[page1].modified=0
			self[page2]=copy.deepcopy(other[page2])
			other[page1]=copy.deepcopy(self[page1])
			del self[page1]
			del other[page2]

class BarebonesProcess(): 
	__id=0

	def __init__(self, f):
		self.id=BarebonesProcess.__id 
		self.name=f.name
		BarebonesProcess.__id+=1
		self.offset=0  
		self.start=0 
		self.end=self.curr=-1 
		self.V={} 
		self.acc=0 
		self.datalist=[]
		BarebonesProcess.pagegenerator(self, [i.strip() for i in f.readlines() if i!='\n']) 

	def pagegenerator(self, temp): 
		ISA=['LDA', 'STO', 'ADD', 'SUB', 'JNE', 'JGE', 'JMP', 'STP'] 
		count=0
		pagecount=len(smem) 
		flag=0
		self.start=pagecount 
		for i, ins in enumerate(temp):
			smem.add(pagecount, ins)
			flag=1
			if ins.split()[0].upper() not in ISA:
				self.datalist.append(pagecount)
				smem[pagecount].modified=0
				self.V[ins.split()[0]]=int(ins.split()[1]) 
			count+=1
			if count==pagesize:
				count, flag=0, 0
				pagecount+=1
		if flag==0: self.end=pagecount-1
		else: self.end=pagecount
		self.datalist=list(sorted(set(self.datalist)))
		self.curr=self.start

def primaryload(A, page, get_one=False): 

	def getswaplist(swappedin):
		L=list(set(pmem.keys())-set(swappedin))
		for i, j in enumerate(L): L[i]=(j, pmem[j].ts)
		return [x[0] for x in sorted(L, key=lambda x: x[1])]
		
	global frametable, cptr, Readyqueue

	""" ------- LRU WITH PREFETCHING BY DEFAULT------- """
	temp1, temp2=page, timer
	swappedin=[]
	A.curr+=1
	if len(pmem)<pmem.maxsize: 
		while True:
			if temp1 not in pmem.keys():
				pmem.swap(smem, temp1, temp1)
			swappedin.append(temp1)
			temp1+=1
			temp2+=pagesize
			if len(Readyqueue)>0 and len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1) or temp2>timeout: break
			elif len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1): break
	if len(pmem)==pmem.maxsize:
		L=getswaplist(swappedin)
		i=0
		while temp2<=timeout and len(L) > i: 
			if temp1 not in pmem.keys():
				pmem.swap(smem, L[i], temp1)
				i+=1
			temp1+=1
			temp2+=pagesize
			if len(Readyqueue)>0:
				if temp1 not in range(A.start, A.end+1) or temp2>timeout:
					break
			elif temp1 not in range(A.start, A.end+1): break

def primaryremove(A): 
	for page in range(A.start, A.end+1):
		if page in pmem.keys(): smem.swap(pmem, page, page)

def savecontext(A, PC, acc, V, page): 
	A.offset=PC
	A.acc=acc
	A.V=V
	A.curr=page

def memvarupdate(A, varname, newval, pageno): 
	page=pmem[pageno]
	for ctr, ins in enumerate(page):
		if ins.split()[0]==varname: pmem[pageno][ctr]=ins.split()[0]+' '+str(newval)
	pmem[pageno].modified=1
	pmem[pageno].updateTS()

def executeprocesses(): 
	global timer, Readyqueue
	Readyqueue=deque(processlist) 
	Running=Readyqueue.popleft() 
	Donequeue=deque() 
	acc, page, PC=0, 0, 0 
	V=Running.V 
	'''The most important part'''
	page_exec_seq=['']
	'''The most important part'''
	while True:
		timer+=1
		if Running==None and len(Readyqueue)==0: break
		if(PC==pagesize): 
			PC=0
			page+=1
		if (timer>timeout or Running==None) and len(Readyqueue)>0: 
					timer=1 
					if Running!=None:
						savecontext(Running, PC, acc, V, page) 
						Readyqueue.append(Running) 
					Running=Readyqueue.popleft() 
					V=Running.V 
					acc=Running.acc
					page=Running.curr
					PC=Running.offset
		elif timer>timeout: timer=1
		if page not in pmem.keys(): primaryload(Running, page)
		IR=pmem[page][PC].strip() 
		if IR.upper()=='STP': 
			primaryremove(Running)
			Donequeue.append(Running)
			Running=None
			continue
		CMD=IR[:IR.index(' ')]
		'''The most important part'''
		page_exec_seq.append(page) 
		'''The most important part'''
		pmem[page].updateTS()
		varname=IR[IR.index(' ')+1:len(IR)]
		if CMD.upper()=="LDA":
			acc=V[varname]  
			in_main=False
			for i in Running.datalist:
				try:
					if varname in [ins.split()[0] for ins in pmem[i] if len(ins.split())>1]: 
						in_main=True
						break
				except:
					if varname in [ins.split()[0] for ins in smem[i] if len(ins.split())>1]: break
			if not in_main: primaryload(Running, i, get_one=True) 		
			page_exec_seq.append(i)
			pmem[i].updateTS()
		elif CMD.upper()=='STO':
			V[varname]=acc
			in_main=False
			for i in Running.datalist:
				try:
					if varname in [ins.split()[0] for ins in pmem[i] if len(ins.split())>1]: 
						in_main=True
						break
				except:
					if varname in [ins.split()[0] for ins in smem[i] if len(ins.split())>1]: break
			if not in_main: primaryload(Running, i, get_one=True) 		
			page_exec_seq.append(i)
			pmem[i].updateTS()
			memvarupdate(Running, varname, acc, i) 
		elif CMD.upper()=='ADD': acc+=V[varname] 
		elif CMD.upper()=='SUB': acc-=V[varname] 
		elif CMD.upper()=='JNE':
			if acc!=0:
				temp=int(IR[IR.index(' ')+1:len(IR)])-1 
				page=(temp//pagesize)+Running.start 
				PC=temp%pagesize
				Running.curr=page 
				continue
		elif CMD.upper()=='JGE':
			if acc>=0:
				temp=int(IR[IR.index(' ')+1:len(IR)])-1
				page=(temp//pagesize)+Running.start 
				PC=temp%pagesize
				Running.curr=page 
				continue
		elif CMD.upper()=='JMP':
			temp=int(IR[IR.index(' ')+1:len(IR)])-1
			page=(temp//pagesize)+Running.start 
			PC=temp%pagesize
			Running.curr=page 
			continue
		PC+=1
	'''The most important part'''
	return page_exec_seq[1:]
	'''The most important part'''

'''The most important part'''
def main(pmemsize, programlist, m_timeout):
	global processlist, timeout, pmem, smem
	pagesize=2
	pmem, smem=BarebonesMemory(pmemsize), BarebonesMemory(128)
	processlist=[BarebonesProcess(open(pgm)) for pgm in programlist]
	timeout=m_timeout
	return executeprocesses()
'''The most important part'''