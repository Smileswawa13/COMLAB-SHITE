package invoicing;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.swing.JPanel;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.rendering.PDFRenderer;

/**
 * A JPanel that displays the first page of a PDF file.
 */
public class InvoiceDisplayPanel extends JPanel {

    private BufferedImage bufferedImage;

    public void loadPdf(String filePath) throws IOException {
        try (PDDocument document = PDDocument.load(new File(filePath))) {
            PDFRenderer renderer = new PDFRenderer(document);
            // Render the first page (index 0)
            this.bufferedImage = renderer.renderImageWithDPI(0, 96); // 96 DPI
            // The panel needs to be repainted to show the new image
            this.repaint();
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (bufferedImage != null) {
            // Center the image in the panel
            int x = (this.getWidth() - bufferedImage.getWidth()) / 2;
            int y = (this.getHeight() - bufferedImage.getHeight()) / 2;
            g.drawImage(bufferedImage, x, y, this);
        }
    }
}