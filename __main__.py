from tkinter import *
import tkinter.messagebox
import copy, time, os
import memsimv64
import newgui
l=list()
nf=True
pfaultcount=0
paccesscount=0
colors=[]
tempres_set=""
tempwork_set=""
temp_var=False
tempvar_res_set=0
pgglobal=''
new_x=0
res_set_dict=dict()
if(newgui.f and newgui.sel==0):
	memsimv64.main(newgui.l, newgui.a, newgui.b, newgui.c, newgui.sel)
	no_of_proc=len(newgui.l)
	sa=memsimv64.la
	sb=memsimv64.lb
	pm=copy.deepcopy(memsimv64.pm)
	sm=memsimv64.secmem
	smm=copy.deepcopy(sm)
	stat=memsimv64.stat
	st=memsimv64.streg
	pg_seq_list=memsimv64.pg_seq_list[1][1:]
	res_set_list=memsimv64.res_set_list
	work_set_list=memsimv64.work_set_list
	pmrem=memsimv64.pmremlist
	pmemlist=memsimv64.pmemlist
	pmemlist=pmemlist[1:]
	p_start=memsimv64.proc_start
	p_end=memsimv64.proc_end
	for i in sm.keys():
		l.append(i)
	pmstatus=[0 for x in range(len(pm))]
	sumtot=0
	g=0
	p=0
	m=0
	f=True
	z=0
	x=0
	pp=""
	newstat=['P0']
	ctr=0
	v=[0 for x in range(2)]
	vm=[0 for x in range(2)]
elif(newgui.f and newgui.sel==1):
	l=list()
	memsimv64.main(newgui.l, newgui.a, newgui.b, newgui.c, newgui.sel)
	no_of_proc=len(newgui.l)
	sa=memsimv64.la
	sb=memsimv64.lb
	pg_seq_list=memsimv64.pg_seq_list[1][1:]
	res_set_list=memsimv64.res_set_list
	work_set_list=memsimv64.work_set_list
	pm=copy.deepcopy(memsimv64.pm)
	sm=memsimv64.secmem
	smm=copy.deepcopy(sm)
	stat=memsimv64.stat
	pmrem=memsimv64.pmremlist
	pmemlist=memsimv64.pmemlist
	pmemlist=pmemlist[1:]
	st=memsimv64.streg
	p_start=memsimv64.proc_start
	p_end=memsimv64.proc_end
	for i in sm.keys():
		l.append(i)
	stat=[x for x in stat if x != '']
	pmstatus=[0 for x in range(len(pm))]
	pm1  = [val for sublist in pm for val in sublist]
	pm1status=[0 for x in range(len(pm1))]
	g=0;ctr=0
	p=0
	m=0
	f=True
	z=0
	x=0
	xx=0
	pp=""
	newstat=['P0']
	loop_var=-1
	sumtot=0
	v=[0 for x in range(2)]
	vm=[0 for x in range(2)]

class App():
	def __init__(self, master, a, b):
		self.entries=[]
		self.entries1=[]
		self.labelsa=[0 for x in range(max(b, 128))]
		self.labelsc=[0 for x in range(max(b, 128))]
		self.labelsb=[]
		self.frame0 = Frame()
		self.frame1 = Frame()
		self.frame12 = Frame()
		self.frame2 = Frame()
		self.frame3 = Frame()
		self.frame4 = Frame()
		self.framesm2 = Frame()
		self.framesml2 = Frame()
		self.framesm3 = Frame()
		self.framesml3 = Frame()
		self.framesm4 = Frame()
		self.frame0.pack(side="top", padx=10)
		self.frame3.pack(side="left", padx=10) 
		self.frame1.pack(side="left", padx=10)
		self.frame12.pack(side="left", padx=10) 
		self.frame4.pack(side="left", padx=10) 
		self.frame2.pack(side="left")
		self.framesml2.pack(side="left", padx=10) 
		self.framesm2.pack(side="left")
		self.framesml3.pack(side="left", padx=10) 
		self.framesm3.pack(side="left")
		self.framesm4.pack(side="right", padx=20)

		self.ea=[0 for x in range(b)]
		self.eb=[0 for x in range(max(b, 128))]
		self.reset=Button(self.frame0, text="RESET", width=10, command=self.reset)
		self.reset.pack(side="left", padx=20)
		self.step=Button(self.frame0, text="STEP", width=10, repeatdelay=500, repeatinterval=100, command=self.load)
		self.step.pack(side="left", padx=20)
		self.run=Button(self.frame0, text="RUN", width=10, command=self.runmethod)
		self.run.pack(side="left", padx=20)
		self.pau=Button(self.frame0, text="PAUSE", width=10, command=self.pause)
		self.pau.pack(side="left", padx=20)
		self.exit=Button(self.frame0, text="EXIT", width=10, command=self.exit)
		self.exit.pack(side="left", padx=20)
	def start(self):
		global smm, sm, pp, p_start, p_end, colors
		sm=copy.deepcopy(smm)
		if(len(sm)>71):
			tkinter.messagebox.showinfo("OVERFLOW", "Memory Overflow")
			root.destroy()
			os.system("python3 __main__.py")
		for i in range(int(newgui.a)):
			k=i
			self.labelsb.append(Label(self.frame3, text = 'Frame '+ str(i), justify = LEFT).pack(pady=5))
			self.labelsc[k]=Label(self.frame12, text = "", justify = LEFT)
			self.ea[i]=Button(self.frame1, text="", width=15, bg="red", disabledforeground="white", state=DISABLED)
			self.ea[i].pack()
			self.labelsc[k].pack(pady=5)	
			self.entries.append(self.ea[i])

		for i in range(24):
			k=i
			if(k<len(sm)):
				self.labelsa[k]=Label(self.frame4, text = 'Page '+ str(k), justify = LEFT)	
				if(len(sm[k])==2):
					self.eb[i]=Button(self.frame2, text=sm[k][0]+ ", " + sm[k][1], width=15, disabledforeground="white", state=DISABLED)	
				else:
					self.eb[i]=Button(self.frame2, text=sm[k][0], width=15, disabledforeground="white", state=DISABLED)

				self.eb[i].pack()
				self.labelsa[k].pack(pady=5)	

				
			else:
				self.eb[i]=Button(self.frame2, text="", width=10)
			
			self.entries1.append(self.eb[i])
		b=k
		for i in range(24):
			k=b+i+1
			if(k<len(sm)):
				self.labelsa[k]=Label(self.framesml2, text = 'Page '+ str(k), justify = LEFT)
				if(len(sm[k])==2):
					self.eb[k]=Button(self.framesm2, text=sm[k][0]+ ", " + sm[k][1], width=15, disabledforeground="white", state=DISABLED)	
				else:
					self.eb[k]=Button(self.framesm2, text=sm[k][0], width=15, disabledforeground="white", state=DISABLED)
				self.eb[k].pack()
				self.labelsa[k].pack(pady=5)
			else:
				self.eb[k]=Button(self.frame2, text="", width=10)
			
			self.entries1.append(self.eb[k])
		b=k
		for i in range(24):
			k=b+i+1
			if(k<len(sm)):
				self.labelsa[k]=Label(self.framesml3, text = 'Page '+ str(k), justify = LEFT)
				if(len(sm[k])==2):
					self.eb[k]=Button(self.framesm3, text=sm[k][0]+ ", " + sm[k][1], width=15, disabledforeground="white", state=DISABLED)	
				else:
					self.eb[k]=Button(self.framesm3, text=sm[k][0], width=15, disabledforeground="white", state=DISABLED)
				self.eb[k].pack()
				self.labelsa[k].pack(pady=5)
			else:
				self.eb[k]=Button(self.frame2, text="", width=50)
			
			self.entries1.append(self.eb[k])
		self.proc=StringVar()
		pp='P0'
		self.proc.set(pp)
		self.labproc=Label(self.framesm4, textvariable = self.proc, justify = LEFT, relief=SUNKEN, width=35).pack()

		self.regvar=StringVar()
		self.labreg=Label(self.framesm4, textvariable = self.regvar, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.lab_res_label=Label(self.framesm4, text ="Resident Set", justify = LEFT, relief=SUNKEN, width=35).pack()
		self.res_set_var=StringVar()
		self.lab_res_set=Label(self.framesm4, textvariable = self.res_set_var, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.lab_res_label=Label(self.framesm4, text ="Working Set", justify = LEFT, relief=SUNKEN, width=35).pack()		
		self.work_set_var=StringVar()
		self.lab_work_set=Label(self.framesm4, textvariable = self.work_set_var, justify = LEFT, relief=SUNKEN, width=35).pack()		
		self.var=StringVar()
		self.lab=Label(self.framesm4, textvariable = self.var, justify = LEFT, relief=SUNKEN, width=35, height=5).pack()
		self.pcountvar=StringVar()
		self.pcount=Label(self.framesm4, textvariable = self.pcountvar, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.pacccountvar=StringVar()
		self.pacccount=Label(self.framesm4, textvariable = self.pacccountvar, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.lab_pgseq_lab=Label(self.framesm4, text ="Page Execution Sequence", justify = LEFT, relief=SUNKEN, width=35).pack()
		self.pgseqvar=StringVar()
		self.pgseq=Label(self.framesm4, textvariable = self.pgseqvar, justify = LEFT, relief=SUNKEN, width=35, height=20, wraplength=275).pack()

		sst=""
		for j in range(len(p_start)):


			if j%2==0:
				sst="green"
			else:
				sst="chocolate"
			colors.append(sst)
			for i in range(p_start[j], p_end[j]+1):
				self.eb[i].config(bg=sst)
		
	def load(self):
		global p, m, newstat, z, pp, v, ctr, sumtot, x, pfaultcount, p_start, p_end, colors, x, tempvar_res_set, temp_var, pgglobal, paccesscount, new_x, res_set_dict
		for i in range(int(newgui.a)):
			self.ea[i].configure(bg="red")
		try:
			if stat[m].split()[0]=='EXECUTING':
				
				self.ea[pm.index(int(stat[m].split()[1]))].configure(bg="black")
				if len(stat[m].split())<4:
					self.var.set("EXECUTING '"+stat[m].split()[2]+"' IN FRAME "+str(pm.index(int(stat[m].split()[1]))))		
				else:
					self.var.set("EXECUTING '"+stat[m].split()[2]+" "+stat[m].split()[3]+"' IN FRAME "+str(pm.index(int(stat[m].split()[1]))))
				if stat[m].split()[2].split()[0].lower()=='lda':
					self.work_set_var.set(str(work_set_list[x]))
					pgglobal=pgglobal+str(pg_seq_list[new_x])+' '+str(pg_seq_list[new_x+1])+' '
					self.pgseqvar.set(pgglobal)
					paccesscount+=2
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
					x+=1
					new_x+=2
					
				elif stat[m].split()[2].split()[0].lower()=='sto':
					self.work_set_var.set(str(work_set_list[x]))
					pgglobal=pgglobal+str(pg_seq_list[new_x])+' '+str(pg_seq_list[new_x+1])+' '
					self.pgseqvar.set(pgglobal)
					paccesscount+=2
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
					x+=1
					new_x+=2
				else:
					paccesscount+=1
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
					pgglobal=pgglobal+str(pg_seq_list[new_x])+' '
					self.pgseqvar.set(pgglobal)
					new_x+=1
				self.res_set_var.set(res_set_dict[pp])

			elif stat[m].split()[0]=="PAGE" or stat[m].split()[0]=="DATA":
				if stat[m].split()[0]=="DATA":
					temp_var=True
				if stat[m].split()[0]=="PAGE":
					paccesscount+=1	
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
				self.var.set(stat[m])
				pfaultcount+=1

				self.pcountvar.set("NUMBER OF PAGE FAULTS = "+str(pfaultcount))
			elif stat[m].split()[0]=="MOVING" or stat[m].split()[0]=="SWAPPING":
				a=pm[pmstatus.index(0, p)]
				if len(sm[a])<2:
					self.ea[pmstatus.index(0, p)].configure(text=sm[a][0])
				else:
					self.ea[pmstatus.index(0, p)].configure(text=sm[a][0]+", "+ sm[a][1])
				
				if stat[m].split()[0]=="MOVING":
					self.res_set_var.set(str(res_set_list[tempvar_res_set]))
					res_set_dict[pp]=str(res_set_list[tempvar_res_set])
					tempvar_res_set+=1
				self.eb[a].configure(bg="gray")

				self.labelsc[pmstatus.index(0, p)].configure(text="Page "+ str(a))
				self.ea[pmstatus.index(0, p)-1].configure(bg="red")
				pmstatus[pmstatus.index(0, p)]=1
				p+=1
				self.var.set(stat[m])

			elif stat[m].split()[0]=="SWITCHING" or stat[m].split()[0]=="RESUMING" or stat[m].split()[0]=="TERMINATING":
				newstat=stat[m].split()
				if newstat[0]=="SWITCHING":
					pp=newstat[len(newstat)-1]
					self.proc.set(pp)
					self.regvar.set(st[z])
					temp_var=True
					self.res_set_var.set('')


				elif newstat[0]=="RESUMING":
					pp=newstat[2]
					self.proc.set(pp)
					self.regvar.set(st[z])
					self.res_set_var.set(res_set_dict[pp])


				else:
					c=0
		
					if(ctr<(len(pmrem)-1)):
						if(ctr!=0):
							sumtot=sumtot+len(pmemlist[ctr-1])

						for i in pmrem[ctr]:
							self.ea[pm.index(i)].configure(text="")
							if len(sm[i])<2:
								self.eb[i].configure(text=sm[i][0])
							else:
								self.eb[i].configure(text=sm[i][0]+", "+ sm[i][1])
							for j in range(len(p_start)):
								if i>=p_start[j] and i<=p_end[j]:
									self.eb[i].configure(bg=colors[j])

							self.labelsa[i].configure(text="Page "+ str(i))
							self.labelsc[pm.index(i)].configure(text="")
							pmstatus[pm.index(i)]=0	

						for i in range(int(newgui.a)):
							if c<len(pmemlist[ctr]) and pmstatus[i]==0:
								if(ctr==0):
									pm[i]=pm[int(newgui.a)+c]
								else:

									pm[i]=pm[sumtot+int(newgui.a)+c]


								c+=1
						
						p=0
						ctr+=1
					elif ctr==(len(pmrem)-1):
						for i in pmrem[ctr]:
							self.ea[pm.index(i)].configure(text="")
							if len(sm[i])<2:
								self.eb[i].configure(text=sm[i][0])
							else:
								self.eb[i].configure(text=sm[i][0]+", "+ sm[i][1])
							for j in range(len(p_start)):
								if i>=p_start[j] and i<=p_end[j]:
									self.eb[i].configure(bg=colors[j])
							self.labelsa[i].configure(text="Page "+ str(i))
							self.labelsc[pm.index(i)].configure(text="")
				self.var.set(stat[m])
			else:
				s=stat[m].split()
				self.ea[p-1].configure(bg="red")
				for j in range(int(s[0]), min(int(s[1]), len(sm)-1)+1):
					if sm[j][0].split()[0]==s[2]:
						sm[j][0]=s[2]+" "+s[3]
						for h in range(int(newgui.a)):
							if self.labelsc[h]['text']=='Page '+str(j):
								break
						if len(sm[j])>1:
							v[1]=h
							
							self.ea[h].configure(text=sm[j][0]+", "+ sm[j][1], bg="blue")
						else:
							v[1]=h
							self.ea[h].configure(text=sm[j][0], bg="blue")
						self.ea[v[0]].configure(bg="red")
						v[0]=v[1]
					elif  len(sm[j])>1 and sm[j][1].split()[0]==s[2]:
						for h in range(int(newgui.a)):
							if self.labelsc[h]['text']=='Page '+str(j):
								break
						v[1]=h
						sm[j][1]=s[2]+" "+s[3]

						self.ea[h].configure(text=sm[j][0]+", "+ sm[j][1], bg="blue")

						v[0]=v[1]
				self.proc.set(pp)
				self.var.set("CHANGING VALUE OF VARIABLE {} IN {}".format(s[2], pp))
				self.regvar.set(st[z])


				z+=1	
			m+=1
		except:
			self.test()
		
	def test(self):
		global g, f, m, z, newstat, vm, p_start, p_end, colors, tempvar_res_set, res_set_dict, pp, no_of_proc, paccesscount
		try:
			
			if stat[m].split()[0]=="SWAPPING":
				a, b=sa[g], sb[g]
				if len(sm[b])<2:
					self.ea[pm.index(a)].configure(text=sm[b][0])
				else:
					self.ea[pm.index(a)].configure(text=sm[b][0]+", "+ sm[b][1])
				if len(sm[a])<2:
					self.eb[a].configure(text=sm[a][0])
				else:
					self.eb[a].configure(text=sm[a][0]+", "+ sm[a][1])
				for i in range(len(p_start)):
					if a>=p_start[i] and a<=p_end[i]:
						self.eb[a].configure(bg=colors[i])

				self.res_set_var.set(str(res_set_list[tempvar_res_set]))
				res_set_dict[pp]=str(res_set_list[tempvar_res_set])
				tempvar_res_set+=1
				self.eb[b].configure(bg="gray")
				self.labelsa[a].configure(text="Page "+str(a))

				self.labelsc[pm.index(a)].configure(text="Page "+ str(b))
				vm[1]=pm.index(a)
				pm[pm.index(a)]=b
				if(vm[0]!=vm[1]):
					self.ea[vm[0]].configure(bg="red")
				vm[0]=vm[1]
				self.var.set(stat[m])
				g=g+1
			elif stat[m].split()[0]=="SWITCHING" or stat[m].split()[0]=="RESUMING" :
				newstat=stat[m].split()
				if stat[m].split()[0]=="SWITCHING":
					pp=newstat[len(newstat)-1]
				elif stat[m].split()[0]=="RESUMING":
					pp=newstat[2]
				
				self.var.set(stat[m])
			else:
				s=stat[m].split()
				
				for j in range(int(s[0]), int(s[1])):
					
					if sm[j][0].split()[0]==s[2]:
						sm[j][0]=s[2]+" "+s[3]
						if len(sm[j])>1:
							self.eb[j].configure(text=sm[j][0]+", "+ sm[j][1])
						else:
							self.eb[j].configure(text=sm[j][0])
					elif  len(sm[j])>1 and sm[j][1].split()[0]==s[2]:
						sm[j][1]=s[2]+" "+s[3]
						self.eb[j].configure(text=sm[j][0]+", "+ sm[j][1])
				self.proc.set(pp)
				self.var.set("CHANGING VALUE OF VARIABLE {} IN {}".format(s[2], pp))
				self.regvar.set(st[z])
				z+=1	
			m+=1
		
		except IndexError:
			f=False
			paccesscount+=no_of_proc	
			self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
			tkinter.messagebox.showinfo("Final", memsimv64.s)
			self.var.set("Execution Complete")
	
	def exit(self):
		root.destroy()	

	def runmethod(self):
		global f, nf
		
		if f and nf:
			self.step.config(state="disabled")
			self.load()
			root.after(100, self.runmethod)
		nf=True
	
	def pause(self):
		global nf
		self.step.config(state="normal")
		nf=False
	
	def reset(self):
		global  g, p, m, z, pm, sa, sb, sm, smm, stat, st, pmrem, pmemlist, l, sumtot, pmstatus, f, pp, newstat, ctr, v, vm, nf
		global p_start, p_end, colors, tempvar_res_set, temp_var, x, pgglobal
		pgglobal=''
		temp_var=False
		x=0
		nf=False
		r=tkinter.messagebox.askquestion("Reset", "Do you want reset with different conditions?", icon='warning')
		
		global paccesscount, new_x, res_set_dict, no_of_proc, pfaultcount
		
		res_set_dict=dict()
		new_x=0
		paccesscount=0
		pfaultcount=0
		
		if r=='no':
			self.step.config(state="normal")
			l=[]
			colors=[]
			p_start=memsimv64.proc_start
			p_end=memsimv64.proc_end
			sa=memsimv64.la
			sb=memsimv64.lb
			pm=copy.deepcopy(memsimv64.pm)
			sm=memsimv64.secmem
			smm=copy.deepcopy(sm)
			stat=memsimv64.stat
			st=memsimv64.streg
			pmrem=memsimv64.pmremlist
			pmemlist=memsimv64.pmemlist
			pmemlist=pmemlist[1:]
			for i in sm.keys():
				l.append(i)
			pmstatus=[0 for x in range(len(pm))]
			sumtot=0
			g=0
			p=0
			m=0
			f=True
			z=0
			pp=""
			newstat=['P0']
			ctr=0
			tempvar_res_set=0
			v=[0 for x in range(2)]
			vm=[0 for x in range(2)]
			for i in self.frame1.winfo_children()+self.frame2.winfo_children()+self.frame3.winfo_children()+self.frame4.winfo_children()+self.framesm2.winfo_children()+self.framesml2.winfo_children()+self.framesm3.winfo_children()+self.framesml3.winfo_children()+self.framesm4.winfo_children()+self.frame12.winfo_children():
				i.destroy()
			self.start()
		
		else:
			root.destroy()
			os.system("python3 __main__.py")
			
class App1():
	def __init__(self, master, a, b):
		self.entries=[]
		self.entries1=[]
		self.labelsa=[0 for x in range(max(b, 128))]
		self.labelsc=[0 for x in range(max(b, 128))]
		self.labelsb=[]
		self.frame0 = Frame()
		self.frame1 = Frame()
		self.frame12 = Frame()
		self.frame2 = Frame()
		self.frame3 = Frame()
		self.frame4 = Frame()
		self.framesm2 = Frame()
		self.framesml2 = Frame()
		self.framesm3 = Frame()
		self.framesml3 = Frame()
		self.framesm4 = Frame()
		self.frame0.pack(side="top", padx=10)
		self.frame3.pack(side="left", padx=10) 
		self.frame1.pack(side="left", padx=10)
		self.frame12.pack(side="left", padx=10) 
		self.frame4.pack(side="left", padx=10) 
		self.frame2.pack(side="left")
		self.framesml2.pack(side="left", padx=10) 
		self.framesm2.pack(side="left")
		self.framesml3.pack(side="left", padx=10) 
		self.framesm3.pack(side="left")
		self.framesm4.pack(side="right", padx=20)

		self.ea=[0 for x in range(b)]
		self.eb=[0 for x in range(max(b, 128))]
		self.reset=Button(self.frame0, text="RESET", width=10, command=self.reset)
		self.reset.pack(side="left", padx=20)
		self.step=Button(self.frame0, text="STEP", width=10, repeatdelay=500, repeatinterval=100, command=self.load)
		self.step.pack(side="left", padx=20)
		self.run=Button(self.frame0, text="RUN", width=10, command=self.runmethod)
		self.run.pack(side="left", padx=20)
		self.pau=Button(self.frame0, text="PAUSE", width=10, command=self.pause)
		self.pau.pack(side="left", padx=20)
		self.exit=Button(self.frame0, text="EXIT", width=10, command=self.exit)
		self.exit.pack(side="left", padx=20)

	def start(self):
		global smm, sm, pp
		sm=copy.deepcopy(smm)
		if(len(sm)>71):
			tkinter.messagebox.showinfo("OVERFLOW", "Memory Overflow")
			root.destroy()
			os.system("python3 __main__.py")
		for i in range(int(newgui.a)):
			k=i
			self.labelsb.append(Label(self.frame3, text = 'Frame '+ str(i), justify = LEFT).pack(pady=5))
			self.labelsc[k]=Label(self.frame12, text = "", justify = LEFT)
			self.ea[i]=Button(self.frame1, text="", width=15, bg="red", disabledforeground="white", state=DISABLED)
			self.ea[i].pack()
			self.labelsc[k].pack(pady=5)	
			self.entries.append(self.ea[i])

		for i in range(24):
			k=i
			if(k<len(sm)):
				self.labelsa[k]=Label(self.frame4, text = 'Page '+ str(k), justify = LEFT)	
				if(len(sm[k])==2):
					self.eb[i]=Button(self.frame2, text=sm[k][0]+ ", " + sm[k][1], width=15, bg="green", disabledforeground="white", state=DISABLED)	
				else:
					self.eb[i]=Button(self.frame2, text=sm[k][0], width=15, bg="green", disabledforeground="white", state=DISABLED)

				self.eb[i].pack()
				self.labelsa[k].pack(pady=5)	

				
			else:
				self.eb[i]=Button(self.frame2, text="", width=10)
			
			self.entries1.append(self.eb[i])
		b=k
		for i in range(24):
			k=b+i+1
			if(k<len(sm)):
				self.labelsa[k]=Label(self.framesml2, text = 'Page '+ str(k), justify = LEFT)
				if(len(sm[k])==2):
					self.eb[k]=Button(self.framesm2, text=sm[k][0]+ ", " + sm[k][1], width=15, bg="green", disabledforeground="white", state=DISABLED)	
				else:
					self.eb[k]=Button(self.framesm2, text=sm[k][0], width=15, bg="green", disabledforeground="white", state=DISABLED)
				self.eb[k].pack()
				self.labelsa[k].pack(pady=5)
			else:
				self.eb[k]=Button(self.frame2, text="", width=10)
			
			self.entries1.append(self.eb[k])
		b=k
		for i in range(24):
			k=b+i+1
			if(k<len(sm)):
				self.labelsa[k]=Label(self.framesml3, text = 'Page '+ str(k), justify = LEFT)
				if(len(sm[k])==2):
					self.eb[k]=Button(self.framesm3, text=sm[k][0]+ ", " + sm[k][1], width=15, bg="green", disabledforeground="white", state=DISABLED)	
				else:
					self.eb[k]=Button(self.framesm3, text=sm[k][0], width=15, bg="green", disabledforeground="white", state=DISABLED)
				self.eb[k].pack()
				self.labelsa[k].pack(pady=5)
			else:
				self.eb[k]=Button(self.frame2, text="", width=50)
			
			self.entries1.append(self.eb[k])
		self.proc=StringVar()
		pp='P0'
		self.proc.set(pp)
		self.labproc=Label(self.framesm4, textvariable = self.proc, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.regvar=StringVar()
		self.labreg=Label(self.framesm4, textvariable = self.regvar, justify = LEFT, relief=SUNKEN, width=35).pack()
		
		self.lab_res_label=Label(self.framesm4, text ="Resident Set", justify = LEFT, relief=SUNKEN, width=35).pack()
		self.res_set_var=StringVar()
		self.lab_res_set=Label(self.framesm4, textvariable = self.res_set_var, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.lab_res_label=Label(self.framesm4, text ="Working Set", justify = LEFT, relief=SUNKEN, width=35).pack()		
		self.work_set_var=StringVar()
		self.lab_work_set=Label(self.framesm4, textvariable = self.work_set_var, justify = LEFT, relief=SUNKEN, width=35).pack()		
		self.var=StringVar()
		self.lab=Label(self.framesm4, textvariable = self.var, justify = LEFT, relief=SUNKEN, width=35, height=5).pack()
		self.pcountvar=StringVar()
		self.pcount=Label(self.framesm4, textvariable = self.pcountvar, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.pacccountvar=StringVar()
		self.pacccount=Label(self.framesm4, textvariable = self.pacccountvar, justify = LEFT, relief=SUNKEN, width=35).pack()
		self.lab_pgseq_lab=Label(self.framesm4, text ="Page Execution Sequence", justify = LEFT, relief=SUNKEN, width=35).pack()
		self.pgseqvar=StringVar()
		self.pgseq=Label(self.framesm4, textvariable = self.pgseqvar, justify = LEFT, relief=SUNKEN, width=35, height=20, wraplength=275).pack()

		sst=""
		for j in range(len(p_start)):
			if j%2==0:
				sst="green"
			else:
				sst="chocolate"
			colors.append(sst)
			for i in range(p_start[j], p_end[j]+1):
				self.eb[i].config(bg=sst)
		
	def load(self):
		global p, m, newstat, z, pp, v, loop_var, ctr, sumtot, pfaultcount, p_start, p_end, colors, tempvar_res_set, temp_var, xx, pgglobal, paccesscount, new_x, res_set_dict
		for i in range(int(newgui.a)):
			self.ea[i].configure(bg="red")
		try:
			if stat[m].split()[0]=='EXECUTING':
				self.ea[pm1.index(int(stat[m].split()[1]))].configure(bg="black")
				if len(stat[m].split())<4:
					self.var.set("EXECUTING '"+stat[m].split()[2]+"' IN FRAME "+str(pm1.index(int(stat[m].split()[1]))))		
				else:
					self.var.set("EXECUTING '"+stat[m].split()[2]+" "+stat[m].split()[3]+"' IN FRAME "+str(pm1.index(int(stat[m].split()[1]))))
				if stat[m].split()[2].split()[0].lower()=='lda':
					self.work_set_var.set(str(work_set_list[xx]))
					pgglobal=pgglobal+str(pg_seq_list[new_x])+' '+str(pg_seq_list[new_x+1])+' '
					self.pgseqvar.set(pgglobal)
					paccesscount+=2
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
					xx+=1
					new_x+=2
					
				elif stat[m].split()[2].split()[0].lower()=='sto':
					self.work_set_var.set(str(work_set_list[xx]))
					pgglobal=pgglobal+str(pg_seq_list[new_x])+' '+str(pg_seq_list[new_x+1])+' '
					self.pgseqvar.set(pgglobal)
					paccesscount+=2
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
					xx+=1
					new_x+=2
				else:
					paccesscount+=1
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
					pgglobal=pgglobal+str(pg_seq_list[new_x])+' '
					self.pgseqvar.set(pgglobal)
					new_x+=1
				m+=1
			elif stat[m].split()[0]=="PAGE" or stat[m].split()[0]=="DATA":
				if stat[m].split()[0]=="DATA":
					temp_var=True
				if stat[m].split()[0]=="PAGE":
					paccesscount+=1	
					self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
				self.var.set(stat[m])
				pfaultcount+=1
				self.pcountvar.set("NUMBER OF PAGE FAULTS = "+str(pfaultcount))
				m+=1
			elif stat[m].split()[0]=="MOVING" or stat[m].split()[0]=="SWAPPING":

				if stat[m].split()[0]=="MOVING":
					i=0
					a=pm[p]
					while(i<len(pm[p])):
						a=pm1[pm1status.index(0, p)]
						if(len(sm[a])<2):
							self.ea[pm1status.index(0, p)].configure(text=sm[a][0])
						else:
							self.ea[pm1status.index(0, p)].configure(text=sm[a][0]+", "+ sm[a][1])


						self.eb[a].configure(bg="gray")
						self.labelsc[pm1status.index(0, p)].configure(text="Page "+ str(a))
						self.ea[pm1status.index(0, p)-1].configure(bg="red")

						pm1status[pm1status.index(0, p)]=1
						i=i+1
					self.res_set_var.set(str(res_set_list[tempvar_res_set]))
					res_set_dict[pp]=str(res_set_list[tempvar_res_set])
					tempvar_res_set+=1
					pmstatus[pmstatus.index(0, p)]=1	
					loop_var=loop_var-1	
					p+=1
					self.var.set(stat[m])
					m+=1
				else:
					self.test()

			elif stat[m].split()[0]=="SWITCHING" or stat[m].split()[0]=="RESUMING" or stat[m].split()[0]=="TERMINATING":
				newstat=stat[m].split()
				if newstat[0]=="SWITCHING":
					pp=newstat[len(newstat)-1]
					self.proc.set(pp)
					self.regvar.set(st[z])
					self.res_set_var.set('')
				elif newstat[0]=="RESUMING":
					pp=newstat[2]
					self.proc.set(pp)
					self.regvar.set(st[z])
					self.res_set_var.set(res_set_dict[pp])
				else:
					c=0

					if(ctr<(len(pmrem)-1)):
						if(ctr!=0):
							tlist=[val for sublist in pmemlist[ctr-1] for val in sublist]

							sumtot=sumtot+len(tlist)
						for i in pmrem[ctr]:
							self.ea[pm1.index(i)].configure(text="")
							if(len(sm[i])<2):
								self.eb[i].configure(text=sm[i][0])
							else:
								self.eb[i].configure(text=sm[i][0]+", "+ sm[i][1])
							for j in range(len(p_start)):
								if i>=p_start[j] and i<=p_end[j]:
									self.eb[i].configure(bg=colors[j])

							self.labelsa[i].configure(text="Page "+ str(i))
							self.labelsc[pm1.index(i)].configure(text="")
							pm1status[pm1.index(i)]=0
						tempmlist=[val for sublist in pmemlist[ctr] for val in sublist]
						for i in range(int(newgui.a)):
							if c<len(tempmlist) and pm1status[i]==0:
								if(ctr==0):
									pm1[i]=pm1[int(newgui.a)+c]
								else:

									pm1[i]=pm1[sumtot+int(newgui.a)+c]


								c+=1
						p=0
						pmlength=[]
						for i in pmemlist[ctr]:
							pmlength.append(len(i))

						ctr+=1
						x=0
						sums=0
						loop_var=-1
					
						for i in range(len(pmlength)):
							sums=sums+pmlength[i]
							pm[i]=pm1[x:sums]
							x+=pmlength[i]						

					elif ctr==(len(pmrem)-1):
						for i in range(int(newgui.a)):
							if(len(self.labelsc[i]["text"].split())>0):
								nx=int(self.labelsc[i]["text"].split()[1])
								self.ea[i].configure(text="")
								if(len(sm[nx])<2):
									self.eb[nx].configure(text=sm[nx][0])
								else:
									self.eb[nx].configure(text=sm[nx][0]+", "+ sm[nx][1])
								for j in range(len(p_start)):
									if nx>=p_start[j] and nx<=p_end[j]:
										self.eb[nx].configure(bg=colors[j])

								self.labelsa[nx].configure(text="Page "+ str(nx))
								self.labelsc[i].configure(text="")
				self.var.set(stat[m])
				m+=1
			else:
				s=stat[m].split()
				self.ea[p-1].configure(bg="red")
				for j in range(int(s[0]), min(int(s[1]), len(sm)-1)+1):
					
					if sm[j][0].split()[0]==s[2]:
						sm[j][0]=s[2]+" "+s[3]
						for h in range(int(newgui.a)):
							if self.labelsc[h]['text']=='Page '+str(j):
								break
						if len(sm[j])>1:
							v[1]=h
							
							self.ea[h].configure(text=sm[j][0]+", "+ sm[j][1], bg="blue")
						else:
							v[1]=h
							self.ea[h].configure(text=sm[j][0], bg="blue")
						self.ea[v[0]].configure(bg="red")
						v[0]=v[1]
					elif  len(sm[j])>1 and sm[j][1].split()[0]==s[2]:
						for h in range(int(newgui.a)):
							if self.labelsc[h]['text']=='Page '+str(j):
								break
						v[1]=h
						sm[j][1]=s[2]+" "+s[3]
						self.ea[h].configure(text=sm[j][0]+", "+ sm[j][1], bg="blue")
						v[0]=v[1]
				self.proc.set(pp)
				self.var.set("CHANGING VALUE OF VARIABLE {} IN {}".format(s[2], pp))
				self.regvar.set(st[z])
				z+=1	
				m+=1
		except IndexError:
			self.test()
		
	def test(self):
		global g, f, m, z, newstat, vm, tempvar_res_set, x, res_set_dict, pp, no_of_proc, paccesscount
		swaplista=[];swaplistb=[]
		try:
			i=0
			if stat[m].split()[0]=="SWAPPING":
				while(i<len(sa[g]) and i<len(sb[g])):
					a, b=sa[g][i], sb[g][i]
					swaplista.append(a)
					swaplistb.append(b)
					if(len(sm[b])<2):
						self.ea[pm1.index(a)].configure(text=sm[b][0])
					else:
						self.ea[pm1.index(a)].configure(text=sm[b][0]+", "+ sm[b][1])

					if(len(sm[a])<2):
						self.eb[a].configure(text=sm[a][0])
					else:
						self.eb[a].configure(text=sm[a][0]+", "+ sm[a][1])
					for k in range(len(p_start)):
						if a>=p_start[k] and a<=p_end[k]:
							self.eb[a].configure(bg=colors[k])
					self.eb[b].configure(bg="gray")


					self.labelsa[a].configure(text="Page "+str(a))

					self.labelsc[pm1.index(a)].configure(text="Page "+ str(b))
					vm[1]=pm1.index(a)
					pm1[pm1.index(a)]=b

					if(vm[0]!=vm[1]):
						self.ea[vm[0]].configure(bg="red")
					vm[0]=vm[1]
					i+=1

				tempvar_res_set+=1
				self.res_set_var.set(str(res_set_list[tempvar_res_set]))
				res_set_dict[pp]=str(res_set_list[tempvar_res_set])
				
				self.var.set(stat[m])
				g=g+1
				
			elif stat[m].split()[0]=="SWITCHING" or stat[m].split()[0]=="RESUMING":
				newstat=stat[m].split()
				if stat[m].split()[0]=="SWITCHING":
					pp=newstat[len(newstat)-1]
				elif stat[m].split()[0]=="RESUMING":
					pp=newstat[2]
				
				self.var.set(stat[m])
			else:
				s=stat[m].split()
				
				for j in range(int(s[0]), int(s[1])):
					
					if sm[j][0].split()[0]==s[2]:
						sm[j][0]=s[2]+" "+s[3]
						if len(sm[j])>1:
							self.eb[j].configure(text=sm[j][0]+", "+ sm[j][1])
						else:
							self.eb[j].configure(text=sm[j][0])
					elif  len(sm[j])>1 and sm[j][1].split()[0]==s[2]:
						sm[j][1]=s[2]+" "+s[3]
						self.eb[j].configure(text=sm[j][0]+", "+ sm[j][1])
				self.proc.set(pp)
				self.var.set("CHANGING VALUE OF VARIABLE {} IN {}".format(s[2], pp))
				self.regvar.set(st[z])
				z+=1	
			m+=1
		except 	IndexError:
			f=False
			paccesscount+=no_of_proc	
			self.pacccountvar.set("NUMBER OF PAGE ACCESSES = "+str(paccesscount))
			tkinter.messagebox.showinfo("Final", memsimv64.s)
			self.var.set("Execution Complete")
	def exit(self):
		root.destroy()	

	def runmethod(self):
		global f, nf
		
		if f and nf:
			self.step.config(state="disabled")
			self.load()
			root.after(100, self.runmethod)
		nf=True
	def pause(self):
		global nf
		self.step.config(state="normal")
		nf=False
	def reset(self):
		global g, p, m, z, pm, ctr, pm1, pm1status, sumtot, sa, sb, sm, smm, stat, pmrem, pmemlist, st, l
		global stat, pmstatus, ctr, f, pp, newstat, loop_var, sumtot, v, vm, nf	
		global colors, p_start, p_end, tempvar_res_set, temp_var, xx, pgglobal
		tempvar_res_set=0
		pgglobal=''
		temp_var=False
		xx=0
		nf=False
		global paccesscount, new_x, res_set_dict, pfaultcount, no_of_proc
		pfaultcount=0
		res_set_dict=dict()
		new_x=0
		paccesscount=0
		r=tkinter.messagebox.askquestion("Reset", "Do you want reset with different conditions?", icon='warning')
		if r=='no':
			self.step.config(state="normal")
			l=[]
			colors=[]
			p_start=memsimv64.proc_start
			p_end=memsimv64.proc_end
			sa=memsimv64.la
			sb=memsimv64.lb
			pm=copy.deepcopy(memsimv64.pm)
			sm=memsimv64.secmem
			smm=copy.deepcopy(sm)
			stat=memsimv64.stat
			pmrem=memsimv64.pmremlist
			pmemlist=memsimv64.pmemlist
			pmemlist=pmemlist[1:]
			st=memsimv64.streg
			for i in sm.keys():
				l.append(i)
			stat=[x for x in stat if x != '']
			pmstatus=[0 for x in range(len(pm))]
			pm1  = [val for sublist in pm for val in sublist]
			pm1status=[0 for x in range(len(pm1))]
			g=0;ctr=0
			p=0
			m=0
			f=True
			z=0
			pp=""
			newstat=['P0']
			loop_var=-1
			sumtot=0
			v=[0 for x in range(2)]
			vm=[0 for x in range(2)]
			for i in self.frame1.winfo_children()+self.frame2.winfo_children()+self.frame3.winfo_children()+self.frame4.winfo_children()+self.framesm2.winfo_children()+self.framesml2.winfo_children()+self.framesm3.winfo_children()+self.framesml3.winfo_children()+self.framesm4.winfo_children()+self.frame12.winfo_children():
				i.destroy()
			self.start()
		else:
			root.destroy()
			os.system("python3 __main__.py")

if(newgui.f and newgui.sel==0):
	root=Tk()
	root.wm_title("Memory Simulator")
	root.geometry('{}x{}'.format(1600, 1600))
	app = App(root, 2, int(newgui.a))
	app.start()
	root.mainloop()

elif(newgui.f and newgui.sel==1):
	root=Tk()
	root.wm_title("Memory Simulator")
	root.geometry('{}x{}'.format(1600, 1600))
	app = App1(root, 2, int(newgui.a))
	app.start()
	root.mainloop()
