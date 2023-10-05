import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r'assets\adults_invoice_ytd_61323.xlsx')

#Working on Void Invoices
void_invoices = df[df['Invoice Status'] == 'Void']
invoice_summary = void_invoices.groupby('Customer Name').agg({'SubTotal' : 'sum' , 'PurchaseOrder' : 'nunique'})
invoice_summary.columns = ['Amount Lost', 'No. of Invoices']
invoice_summary_sort_amount = invoice_summary.sort_values('Amount Lost', ascending=False)
invoice_summary_sort_number = invoice_summary.sort_values('No. of Invoices', ascending=False)
# Plot the top 10 customers with most cancelled invoices
# top_10_customers = invoice_summary_sort_amount.head(10)
# fig, ax = plt.subplots(figsize=(10, 6))
# top_10_customers.plot(kind='bar', y='Amount Lost', legend=False, ax=ax)
# plt.xlabel('Customer Name', fontsize = 2)
# plt.ylabel('Amount Lost')
# plt.title('Top 10 Customers with Most Cancellations')
# plt.xticks(rotation=15)
# plt.show()
print(invoice_summary['Amount Lost'].sum())