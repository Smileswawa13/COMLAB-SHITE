/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package login;

import com.formdev.flatlaf.FlatDarkLaf;

public class Login {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        FlatDarkLaf.setup();
        new loginScreen().setVisible(true);
    }
    
}
