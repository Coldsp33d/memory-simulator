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
									python3 memsimv6.3.py
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

from collections import deque

import sys, copy, time, math, random

timer, pagesize, pf_enable, algochoice=0, 2, 0, -1
frametable, cptr=[], 0
opt_list=[]

la=[];lb=[]
pm=[]
pmrem=[]
pmremlist=[]
stat=[]
streg=[]
s=""
repalgo={1: 'FIFO', 2: 'Random', 3: 'Clock', 4: 'LRU', 5: 'Optimal (not practical)'}
pmemlist=[];pmm=[]
pmem, smem=None, None

Readyqueue=None

# -----------------------------------------------------------------------------------

class Page(list):		#model class for pages stored in virtual memory

	def __init__(self, instruction):
		super(Page, self).append(instruction)
		self.ts=time.time()
		self.fifots=self.ts

	def __str__(self, timestamp=False):
		if timestamp is not False:
			s=repr(self)+ '\t' + str(self.ts)
			'''newly added'''
			if hasattr(self, "modified"): 
				s+="\tM="+str(self.modified)
			return s
			'''newly added'''

		else: 
			'''newly added'''
			s=repr(self) 
			if hasattr(self, "modified"): 
				s+="\tM="+str(self.modified)
			return s
			'''newly added'''

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
			'''newly added'''
			if hasattr(self[page1], "modified") and self[page1].modified==1:
				self[page1].modified=0
				#print("Changing modified bit")
			'''newly added'''

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
		
		'''newly added'''
		self.datalist=[]
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
				'''newly added'''
				flag=0
				'''newly added'''

		'''newly added'''
		if flag==0: self.end=pagecount-1
		else: self.end=pagecount
		'''newly added'''

		self.datalist=list(sorted(set(self.datalist)))
		self.curr=self.start


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

				'''newly added'''
				if hasattr(pmem[k[0]], "modified"): print("\tM={}".format(pmem[k[0]].modified))
				'''newly added'''
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

	global frametable, cptr, Readyqueue
	pm_page_list=[]
	pm_swap_list=[]
	sm_swap_list=[]
	status=""

	""" ------- PREFETCHING DISABLED (MULTI-PAGE LOADING STILL SUPPORTED)------- """

	if pf_enable == 0 or get_one==True:
		'''newly added'''
		temp1, temp2=page, timer

		if len(pmem)<pmem.maxsize: #if there are free page frames in primary memory
			while True:
				if temp1 not in pmem.keys():
					print("| Moving", temp1, "to main memory |  ", end="")
					stat.append("MOVING"+" "+str(temp1)+" "+"TO PRIMARY MEMORY")
					pm.append(temp1)
					pmm.append(temp1)
					pmem.swap(smem, temp1, temp1)
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
			print("| Swapping", k, "and", page, end=" | ")
			stat.append("SWAPPING"+" "+str(k)+" AND "+str(page) )
			la.append(k)
			lb.append(page)
			pmem.swap(smem, k, page)
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
				print("| Moving", temp1, "to main memory |  ", end="")
				status=status+"MOVING"+" "+str(temp1)+" "+"TO PRIMARY MEMORY\n"
				pm_page_list.append(temp1)
				pmem.swap(smem, temp1, temp1)
				frametable[frametable.index((None, 0))]=(temp1, 1)
				pmem[temp1].updateFifoTS()
			swappedin.append(temp1)
			temp1+=1
			temp2+=pagesize
			
			if len(Readyqueue)>0 and (len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1) or temp2>timeout):
					break
			elif len(pmem)>=pmem.maxsize or temp1 not in range(A.start, A.end+1): 
					break
		stat.append(status)
		status=""
		pmm.append(pm_page_list)
		pm.append(pm_page_list)
		pm_page_list=[]		
				 	

	if len(pmem)==pmem.maxsize:
		L=getswaplist(swappedin)
		i=0
		while temp2<=timeout and len(L) > i: 
						#second condition will matter only for very small main memories
			if temp1 not in pmem.keys():
				print("| Swapping", L[i], "and", temp1, end=" | ")
				pmem.swap(smem, L[i], temp1)
				status=status+"SWAPPING"+" "+str(L[i])+" AND "+str(temp1) +"\n"
				pm_swap_list.append(L[i])
				sm_swap_list.append(temp1)
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
		stat.append(status)
		status=""
		la.append(pm_swap_list)
		pm_swap_list=[]	
		
		lb.append(sm_swap_list)
		sm_swap_list=[]	

# -----------------------------------------------------------------------------------

def executeprocesses(): #main method for executing the required number of processes
	global timer, Readyqueue,pmrem,pmm,s,opt_list
	a=""
	def primaryremove(A): #inner function to remove pages from a terminated process
		global pmrem
		for page in range(A.start, A.end+1):
			if page in pmem.keys():
				smem.swap(pmem, page, page)
				try:
					frametable[frametable.index((page, 1))]=(None, 0)
				except: 
					frametable[frametable.index((page, 0))]=(None, 0)
				pmrem.append(page)
		pmremlist.append(pmrem)
		pmrem=[]

	def savecontext(A, PC, acc, V, page): #inner function to save the current context in PCB of process A for context switch
		A.offset=PC
		A.acc=acc
		A.V=V
		A.curr=page
		
	def memvarupdate(A, varname, newval, pageno): #inner fnc to update variables in memory when a 'STO' operation is encountered
		'''newly added'''
		page=pmem[pageno]
		for ctr, ins in enumerate(page):
			if ins.split()[0].upper()==varname:
				pmem[pageno][ctr]=ins.split()[0]+' '+str(newval)
		pmem[pageno].modified=1
		pmem[pageno].updateTS()
		'''newly added'''
		s=''
		for k,v in A.V.items():
			s=s+str(k)+"  :  "+str(v)+ "\n"
		streg.append(s)
		stat.append(str(A.start)+" "+str(A.end+1)+" "+str(varname)+" "+str(newval))

	Readyqueue=deque(processlist) #Ready queue stores the processes ready for execution
	Running=Readyqueue.popleft() #Running references the currently executing process
	Donequeue=deque() #Done queue stores the process which have completed execution

	#print('\n--------------------------------------\n')

	timer=0 #timer for managing interleaving

	acc, page, PC=0, 0, 0 #processor pointers
	faultcount=0 #stores the count of page faults
	V=Running.V #current variable context
	    
	t1=time.time()
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
						tests='SWITCHING PROCESS P{}'.format(Running.id)
						print('SWITCHING PROCESS P{}'.format(Running.id), end=" ")
						savecontext(Running, PC, acc, V, page) #save the context of the current process in the process control block
						Readyqueue.append(Running) #move the process to ready queue

					Running=Readyqueue.popleft() #execute the next waiting process
					
					if isswitch:
						print("WITH P{}".format(Running.id))
						tests1=tests+" "+"WITH P{}".format(Running.id)
					else: 
						print("RESUMING PROCESS P{} (previous running process has finished)".format(Running.id))
						tests1="\tRESUMING PROCESS P{}\n(Previous running process has finished)".format(Running.id)
						#time.sleep(0.3)
					stat.append(tests1)
					V=Running.V #restore context for the newly switched process
					acc=Running.acc
					page=Running.curr
					PC=Running.offset

		elif timer>timeout: 
			print()
			timer=1

		print("| {0:^3d} |".format(timer), end="   ")
		if page not in pmem.keys():
			#time.sleep(0.1)
			print("PAGE FAULT", end=":   ")
			stat.append("PAGE FAULT")
			faultcount+=1
			primaryload(Running, page)
			print()

		else: 
			if algochoice==3: 
				#if page is in main memory, but used bit is 0, set used bit to 1
				if frametable.__contains__((page, 0)): frametable[frametable.index((page, 0))]=(page, 1)
		s1="EXECUTING "
		s1=s1+str(page)+ " "
		
		IR=pmem[page][PC].strip() #IR stores the current instruction
		s1=s1+pmem[page][PC]
		if IR.upper()=='STP': 
			print("TERMINATING PROCESS P{} (and removing its pages from primary memory)".format(Running.id))
			tests1="\tTERMINATING PROCESS P{}\n(and removing its pages from primary memory)".format(Running.id)
			pmemlist.append(pmm)
			pmm=[]
			primaryremove(Running)
			stat.append(tests1)
			Donequeue.append(Running)
			Running=None
			#memdisplay()
			continue
		
		
		CMD=IR[:IR.index(' ')] #extract opcode from current instruction
		
		stat.append(s1)
		if algochoice==5:
			del opt_list[0]	
		pmem[page].updateTS()

		varname=IR[IR.index(' ')+1:len(IR)]
		if CMD.upper()=="LDA":
			
			acc=V[varname]  #memory operation

			'''Check if that page is in main memory:
				- if yes, no problem 
				- if no, page fault; get the page''' 

			'''newly added'''
			in_main=False
			for i in Running.datalist:
				try:
					if varname in [ins.split()[0] for ins in pmem[i] if len(ins.split())>1]: 
						in_main=True
						break
				except:
					if varname in [ins.split()[0] for ins in smem[i] if len(ins.split())>1]: break

			if not in_main:

				print("DATA PAGE FAULT", end=":   ")
				stat.append("DATA PAGE FAULT")
				faultcount+=1	
				primaryload(Running, i) 
			if algochoice==5:
				del opt_list[0]	
			pmem[i].updateTS()

			if algochoice==3: 
				#if data page is in main memory, but used bit is 0, set used bit to 1
				if frametable.__contains__((i, 0)): frametable[frametable.index((i, 0))]=(i, 1)
			'''newly added'''

		elif CMD.upper()=='STO':
			V[varname]=acc
			
			'''newly added'''
			in_main=False
			for i in Running.datalist:
				try:
					if varname in [ins.split()[0] for ins in pmem[i] if len(ins.split())>1]: 
						in_main=True
						break
				except:
					if varname in [ins.split()[0] for ins in smem[i] if len(ins.split())>1]: break
			if not in_main:
				print("DATA PAGE FAULT", end=":   ")
				stat.append("DATA PAGE FAULT")
				faultcount+=1
				primaryload(Running, i) 

			if algochoice==5:
				
				del opt_list[0]	
			pmem[i].updateTS()

			if algochoice==3: 
				#if data page is in main memory, but used bit is 0, set used bit to 1
				if frametable.__contains__((i, 0)): frametable[frametable.index((i, 0))]=(i, 1)

			memvarupdate(Running, varname, acc, i) #memory operation, update value in the appropriate page in memory
			'''newly added'''

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
	
	"""
	print('\n--------------------------------------\n')
	memdisplay()
	print('\n--------------------------------------\n')
	"""

	print(len(Donequeue), "PROCESSES COMPLETED EXECUTION.\n")
	print("TIME TAKEN:", (t2-t1), "\n")
	print(faultcount, "PAGE FAULTS.\n")
	print("FINAL REGISTER/VARIABLE STATES:")
	for ctr, i in enumerate(processlist):
		print("P{0}".format(i.id),"\t",{'ACC':i.acc}, i.V)

	#print(len(Donequeue), "PROCESSES COMPLETED EXECUTION.\n")
	s=s+str(len(Donequeue))+ " "+"PROCESSES COMPLETED EXECUTION."+"\n"
	#print("TIME TAKEN:", (t2-t1), "\n")
	s=s+"TIME TAKEN:" +" " +str(t2-t1)+"\n"
	s=s+str(faultcount)+" PAGE FAULTS"+"\n" 
	#print("FINAL REGISTER/VARIABLE STATES:")
	s=s+"FINAL REGISTER/VARIABLE STATES:\n\n"
	for ctr, i in enumerate(processlist):
		for k,v in i.V.items():
			a=a+k+" : "  +str(v)+"\n"
		s=s+"P{0}".format(i.id)+"\n"+"ACC : "+str(i.acc)+"\n"+a+"\n"
		#print("P{0}".format(i.id),"\t",{'ACC':i.acc}, i.V)
		a=""
	

# -----------------------------------------------------------------------------------
def main(a,b,c,d,e):

	global pmem, smem, processlist, timeout, secmem, la, lb, frametable, cptr, algochoice,pf_enable,opt_list

	pmemsize=int(b)
	#pmemsize=int(input("Enter the no. of physical memory page frames: ")) # -------- 1st input --------
	assert pmemsize>0, "Primary memory size must be a positive integer"

	pmem, smem=Memory(pmemsize), Memory(128) #creation of primary and secondary memory objects
	
	#processlist=[Process(open('cmd.txt')), Process(open('cmd2.txt')), Process(open('cmd3.txt')), Process(open('cmd4.txt'))]
								#processlist is a list of all the processes that are to be executed

	for x in range(pmemsize):
		frametable.append((None, 0))
	cptr=0
	
	'''proglist=['cmd.txt','cmd2.txt','cmd3.txt','cmd4.txt']
	t=int(input("Enter the number of processes to run (maximum 4 for now): "))  # -------- 2nd input --------
	assert 1<=t<=4, "Number of processes must fall within range"
	proglist=proglist[:t]'''
	processlist=[]
	proglist=a
	for i in proglist:
		processlist.append(Process(open(i)))
	secmem=copy.deepcopy(dict(smem))
	"""
	This simulator can run any number of processes (not just 4), 
	provided the programs are available 
	and have been written with MU0 instructions which are syntactically correct
	"""
	timeout=int(c)
	#timeout=int(input("Enter timeout period (period after which a process is switched): ")) # -------- 3rd input --------
	assert timeout>0, "Timeout period must be a positive integer"

	#print() 
	'''for i in range(3, 0, -1):
		print('Starting in %d...\a\r'%i, end="")
		time.sleep(1)'''
	#print()

	'''algochoice=int(input("Choose replacement algorithm {}: ".format(repalgo)))
	assert 1<=algochoice<=4, "Invalid choice"'''
	algochoice=d
	if algochoice==5:
	    import opt_module
	    programlist=[x.name for x in processlist]
	    opt_list=opt_module.main(pmemsize, programlist, timeout)
	    

	if algochoice!=3: #Clock algorithm works with demand paging only
		#pf_enable=1 if input("Enable prefetching [y/n]? ").lower() in ['y', 'ye', 'yes'] else 0
		pf_enable=int(e)

		if pf_enable: 
				print('\n--------------------------------------\n')
				print('''An assumption will be made that all instructions 
	take only one processor cycle regardless of their nature.''')
				print('\n--------------------------------------\n')
	executeprocesses() #call the subroutine to execute required number of processes
	la=[x for x in la if x != []]
	lb=[x for x in lb if x != []]
	#print(pmemlist)
	#print(pm)
	#print(la)#,lb,pm,stat,streg)
	#print(stat)
	#print(streg)


if __name__=="__main__":

	pagesize=2 #fixed
	
	pmemsize=int(input("Enter the no. of physical memory page frames: ")) # -------- 1st input --------
	assert pmemsize>0, "Primary memory size must be a positive integer"

	pmem, smem=Memory(pmemsize), Memory(128) #creation of primary and secondary memory objects
	
	for x in range(pmemsize):
		frametable.append((None, 0))
	cptr=0

	processlist=[Process(open('cmd4.txt')), Process(open('cmd3.txt')), 
	#Process(open('cmd.txt')), Process(open('cmd2.txt'))
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





