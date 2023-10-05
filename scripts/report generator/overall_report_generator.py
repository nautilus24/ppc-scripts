import pandas as pd
import matplotlib.pyplot as plt
from items_script import df_invoice_to_customer

# Read the extracted data file
# extracted_df = pd.read_excel('extracted_data.xlsx')

# Calculate the total invoice amount for each customer
customer_invoice_amount = df_invoice_to_customer.groupby('Customer')['Cost Without Freight'].sum().sort_values(ascending=False)

# Calculate the number of orders for each customer
customer_order_count = df_invoice_to_customer['Customer'].value_counts().sort_values(ascending=False)

# Top 20 customers with the highest invoice amount
top_20_customers_invoice = customer_invoice_amount.head(20)

# Top 10 customers with the highest order count
top_20_customers_order = customer_order_count.head(20)

# Create figure and axes for subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 8))

# Plot top 20 customers by invoice amount
axs[0].barh(top_20_customers_invoice.index, top_20_customers_invoice.values)
axs[0].set_title('Top 20 Customers by Invoice Amount')
axs[0].set_xlabel('Invoice Amount')
axs[0].set_ylabel('Customer')
axs[0].invert_yaxis()

# Plot top 10 customers by order count
axs[1].barh(top_20_customers_order.index, top_20_customers_order.values)
axs[1].set_title('Top 20 Customers by Order Count')
axs[1].set_xlabel('Order Count')
axs[1].set_ylabel('Customer')
axs[1].invert_yaxis()

# Adjust spacing between subplots
plt.subplots_adjust(wspace=0.5)

# Display the plots
plt.show()
