"""
----- MEMORY SIMULATOR PROGRAM (Backend) -----
 
Aim:	
To simulate basic memory management functions of an operating system in a uniprocessor environment 
which supports interleaved execution of multiple processes.
This simulator also aims to demonstrate page faults and how they are affected by parameters such as
frame size, program size, etc, and how to minimize them.

Features: 
	- Demonstrates page switching together with context switching (scheduling on FCFS basis only). 
(Emphasis has been laid on memory management function of OS, treating other OS functions as if it were a black box.)
	- Executes (more than one) meaningful programs written with MU0 instructions and displays the output for each program.
(Simulator assumes the programs are syntactically correct.)
	- Call the program using the command 
									python3 memsimv6.5.py
	- Demonstrates the working of the following replacement algorithms: 
		1) FIFO (w/ and w/o prepaging) 
		2) Random (w/ and w/o prepaging)
		3) Clock (w/o prepaging)
		4) LRU (w/ and w/o prepaging).
		5) Optimal (only for comparison purposes, it isn't a practical implementation.)

Note: In order to support pre-emptive paging, this simulator assumes that all processes are allowed to execute
a set number of instructions until a time out occurs. This is not the case in real time systems. 
Using a combination of LRU replacement and pre-emptive paging, we can reduce the number of page faults to less than 50%
compared to a system implementing FIFO replacement and demand-paging.

"""
# -----------------------------------------------------------------------------------

from collections import deque, OrderedDict

import sys, copy, time, math, random, re

timer, pagesize, pf_enable, algochoice=0, 2, 0, -1
frametable, cptr=[], 0
opt_list=[]

repalgo={1: 'FIFO', 2: 'Random', 3: 'Clock', 4: 'LRU', 5: 'Optimal (not practical)'}

pmem, smem=None, None

Readyqueue=None

# -----------------------------------------------------------------------------------

'''newly added'''
class Timer:

	def __init__(self, initial=None):
		self.started=0
		if initial==None:
			self.starttime=self.resumetime=self.timer=time.time()
		else: 
			self.starttime=self.resumetime=self.timer=time.time()+initial
	
	def __str__(self):
		if self.started==0:
			return str(self.timer - self.starttime)
		else: 
			return str(self.timer + time.time() - self.resumetime - self.starttime)

	def start(self):
		self.resume()

	def resume(self):
		self.started=1
		self.resumetime=time.time()

	def pause(self):
		self.started=0
		self.timer=self.timer + time.time()-self.resumetime

	def reset(self):
		self.started=0
		self.starttime=self.resumetime=self.timer=time.time()
'''newly added'''

# -----------------------------------------------------------------------------------

'''newly added'''
stopwatch=Timer()
'''newly added'''

# -----------------------------------------------------------------------------------

class Page(list):		#model class for pages stored in virtual memory

	def __init__(self, instruction):
		super(Page, self).append(instruction)
		self.ts=time.time()
		self.fifots=self.ts

	def __str__(self, timestamp=False):
		if timestamp is not False:
			s=repr(self)+ '\t' + str(self.ts)
			
			if hasattr(self, "modified"): 
				s+="\tM="+str(self.modified)
			return s

		else: 
			
			s=repr(self) 
			if hasattr(self, "modified"): 
				s+="\tM="+str(self.modified)
			return s
			
	def updateFifoTS(self):
		self.fifots=time.time()

	def updateTS(self):
		self.ts=time.time()

# -----------------------------------------------------------------------------------

class Memory(dict):  	#model class for memory objects (primary and secondary memory)
	def __init__(self, maxsize):
		self.maxsize=maxsize

	def __str__(self, timestamp=False):  #define the printing behaviour for the memory
	
		s=''
		
		for k, v in self.items():
			s+="PAGE{}".format(str(k))+'\t\t'+v.__str__(timestamp)+'\n'

		return s

	def add(self, page, instruction): #add instruction to the particular page 
		if page not in self.keys():
			self[page]=Page(instruction)

		else: self[page].append(instruction)

	def swap(self, other, page1, page2): #swap page1 of self (primary) with page2 of other (secondary)

		if page1==page2:	
			self[page1]=copy.deepcopy(other[page1])
			del other[page2]

		else: 
			

			if hasattr(self[page1], "modified") and self[page1].modified==1:
				self[page1].modified=0
				#print("Changing modified bit")

			self[page2]=copy.deepcopy(other[page2])
			other[page1]=copy.deepcopy(self[page1])
			del self[page1]
			del other[page2]

			#can't swap references, deleting will then cause both instances to go

# -----------------------------------------------------------------------------------

class Process(): #model class for processes 

	__id=0
	
	def __init__(self, f):

		"""
		A process has associated with it 
		pointers and other control data 
		which the OS needs to manage the process. This is the process control block
		"""

		# data follows this line
		self.id=Process.__id # unique process identifier
		self.name=f.name
		Process.__id+=1
		self.offset=0  #stores the offset relative to the page of the instruction last executed           
		self.start=0 #points to the first page of the process
		self.end=self.curr=-1 #end points to the last page, curr points to the current page being executed
		self.V={} #V stores the variable environment 
		self.acc=0 #acc stores the accumulator for this process which interacts with the processor accumulator
		
		self.datalist=[]

		'''newly added'''
		self.pagemap={}
		self.residentset=[]
		self.workingset=None
		'''newly added'''
		

		
		Process.pagegenerator(self, [i.strip() for i in f.readlines() if i!='\n']) 
		#pagegenerator is a class function which loads the instructions for the given process into secondary memory

	def pagegenerator(self, temp): #class function to load processes into main memory

		ISA=['LDA', 'STO', 'ADD', 'SUB', 'JNE', 'JGE', 'JMP', 'STP'] #MU0 instruction mnemonics 

		count=0
		pagecount=len(smem) #keeps track of the first free page frame of secondary memory
		flag=0

		self.start=pagecount #initialise start pointer

		for i, ins in enumerate(temp):
			#if(count==0): self[i//pagesize]=pagecount
			smem.add(pagecount, ins)
			flag=1
			if ins.split()[0].upper() not in ISA:
				
				self.datalist.append(pagecount)
				
				smem[pagecount].modified=0

				self.V[ins.split()[0]]=int(ins.split()[1]) #add variables to the process variable environment
				
			count+=1
			if count==pagesize:
				count=0
				pagecount+=1
				flag=0

		if flag==0: self.end=pagecount-1
		else: self.end=pagecount
		
		self.datalist=list(sorted(set(self.datalist)))
		
		self.curr=self.start

		'''newly added'''
		self.pagemap={ j : i for i, j in zip(range(0, self.end-self.start), range(self.start, self.end))}
		'''newly added'''

# -----------------------------------------------------------------------------------

def memdisplay(dispPrim=True): #simple display function for memory objects

	print()

	if dispPrim:
		print("PRIMARY MEMORY")
		for i, k in enumerate(frametable):
			if k[0] is None:
				print("F{}\t\t\tEmpty\t\t\t".format(i))
			else: 
				print("F{}\tPAGE{}    {}".format(i, k[0], pmem[k[0]]), end="")

				
				if hasattr(pmem[k[0]], "modified"): print("\tM={}".format(pmem[k[0]].modified))
				
	print()

	if len(smem) is not 0:
		print("SECONDARY MEMORY")
		print(smem.__str__(), end="")

# -----------------------------------------------------------------------------------

def primaryload(A, page, get_one=False): #load page 'page' for process 'A' in primary memory

	def getswaplist(swappedin):
		L=list(set(pmem.keys())-set(swappedin))

		if algochoice==1: #FIFO
			for i, j in enumerate(L):
				L[i]=(j, pmem[j].fifots)
			return [x[0] for x in sorted(L, key=lambda x: x[1])]

		elif algochoice==2: #Random
			random.shuffle(L)
			return L

		elif algochoice==3: #CLOCK 
			global frametable, cptr
			while True:
				temp=frametable[cptr]
				if temp[0]!=None and temp[1]==1:
					frametable[cptr]=(temp[0], 0)

				elif temp[0]!=None and temp[1]==0:
					cptr=(cptr+1)%len(frametable)
					return [temp[0]]
				cptr=(cptr+1)%len(frametable)

		elif algochoice==4: #LRU
			for i, j in enumerate(L):
				L[i]=(j, pmem[j].ts)
			return [x[0] for x in sorted(L, key=lambda x: x[1])]

		elif algochoice==5: #Optimal
			exec_dict={pm: opt_list.index(pm) if pm in opt_list else float('inf') for pm in L}
			return [x[0] for x in sorted(exec_dict.items(), key=lambda x: x[1], reverse=True)]

	global frametable, cptr, Readyqueue, stopwatch

	""" ------- PREFETCHING DISABLED (MULTI-PAGE LOADING STILL SUPPORTED)------- """

	if pf_enable == 0 or get_one==True:
		
		temp1, temp2=page, timer

		if len(pmem)<pmem.maxsize: #if there are free page frames in primary memory
			while True:
				if temp1 not in pmem.keys():

					'''newly added'''
					stopwatch.pause()
					print("| Moving", temp1, "to main memory |  ", end="")
					stopwatch.resume()
					'''newly added'''

					pmem.swap(smem, temp1, temp1)

					'''newly added'''
					A.residentset.append(temp1)
					'''newly added'''

					frametable[frametable.index((None, 0))]=(temp1, 1)
					pmem[temp1].updateFifoTS()
					if get_one==True: 
						return
				temp1+=1
				temp2+=pagesize

				if len(Readyqueue)>0 and (len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1) or temp2>timeout):
						break
				elif len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1): break
		
		else: 
			k=getswaplist([])[0]

			'''newly added'''
			stopwatch.pause()
			print("| Swapping", k, "and", page, end=" | ")
			stopwatch.resume()
			'''newly added'''
		
			pmem.swap(smem, k, page)
			
			'''newly added'''
			for process in processlist:
				if k in process.pagemap.values():    
					del process.residentset[process.residentset.index(k)]
					break

			A.residentset.append(page)
			'''newly added'''
			
			if algochoice==3: #using clock algorithm
				frametable[frametable.index((k, 0))]=(page, 1)
			else: 
				frametable[frametable.index((k, 1))]=(page, 1)
			pmem[page].updateFifoTS()

		A.curr+=1
		return

	""" ------- PREFETCHING ENABLED ------- """

	temp1, temp2=page, timer
	swappedin=[]	
	A.curr+=1

	if len(pmem)<pmem.maxsize: #if there are free page frames in primary memory
		while True:
			if temp1 not in pmem.keys():

				'''newly added'''
				stopwatch.pause()
				print("| Moving", temp1, "to main memory |  ", end="")
				stopwatch.resume()
				'''newly added'''

				pmem.swap(smem, temp1, temp1)
					
				'''newly added'''
				A.residentset.append(temp1)
				'''newly added'''

				frametable[frametable.index((None, 0))]=(temp1, 1)
				pmem[temp1].updateFifoTS()
			swappedin.append(temp1)
			temp1+=1
			temp2+=pagesize

			if len(Readyqueue)>0 and (len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1) or temp2>timeout):
					break
			elif len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1): 
					break

	if len(pmem)==pmem.maxsize:
		L=getswaplist(swappedin)
		i=0
		while temp2<=timeout and len(L) > i: 
						#second condition will matter only for very small main memories
			if temp1 not in pmem.keys():
				
				'''newly added'''
				stopwatch.pause()
				print("| Swapping", L[i], "and", temp1, end=" | ")
				stopwatch.resume()
				'''newly added'''
				
				pmem.swap(smem, L[i], temp1)

				'''newly added'''
				for process in processlist:
					if L[i] in process.pagemap.values():    
						del process.residentset[process.residentset.index(L[i])]
						break

				A.residentset.append(temp1)
				'''newly added'''

				try:
					frametable[frametable.index((L[i], 1))]=(temp1, 1)
				except: 
					frametable[frametable.index((L[i], 0))]=(temp1, 1)
				i+=1
				pmem[temp1].updateFifoTS()
			temp1+=1
			temp2+=pagesize

			if len(Readyqueue)>0 and (temp1 not in range(A.start, A.end+1) or temp2>timeout):
					break
			elif temp1 not in range(A.start, A.end+1): break

# -----------------------------------------------------------------------------------

def executeprocesses(): #main method for executing the required number of processes
	global timer, Readyqueue
	
	print(smem)

	def primaryremove(A): #inner function to remove pages from a terminated process

		A.residentset=[None]*timeout
		A.workingset.clear()

		for page in range(A.start, A.end+1):
			if page in pmem.keys():
				smem.swap(pmem, page, page)
				try:
					frametable[frametable.index((page, 1))]=(None, 0)
				except: 
					frametable[frametable.index((page, 0))]=(None, 0)

	def savecontext(A, PC, acc, V, page): #inner function to save the current context in PCB of process A for context switch
		A.offset=PC
		A.acc=acc
		A.V=V
		A.curr=page
		
	def memvarupdate(A, varname, newval, pageno): #inner fnc to update variables in memory when a 'STO' operation is encountered
		
		page=pmem[pageno]
		for ctr, ins in enumerate(page):
			if ins.split()[0]==varname:
				pmem[pageno][ctr]=ins.split()[0]+' '+str(newval)
		pmem[pageno].modified=1
		pmem[pageno].updateTS()
		

	Readyqueue=deque(processlist) #Ready queue stores the processes ready for execution

	'''newly added'''
	page_exec_seq=['']

	for process in Readyqueue:
		process.workingset=deque(maxlen=timeout)
	'''newly added'''
	Running=Readyqueue.popleft() #Running references the currently executing process
	Donequeue=deque() #Done queue stores the process which have completed execution

	#print('\n--------------------------------------\n')

	timer=0 #timer for managing interleaving

	acc, page, PC=0, 0, 0 #processor pointers
	faultcount=0 #stores the count of page faults
	accesscount=0 
	V=Running.V #current variable context

	t1=time.time()
	stopwatch=Timer()
	stopwatch.start()

	while True:

		timer+=1

		if Running==None and len(Readyqueue)==0: #nothing running and nothing waiting, execution finished
			break

		if(PC==pagesize): #reset PC and increment page pointer
			PC=0
			page+=1

		if (timer>timeout or Running==None) and len(Readyqueue)>0: #if timeout and there are more processes waiting...
			
				#if page not in pmem.keys():

					print()
					timer=1 #reset timer

					isswitch=False #store True if it is a switch between two executing processes, 
									#store False if resuming a process when the other has finished

					if Running!=None:
						isswitch=True
						'''newly added'''
						stopwatch.pause()
						print('SWITCHING PROCESS P{}'.format(Running.id), end=" ")
						stopwatch.resume()
						'''newly added'''

						savecontext(Running, PC, acc, V, page) #save the context of the current process in the process control block
						Readyqueue.append(Running) #move the process to ready queue

					Running=Readyqueue.popleft() #execute the next waiting process
					
					'''newly added'''
					stopwatch.pause()
					if isswitch:
						print("WITH P{}".format(Running.id))
					else: print("RESUMING PROCESS P{} (previous running process has finished)".format(Running.id))
					#time.sleep(0.3)
					stopwatch.resume()
					'''newly added'''
					
					
					V=Running.V #restore context for the newly switched process
					acc=Running.acc
					page=Running.curr
					PC=Running.offset

		elif timer>timeout: 
			print()
			timer=1

		'''newly added'''
		stopwatch.pause()
		print("| {0:^3d} |".format(timer), end="   ")
		stopwatch.resume()
		'''newly added'''

		if page not in pmem.keys():
			#time.sleep(0.1)
		
			'''newly added'''
			stopwatch.pause()
			print("PAGE FAULT", end=":   ")
			stopwatch.resume()
			'''newly added'''
		
			faultcount+=1
			accesscount+=1
			primaryload(Running, page)
			print()

		else: 
			accesscount+=1
			if algochoice==3: 
				#if page is in main memory, but used bit is 0, set used bit to 1
				if frametable.__contains__((page, 0)): frametable[frametable.index((page, 0))]=(page, 1)
		
		IR=pmem[page][PC].strip() #IR stores the current instruction

		if IR.upper()=='STP': 
			'''newly added'''
			stopwatch.pause()
			print("TERMINATING PROCESS P{} (and removing its pages from primary memory)".format(Running.id))
			stopwatch.resume()
			'''newly added'''
			primaryremove(Running)
			Donequeue.append(Running)
			Running=None
			#memdisplay()
			continue

		CMD=IR[:IR.index(' ')] #extract opcode from current instruction

		'''newly added'''
		page_exec_seq.append(page)
		try:
			Running.workingset.remove(page)	
		except: pass

		Running.workingset.append(page)
		stopwatch.pause()
		print("Resident set (P{}): {}".format(Running.id, Running.residentset))
		print("Working set: (P{}): {}".format(Running.id, Running.workingset))

		stopwatch.resume()
		'''newly added'''
		
		if algochoice==5:
			del opt_list[0]	
		pmem[page].updateTS()

		varname=IR[IR.index(' ')+1:len(IR)]

		if CMD.upper()=="LDA":
			acc=V[varname]  #memory operation

			'''Check if that page is in main memory:
				- if yes, no problem 
				- if no, page fault; get the page
			''' 

			in_main=False
			for i in Running.datalist:
				try:
					if varname in [ins.split()[0] for ins in pmem[i] if len(ins.split())>1]: 
						in_main=True
						break
				except:
					if varname in [ins.split()[0] for ins in smem[i] if len(ins.split())>1]: 
						break

			if not in_main:
				'''newly added'''
				stopwatch.pause()
				print("DATA PAGE FAULT", end=":   ")
				stopwatch.resume()
				'''newly added'''
				faultcount+=1	
				primaryload(Running, i, get_one=True) 
			if algochoice==5:
				del opt_list[0]	
			pmem[i].updateTS()

			'''newly added'''
			page_exec_seq.append(i)
			try:
				Running.workingset.remove(i)	
			except: pass

			Running.workingset.append(i)

			stopwatch.pause()
			print("Working set: (P{}): {}".format(Running.id, Running.workingset))

			stopwatch.resume()
			'''newly added'''

			if algochoice==3: 
				#if data page is in main memory, but used bit is 0, set used bit to 1
				if frametable.__contains__((i, 0)): frametable[frametable.index((i, 0))]=(i, 1)
			

		elif CMD.upper()=='STO':
			V[varname]=acc
			
			
			in_main=False
			for i in Running.datalist:
				try:
					if varname in [ins.split()[0] for ins in pmem[i] if len(ins.split())>1]: 
						in_main=True
						break
				except:
					if varname in [ins.split()[0] for ins in smem[i] if len(ins.split())>1]: 
						break
			if not in_main:
				'''newly added'''
				stopwatch.pause()
				print("DATA PAGE FAULT", end=":   ")
				stopwatch.resume()
				'''newly added'''
				faultcount+=1
				primaryload(Running, i, get_one=True) 
			
			if algochoice==5:
				del opt_list[0]	

			pmem[i].updateTS()

			'''newly added'''
			page_exec_seq.append(i)
			try:
				Running.workingset.remove(i)	
			except: pass

			Running.workingset.append(i)

			stopwatch.pause()
			print("Working set: (P{}): {}".format(Running.id, Running.workingset))

			stopwatch.resume()
			'''newly added'''

			if algochoice==3: 
				#if data page is in main memory, but used bit is 0, set used bit to 1
				if frametable.__contains__((i, 0)): frametable[frametable.index((i, 0))]=(i, 1)

			memvarupdate(Running, varname, acc, i) #memory operation, update value in the appropriate page in memory
		
		elif CMD.upper()=='ADD':
			acc+=V[varname] #ALU operation
			
		elif CMD.upper()=='SUB': 
			acc-=V[varname] #ALU operation
		
		elif CMD.upper()=='JNE':
			if acc!=0:
				temp=int(IR[IR.index(' ')+1:len(IR)])-1 
				page=(temp//pagesize)+Running.start #reload all the processor pointers
				PC=temp%pagesize
				Running.curr=page #set the process pointer
				continue

		elif CMD.upper()=='JGE':
			if acc>=0:
				temp=int(IR[IR.index(' ')+1:len(IR)])-1
				page=(temp//pagesize)+Running.start #reload all the processor pointers
				PC=temp%pagesize
				Running.curr=page #set the process pointer
				continue

		elif CMD.upper()=='JMP':
			temp=int(IR[IR.index(' ')+1:len(IR)])-1
			page=(temp//pagesize)+Running.start #reload all the processor pointers
			PC=temp%pagesize
			Running.curr=page #set the process pointer
			continue

		PC+=1
	t2=time.time()
	stopwatch.pause()

	'''newly added'''
	page_exec_seq=page_exec_seq[1:]
	'''newly added'''

	"""
	print('\n--------------------------------------\n')
	memdisplay()
	print('\n--------------------------------------\n')
	"""

	print(len(Donequeue), "PROCESSES COMPLETED EXECUTION.\n")

	print("TIME TAKEN:", (str(stopwatch)), "\n")

	print(faultcount, "PAGE FAULTS OUT OF", accesscount, "PAGE ACCESSES.\n")

	print("FINAL REGISTER/VARIABLE STATES:")
	for ctr, i in enumerate(processlist):
		'''newly added'''
		print("P{0}".format(i.id),"\t",{'ACC':i.acc}, sorted(i.V.items()))
		'''newly added'''
	

# -----------------------------------------------------------------------------------

if __name__=="__main__":

	pagesize=2 #fixed
	
	pmemsize=int(input("Enter the no. of physical memory page frames: ")) # -------- 1st input --------
	assert pmemsize>0, "Primary memory size must be a positive integer"

	pmem, smem=Memory(pmemsize), Memory(256) #creation of primary and secondary memory objects
	
	for x in range(pmemsize):
		frametable.append((None, 0))
	cptr=0


	processlist=[
	Process(open('cmd3.txt')),  Process(open('cmd2.txt')),
	]
								#processlist is a list of all the processes that are to be executed



	"""
	t=int(input("Enter the number of processes to run (maximum 4 for now): "))  # -------- 2nd input --------
	assert 1<=t<=4, "Invalid choice"

	This simulator can run any number of processes, 
	provided the programs are available 
	and have been written with MU0 instructions and are syntactically correct
	"""
	
	timeout=int(input("Enter timeout period (period after which a process is switched): ")) # -------- 3rd input --------
	assert timeout>0, "Timeout period must be a positive integer"

	algochoice=int(input("Choose replacement algorithm {}: ".format(repalgo)))
	assert 1<=algochoice<=5, "Invalid choice"
		
	if algochoice==5:
	    import opt_module
	    programlist=[x.name for x in processlist]
	    opt_list=opt_module.main(pmemsize, programlist, timeout)

	if algochoice!=3: #Clock algorithm works with demand paging only
	    pf_enable=1 if input("Enable prefetching [y/n]? ").lower() in ['y', 'ye', 'yes', 'yeah', 'yep'] else 0
	    
	    """
		An assumption will be made that all instructions 
	take only one processor cycle regardless of their nature.
		"""
	executeprocesses() #call the subroutine to execute required number of processes

# -----------------------------------------------------------------------------------





