package invoicing;

import javax.swing.SwingUtilities;

/**
 * The main entry point to run the application.
 */
public class RunApplication {

    public static void main(String[] args) {
        // Ensure the UI is created on the Event Dispatch Thread
        SwingUtilities.invokeLater(() -> {
            new MainFrame().setVisible(true);
        });
    }
}