/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.GuiProjectMain to edit this template
 */
package GuiProject;

import java.io.File;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

/**
 *
 * @author Admin
 */
public class GuiProjectMain {

    public static void main(String[] args) {
        String filepath = "ValveRemix.wav";
        Playmusic(filepath);
        new loginScreen().setVisible(true);

    }

    public static void Playmusic(String location) {
        try {
            File musicPath = new File(location);
            if (musicPath.exists()) {
                AudioInputStream audioInput = AudioSystem.getAudioInputStream(musicPath);
                Clip clip = AudioSystem.getClip();
                clip.open(audioInput);
                clip.start();

            } else {
                System.out.println("Cant Find File");
            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
