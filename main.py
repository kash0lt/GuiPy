from tkinter import *

root = Tk()

# Creating a label widget
myLabel = Label(root, text="Hello World!")
# Adding the label to the screen
myLabel.grid(row=0, column=0)

# Now we need the event loop 'mainloop' for the root 'screen'
root.mainloop()
