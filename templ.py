def view_employees(self):
    conn, cursor = self.connect_to_database()
    cursor.execute("SELECT * FROM Employees")
    results = cursor.fetchall()
    conn.close()

    self.display_results(results)


def display_results(self, results):
    top_level = Tk()
    top_level.title("Database Results")
    top_level.geometry("800x600")

    tree = ttk.Treeview(top_level)
    tree.pack(expand=True, fill='both')

    tree['columns'] = [i for i in range(len(results[0]))]
    tree.column("#0", width=0, stretch='NO')

    for i in range(len(results[0])):
        tree.column(i, anchor='w', width=100)
        tree.heading(i, text="Column " + str(i), anchor='w')

    for row in results:
        tree.insert('', 'end', text="", values=row)

    top_level.mainloop()