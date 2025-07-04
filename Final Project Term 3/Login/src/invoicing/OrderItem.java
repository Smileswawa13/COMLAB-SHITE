package invoicing;

import java.math.BigDecimal;

/**
 * Data model for individual items in an order.
 */
public class OrderItem {
    private final String description;
    private final int quantity;
    private final BigDecimal unitPrice;

    public OrderItem(String description, int quantity, BigDecimal unitPrice) {
        this.description = description;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    public String getDescription() {
        return description;
    }

    public int getQuantity() {
        return quantity;
    }

    public BigDecimal getUnitPrice() {
        return unitPrice;
    }

    public BigDecimal getTotalPrice() {
        return unitPrice.multiply(new BigDecimal(quantity));
    }
}