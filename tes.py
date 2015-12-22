from tkinter import *
from tkinter.dialog import Dialog


class OldDialogDemo(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master=master
		Pack.config(self)  # same as self.pack()
		ans = Dialog(self,
	                     title   = 'Memory Simulator',
	                     text    = 'Select your option',
	                     bitmap  = 'questhead',
	                     default = 0, strings = ('Load from file', 'Enter code in console', 'Cancel'))
		if ans.num == 0:
			import newgui
		elif ans.num == 1:
			self.createWidgets(master)
	def make_tb(self, frame):
		self.text=Text(frame, height=12, bd=2, font='Verdana 20')
		self.vsb=Scrollbar(frame, orient="vertical", command=self.text.yview)
		self.hsb=Scrollbar(frame, orient="horizontal", command=self.text.xview)
		self.text.configure(yscrollcommand=self.vsb.set)
		self.text.configure(xscrollcommand=self.hsb.set)
		self.vsb.pack(side="right", fill="y", padx=(0, 10), ipady=5)
		self.hsb.pack(side="bottom", fill="x", pady=(0, 10))
		self.text.pack(side="left", fill="both", padx=2, pady=10, expand=True)

	def createWidgets(self, master):
		self.mframe=Frame(master, width=1000, height=1000, )
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

		self.cont=Button(frame2, text="CONTINUE", command=self.start)
		self.cont.pack(ipadx=10, ipady=10, expand=1, side=TOP)

		self.quit=Button(bottomframe, text="QUIT", bg="red", fg="white", command=master.destroy)
		self.quit.pack(fill=Y, expand=1, side=RIGHT  )
		self.text.see("1.0")
	def start(self):
		pl=self.text.get("1.0", END).strip()
		print(pl)


root=Tk()
app=OldDialogDemo(master=root)
app.mainloop()
