package invoicing;

import java.util.List;

/**
 * Data model for a complete order.
 */
public class Order {
    private final String invoiceNumber;
    private final String customerName;
    private final List<OrderItem> items;

    public Order(String invoiceNumber, String customerName, List<OrderItem> items) {
        this.invoiceNumber = invoiceNumber;
        this.customerName = customerName;
        this.items = items;
    }

    public String getInvoiceNumber() {
        return invoiceNumber;
    }

    public String getCustomerName() {
        return customerName;
    }

    public List<OrderItem> getItems() {
        return items;
    }
}