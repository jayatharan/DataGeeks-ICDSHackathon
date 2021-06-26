from model import InvoiceTotalFinder
import os
import pandas as pd

invoiceTotalFinder = InvoiceTotalFinder()

folder_path = './img'
entries = sorted(os.listdir(folder_path))

invoice_totals = []
for entry in entries:
    invoiceTotalFinder.convert_img(folder_path+"/"+entry)
    invoice_totals.append(invoiceTotalFinder.get_total())


out = pd.DataFrame()
out['File Name'] = entries
out['total'] = invoice_totals
out.to_csv('TEST_output.csv', index=False)

print(out)
