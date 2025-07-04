package invoicing;

import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Cell;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.properties.TextAlignment;
import com.itextpdf.layout.properties.UnitValue;

import java.io.File;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

public class InvoiceGenerator {

    /**
     * Creates a PDF invoice and returns the path to the generated file.
     * @return The absolute path of the created PDF file.
     * @throws IOException If an I/O error occurs.
     */
    public static String createPdfInvoice() throws IOException {
        // 1. Prepare hardcoded data
        List<OrderItem> items = Arrays.asList(
            new OrderItem("Ergonomic Keyboard", 1, new BigDecimal("75.00")),
            new OrderItem("Gaming Mouse", 1, new BigDecimal("45.50")),
            new OrderItem("USB-C Cable 2m", 2, new BigDecimal("12.00"))
        );
        Order order = new Order("MMCM-2025-789", "Ice", items);

        // 2. Define the output folder and filename
        String outputFolder = "invoices";
        File folder = new File(outputFolder);
        if (!folder.exists()) {
            folder.mkdirs();
        }
        File pdfFile = new File(String.format("%s/%s_%s.pdf", outputFolder, order.getCustomerName(), order.getInvoiceNumber()));
        String filePath = pdfFile.getAbsolutePath();

        // 3. Generate the PDF document
        try (PdfWriter writer = new PdfWriter(filePath);
             PdfDocument pdfDoc = new PdfDocument(writer);
             Document document = new Document(pdfDoc)) {

            document.add(new Paragraph("INVOICE").setFontSize(22).setTextAlignment(TextAlignment.CENTER));
            document.add(new Paragraph("Customer: " + order.getCustomerName()).setMarginTop(20));
            document.add(new Paragraph("Invoice #: " + order.getInvoiceNumber()));
            document.add(new Paragraph("\n"));

            Table table = new Table(UnitValue.createPercentArray(new float[]{50, 15, 20, 20})).useAllAvailableWidth();
            table.addHeaderCell(new Cell().add(new Paragraph("Item Description")));
            table.addHeaderCell(new Cell().add(new Paragraph("Qty").setTextAlignment(TextAlignment.CENTER)));
            table.addHeaderCell(new Cell().add(new Paragraph("Unit Price").setTextAlignment(TextAlignment.RIGHT)));
            table.addHeaderCell(new Cell().add(new Paragraph("Total").setTextAlignment(TextAlignment.RIGHT)));

            BigDecimal grandTotal = BigDecimal.ZERO;
            for (OrderItem item : order.getItems()) {
                table.addCell(new Cell().add(new Paragraph(item.getDescription())));
                table.addCell(new Cell().add(new Paragraph(String.valueOf(item.getQuantity())).setTextAlignment(TextAlignment.CENTER)));
                table.addCell(new Cell().add(new Paragraph(String.format("$%.2f", item.getUnitPrice())).setTextAlignment(TextAlignment.RIGHT)));
                BigDecimal total = item.getTotalPrice();
                table.addCell(new Cell().add(new Paragraph(String.format("$%.2f", total)).setTextAlignment(TextAlignment.RIGHT)));
                grandTotal = grandTotal.add(total);
            }
            document.add(table);

            document.add(new Paragraph("Grand Total: " + String.format("$%.2f", grandTotal))
                    .setFontSize(14).setTextAlignment(TextAlignment.RIGHT).setMarginTop(10));

            System.out.println("PDF Invoice created successfully at: " + filePath);
        }
        
        // Return the path to the created file
        return filePath;
    }
}