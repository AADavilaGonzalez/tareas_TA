
if __name__=="__main__":
    import tkinter as tk

    root = tk.Tk()
    dpi = root.winfo_fpixels("1i")
    root.geometry("320x200")
    root.title = "Testing"

    sqrlabel = tk.Label(root, text=f"dpi:{dpi}", bd=2, relief="solid")
    sqrlabel.pack(padx=10,pady=10)

    root.mainloop()