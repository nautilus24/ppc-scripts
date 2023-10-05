import pandas as pd
import matplotlib.pyplot as plt
from items_script import df_invoice_to_customer

# Filter the data for rows where Invoice Status is "Closed"
closed_invoices = df_invoice_to_customer[df_invoice_to_customer['Invoice Status'] == 'Closed']

# Calculate the total invoice amount for each customer with closed invoices
customer_invoice_amount_closed = closed_invoices.groupby('Customer')['Cost Without Freight'].sum().sort_values(ascending=False)

# Calculate the number of orders for each customer with closed invoices
customer_order_count_closed = closed_invoices['Customer'].value_counts().sort_values(ascending=False)

# Top 20 customers with the highest invoice amount for closed invoices
top_20_customers_invoice_closed = customer_invoice_amount_closed.head(20)

# Top 10 customers with the highest order count for closed invoices
top_20_customers_order_closed = customer_order_count_closed.head(20)

# Create figure and axes for subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 8))

# Plot top 20 customers by invoice amount for closed invoices
axs[0].barh(top_20_customers_invoice_closed.index, top_20_customers_invoice_closed.values)
axs[0].set_title('Top 20 Customers by Invoice Amount (Closed Invoices)')
axs[0].set_xlabel('Invoice Amount')
axs[0].set_ylabel('Customer')
axs[0].invert_yaxis()

# Plot top 10 customers by order count for closed invoices
axs[1].barh(top_20_customers_order_closed.index, top_20_customers_order_closed.values)
axs[1].set_title('Top 20 Customers by Order Count (Closed Invoices)')
axs[1].set_xlabel('Order Count')
axs[1].set_ylabel('Customer')
axs[1].invert_yaxis()

# Adjust spacing between subplots
plt.subplots_adjust(wspace=0.5)

# Display the plots
plt.show()
