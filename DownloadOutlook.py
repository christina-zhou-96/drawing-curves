from win32com.client import Dispatch
import datetime as date
import os.path

outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder("6")
all_inbox = inbox.Items
val_date = date.date.today()

for msg in all_inbox:
    print(msg)

