from tkinter import *
from tkinter import filedialog
from tkinter.dialog import Dialog
import tkinter.messagebox

i=40
j=0
a="";b="";sel=0
l=[]
f=False
tru=False
parse=""

class Mem():

	def __init__(self, master, choice):
		self.master=master
		self.entered_number = 0
		self.li=[]
		self.lj=[]
		self.e3=[0 for x in range(10)]
		self.e4=[0 for x in range(11)]
		self.chvar = IntVar()
		master.geometry("800x600+300+100")
		self.fra=Frame(master, width=800, height=600)
		self.fra.grid(rowspan=100, columnspan=100)
		if choice==0:
			self.broButton =Button(master, text = 'Browse', width = 6, command=self.browse_file)
			self.broButton.grid(row=40, column=29)
			self.arrow = PhotoImage(file='dd.png')
			self.x = PhotoImage(file='x.png')
		self.one=Label(master, text="Choose the no. of physical memory page frames")
		self.two=Label(master, text="Enter timeout period (period after which a process is switched)")
		self.three=Label(master, text="Enable Prefetching?")
		vcmd = master.register(self.validate)

		self.e2=Entry(master, validate="key", validatecommand=(vcmd, '%P'))
		self.lst1 = ['4', '8', '16']
		self.lst2 = ['First-In-First-Out (FIFO) (Worst)', 'Random Replacement', 'Clock (do not enable prefetching)', 'Least Recently Used (LRU) (Practically Best)', 'Optimal (Theoretically Best)']
		self.var1 = StringVar()
		self.var1.set("Choose your option")
		self.var2 = StringVar()
		self.var2.set("Choose your replacement algorithm")
		self.e1 = OptionMenu(master, self.var1, *self.lst1)
		self.e5 = OptionMenu(master, self.var2, *self.lst2, command=self.rep_algo)

		self.e1.config(width=15)
		self.e5.config(width=28)
		self.one.grid(row=61, column=29)
		self.e1.grid(row=61, column=30)
		self.two.grid(row=62, column=29)
		self.e2.grid(row=62, column=30)
		self.e5.grid(row=63, column=30)
		self.but =Button(master, text = 'Submit', width = 6, command=self.on_button)
		self.but.grid(row=70, column=30)

	def rep_algo(self, value):
		self.var = IntVar()
		if(value!='Clock'):
			
			self.rb = Radiobutton(self.master, text="Yes", variable=self.var, value=1)
			self.rb1 = Radiobutton(self.master, text="No", variable=self.var, value=2)
			self.rb.grid(row=64, column=30)
			self.rb1.grid(row=65, column=30)
			self.three.grid(row=64, column=29, rowspan=2)
		else:
			self.var.set(0)
			try:
				self.rb.grid_forget()
				self.rb1.grid_forget()
				self.three.grid_forget()
			except:
				print(end="")

	def on_button(self):
		global a, b, f, sel, c
		a=self.var1.get()
		b=self.e2.get()
		c=self.lst2.index(self.var2.get())+1
		if(self.var.get()==1):
			sel = 1
		else:
			sel=0
		print(a, b, c, sel)
		self.master.destroy()	
		f=True

	def browse_file(self):
		global i, j
		fname = filedialog.askopenfilename()
		if(len(fname)!=0):
			l.append(fname)
			a=fname.split('/')
			self.e3[j]=Label(root, text=a[len(a)-1], relief=SUNKEN, width=25)
			self.e3[j].grid(row=i, column=30)
			self.e4[j]=Button(image=self.x, command=lambda x=j, y=i: self.delete(x, y))
			self.e4[j].grid(row=i, column=31)
			self.li.append(i)
			self.lj.append(j)
			i=i+1;j=j+1

	def delete(self, k, m):
		global i, j
		self.e3[k].destroy()
		self.e4[k].destroy()
		self.e3[k]=self.e3[k+1]
		self.e4[k]=self.e4[k+1]
		if(type(self.e3[k]) is int):
			i=i-1
			j=j-1
			k=k-1
		else:
			print(type(self.e3[k]))
			self.e3[k].grid(row=m, column=30)
			self.e4[k].grid(row=m, column=31)
		l.remove(l[k])

	def validate(self, new_text):
		if not new_text: # the field is being cleared
			self.entered_number = 0
			return True

		try:
			if(int(new_text)<=int(self.var1.get())):
				self.entered_number = int(new_text)
				return True
			else:
				return False
		except ValueError:
			return False

class OldDialogDemo(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master=master
		Pack.config(self)  # same as self.pack()
		self.ans = Dialog(self, 
	                     title   = 'Memory Simulator', 
	                     text    = 'Select your option', 
	                     bitmap  = 'questhead',
 
	                     default = 0, strings = ('Load from file', 'Enter code in console', 'Cancel'))


		if self.ans.num == 1:
			master.geometry("1600x1000")
			self.createWidgets(master)


	def make_tb(self, frame):
		self.text=Text(frame, height=12, bd=2, font='Courier 20', undo=True)
		self.vsb=Scrollbar(frame, orient="vertical", command=self.text.yview)
		self.hsb=Scrollbar(frame, orient="horizontal", command=self.text.xview)
		self.text.configure(yscrollcommand=self.vsb.set)
		self.text.configure(xscrollcommand=self.hsb.set)
		self.vsb.pack(side="right", fill="y", padx=(0, 10), ipady=5)
		self.hsb.pack(side="bottom", fill="x", pady=(0, 10))
		self.text.pack(side="left", fill="both", padx=2, pady=10, expand=True)


	def createWidgets(self, master):
		self.mframe=Frame(master, width=200, height=400 )
		self.mframe.pack(padx=(10, 0), ipadx=15, ipady=0)
		frame=Frame(self.mframe)
		frame.pack(side=TOP)
		frame2=Frame(self.mframe, bd=2)
		frame2.pack(padx=20, ipadx=10)

		bottomframe=Frame(self.mframe, bd=2)
		bottomframe.pack(side=BOTTOM, fill=BOTH, pady=5, expand=1)

		self.head=Label(frame, text="Enter the code and click on 'Continue'", font='size: 15', fg="black")
		self.head.pack(padx=10, pady=(10, 0))
	
		self.make_tb(frame)
		self.lab=Label(frame2, text="ERROR STATUS", width=800, relief=SUNKEN)
		self.lab.pack(ipadx=10, ipady=10, expand=1, side=TOP)
		self.errvar=StringVar()
		self.errlabel=Label(frame2, textvariable=self.errvar, width=800, height=3, relief=SUNKEN)
		self.errlabel.pack(ipadx=10, ipady=10, expand=1, side=TOP)
		self.comp=Button(frame2, text="COMPILE", command=self.compile_method)
		self.comp.pack(ipadx=10, ipady=10, expand=1, side=LEFT)
		self.cont=Button(frame2, text="CONTINUE", state="disabled", command=self.start)
		self.cont.pack(ipadx=10, ipady=10, expand=1, side=LEFT)
		self.clear=Button(frame2, text="CLEAR SCREEN", command=self.dele)
		self.clear.pack(ipadx=10, ipady=10, expand=1, side=LEFT)
		self.how_to=Button(frame2, text="HELP", command=self.help)
		self.how_to.pack(ipadx=10, ipady=10, expand=1, side=LEFT)
		self.quit=Button(frame2, text="EXIT", bg="red", fg="white", command=master.destroy)
		self.quit.pack(ipadx=10, ipady=10, expand=1, side=LEFT  )
		self.text.see("1.0")

	def compile_method(self):
		global l, tru
		parse=self.text.get("1.0", END).strip()
		self.errvar.set('')
		self.text.edit_reset()
		import MU0gen
		MU0gen.main(parse)

		if MU0gen.syn_error==False:
			self.cont.config(state="normal")
			tru=True
			self.errvar.set(MU0gen.err)
			MU0gen.err=''
			l=[]
			l.append('test.txt')
			
		else:

			self.cont.config(state="disabled")
			self.errvar.set(MU0gen.err)
			MU0gen.err=''
			MU0gen.syn_error=False
			tru=False

	def start(self):
		global tru
		if tru:
			self.master.destroy()
			root=Tk()
			root.wm_title("Memory Simulator")
			app=Mem(master=root, choice=1)

	def help(self):
		x=open("howto.txt", "r")
		s=""
		self.window = Toplevel(root)
		self.window.geometry("800x600+300+100")
		self.ok=Button(self.window, text="OK", command=self.window.destroy)
		self.ok.pack(side="bottom")
		for i in x.readlines():
			s=s+i
		self.text=Text(self.window, height=12, bd=2, font='arial 10 bold', undo=True)
		self.text.insert("1.0", s)
		self.text.config(state=DISABLED, bg="light gray")
		self.vsb=Scrollbar(self.window, orient="vertical", command=self.text.yview)
		self.text.configure(yscrollcommand=self.vsb.set)
		self.text.configure(xscrollcommand=self.hsb.set)
		self.vsb.pack(side="right", fill="y", padx=(0, 10), ipady=5)
		self.text.pack(side="left", fill="both", padx=2, pady=10, expand=True)

	def dele(self):
		self.errvar.set('')
		self.text.delete("1.0", END)
		self.cont.config(state="disabled")
			
root=Tk()
root.wm_title("Memory Simulator")

app=OldDialogDemo(master=root)
if app.ans.num==0:
	app.destroy()
	app = Mem(root, app.ans.num)
elif app.ans.num==2:
	root.destroy()

	

root.mainloop()
