from model import InvoiceTotalFinder
import os
import pandas as pd

invoiceTotalFinder = InvoiceTotalFinder()

folder_path = './evaluation-set'
entries = sorted(os.listdir(folder_path))

grand_total = 0
invoice_totals = []
for entry in entries:
    invoiceTotalFinder.convert_img(folder_path+"/"+entry)
    ttl = invoiceTotalFinder.get_total()
    invoice_totals.append(ttl)
    grand_total += ttl

invoice_totals.append(grand_total)
entries.append("Grand Total")
out = pd.DataFrame()
out['File Name'] = entries
out['total'] = invoice_totals
out.to_csv('EVALUATION_output.csv', index=False)

print(out)
