from tkinter import *
from tkinter import filedialog
from view_audit_structure import compute_audit_structure, output_structure

class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)        
		self.master = master
		self.pack(fill=BOTH, expand=1)
		self.search_var = StringVar()
		self.search_var.trace('w', self.highlight_searched)

		openButton = Button(self, text="Open file", command=self.openProcessAndOutputFile)
		openButton.pack(fill=BOTH, expand=1)

		saveButton = Button(self, text="Save file", command=self.saveFile)
		saveButton.pack(fill=BOTH, expand=1)

		selectAllButton = Button(self, text="Select all", command=self.selectAll)
		selectAllButton.pack(fill=BOTH, expand=1)

		deselectAllButton = Button(self, text="Deselect all", command=self.deselectAll)
		deselectAllButton.pack(fill=BOTH, expand=1)
		
		inputBar = Entry(self, textvariable=self.search_var)
		inputBar.pack(fill=BOTH, expand=1)
		
		searchButton = Button(self, text="Search")
		searchButton.pack(fill=BOTH, expand=1, )

		self.output = Listbox(selectmode='multiple')
		self.output.pack(fill=BOTH, expand=1)

		self.initialContent = ''
		self.initialList = list()
		self.highlight_searched

	def highlight_searched(self, *args):
		search = self.search_var.get()
		self.output.delete(0, END)
		for item in self.initialList:
			if search.lower() in item.lower():
				self.output.insert(END, item)

	def selectAll(self):
		self.output.select_set(0, END)

	def deselectAll(self):
		self.output.selection_clear(0, END)
		
	def saveFile(self):

		if not self.initialContent:
			return
		
		file = filedialog.asksaveasfile(mode="w", filetypes = (("Audit files", "*.audit") ,("All files", "*.*")))

		if not file:
			return
		
		f = open(file.name, "w")
		f.write(self.initialContent)
		f.close()

	def openProcessAndOutputFile(self):
		file = filedialog.askopenfile(mode="r", filetypes = (("Audit files", "*.audit") ,("All files", "*.*")))

		if not file:
			return
		
		f = open(file.name, "r")
		self.initialContent = f.read()

		structure = compute_audit_structure(self.initialContent)

		form = '{}'

		customItemFlag = False
		for (_, _, text) in structure:
			if (text == "<custom_item>"):
				customItemFlag = True
				continue
			
			if (customItemFlag == True):
				self.output.insert(END, form.format(text))
				customItemFlag = False

		self.initialList = self.output.get(0, END)
			
root = Tk()
app = Window(root)
root.wm_title("Security Inspector")
root.geometry("500x500")
root.mainloop()