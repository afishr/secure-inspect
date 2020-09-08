from tkinter import *
from tkinter import filedialog
from view_audit_structure import compute_audit_structure, output_structure

class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)        
		self.master = master
		self.pack(fill=BOTH, expand=1)

		openButton = Button(self, text="Open file", command=self.openProcessAndOutputFile)
		openButton.grid(column=1)

		saveButton = Button(self, text="Save file", command=self.saveFile)
		saveButton.grid(column=1)

		self.output = Text()
		self.output.pack(fill=BOTH, expand=1)

		self.initialContent = ''

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

		self.output.config(state=NORMAL)

		customItemFlag = False
		for (_, _, text) in structure:
			if (text == "<custom_item>"):
				customItemFlag = True
				continue
			
			if (customItemFlag == True):
				self.output.insert(END, form.format(text))
				self.output.insert(END, '\n')
				customItemFlag = False

		self.output.config(state=DISABLED)
			
root = Tk()
app = Window(root)
root.wm_title("Security Inspector")
root.geometry("500x500")
root.mainloop()