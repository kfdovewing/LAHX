import tkinter as tk

root = tk.Tk()
root.geometry("500x300")
root.title("Shop")

money = tk.IntVar(root, value = 100)

funds = tk.Label(root, text ="funds: $" + str(money.get()))
funds.grid(row = 0, column = 0, padx=5, pady=5)

def buy_item(items, index_list, i, total):
    index = index_list[i]
    cost = items[index]
    if total.get() - cost <0:
        invalid = tk.Label(root, text = "Not enough money!")
        invalid.grid(row = 2, column = 0, padx=5, pady=5)
        invalid.after(2000, invalid.destroy)

def update_money(items, index_list, i, total):
    cost = items[index_list[i]]
    return total.get()-cost

def update_display(total, btn):
    funds.config(text = "funds: $" + str(total.get()))
    btn.config(text = "SOLD OUT")

def update(index_list, i, btn):
    buy_item(items, index_list, i, money)
    money.set(update_money(items, index_list, i, money))
    update_display(money, btn)


    

def list_items(items):
    index_list = list(items.keys())
    for i in range(len(items)):
        btn = tk.Button(root, text = index_list[i] + " : $" + str(items[index_list[i]]))
        btn.config(command = lambda i=i, btn = btn : update(index_list, i, btn))
        row, col = divmod(i, 4)
        btn.grid(row = row+1, column = col, padx=5, pady=5)

items = {
    "free gift" : 0,
    "item 1" : 10,
    "item 2" : 20,
    "item 3" : 30
}
list_items(items)



root.mainloop()