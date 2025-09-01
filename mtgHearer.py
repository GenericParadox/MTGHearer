import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading
import time

deck_file = "deck.txt"
r = sr.Recognizer()

class VoiceDeckApp:
    def __init__(self, master):
        self.master = master
        master.title("Voice MTG Deck Builder")

        # Text area
        self.text_area = tk.Text(master, height=4, width=40, font=("Helvetica", 16))
        self.text_area.pack(pady=10)
        self.text_area.insert(tk.END, "Press 'Capture' or 'C' to record a card.\n")
        self.text_area.config(state=tk.DISABLED)

        # Buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.capture_button = tk.Button(button_frame, text="Capture", command=self.capture_card)
        self.capture_button.grid(row=0, column=0, padx=5)

        self.confirm_button = tk.Button(button_frame, text="Confirm", command=self.confirm_card)
        self.confirm_button.grid(row=0, column=1, padx=5)

        self.retry_button = tk.Button(button_frame, text="Retry", command=self.retry_card)
        self.retry_button.grid(row=0, column=2, padx=5)

        self.quit_button = tk.Button(button_frame, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=0, column=3, padx=5)

        self.captured_card = None
        self.rapid_fire_running = False

        # Key bindings
        master.bind("<c>", lambda e: self.capture_card())
        master.bind("<Return>", lambda e: self.confirm_card())
        master.bind("<r>", lambda e: self.retry_card())
        master.bind("<q>", lambda e: self.master.quit())
         # Rapid-fire key binding
        master.bind("<KeyPress-f>", lambda e: self.start_rapid_fire())
        master.bind("<KeyRelease-f>", lambda e: self.stop_rapid_fire())



    def update_text(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, message)
        self.text_area.config(state=tk.DISABLED)

    def capture_card(self):
        threading.Thread(target=self._capture_card_thread).start()

    def _capture_card_thread(self):
        self.update_text("Recording for 3 seconds...")
        time.sleep(0.1)  # tiny delay to update UI
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, phrase_time_limit=3)
            self.captured_card = r.recognize_google(audio)
            self.update_text(f"Captured card:\n{self.captured_card}\nPress 'Confirm' or Enter to save, 'Retry' or R to redo.")
        except sr.UnknownValueError:
            self.captured_card = None
            self.update_text("Could not understand audio. Press 'Retry' or R to try again.")
        except sr.RequestError as e:
            self.captured_card = None
            self.update_text(f"Request failed; {e}")

    def confirm_card(self):
        if self.captured_card:
            with open(deck_file, "a", encoding="utf-8") as f:
                f.write(f"1x {self.captured_card}\n")
            self.update_text(f"Added '{self.captured_card}' to {deck_file}\nPress 'Capture' or 'C' for next card.")
            self.captured_card = None
        else:
            self.update_text("No card to confirm. Press 'Capture' or 'C' to try again.")

    def retry_card(self):
        self.captured_card = None
        self.update_text("Retrying. Press 'Capture' or 'C' to record a card again.")

    def start_rapid_fire(self):
        if not self.rapid_fire_running:
            self.rapid_fire_running = True
            threading.Thread(target=self._rapid_fire_thread).start()
            self.update_text("Rapid-fire mode ON. Hold F and start speaking cards!")

    def stop_rapid_fire(self):
        if self.rapid_fire_running:
            self.rapid_fire_running = False
            self.update_text("Rapid-fire mode OFF. Press 'Capture' or 'C' to continue normal capture.")

    def _rapid_fire_thread(self):
        while self.rapid_fire_running:
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r.listen(source, phrase_time_limit=2)

                card_name = r.recognize_google(audio)
                with open(deck_file, "a", encoding="utf-8") as f:
                    f.write(f"1x {card_name}\n")
                self.update_text(f"Rapid-fire added: {card_name}")

            except sr.UnknownValueError:
                self.update_text("Rapid-fire: could not understand audio, keep speaking...")
            except sr.RequestError as e:
                self.update_text(f"Rapid-fire request failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceDeckApp(root)
    root.mainloop()
"""Example Import Text:
1x Banishing Light (scd) 9 [Sideboard,Removal]
2x Battle Sliver (m14) 128 [Sliver]
1x Behold the Beyond (soi) 101 [Tutor]
2x Blur Sliver (cmm) 873 [Sliver]
1x Burnished Hart (cmm) 373 [Sideboard,Ramp]
1x Cho-Manno, Revolutionary (10e) 12 [Protection]
1x Day's Undoing (cmm) 85 [Sideboard,Draw]
1x Diffusion Sliver (cmm) 845 [Sliver]
1x Dragonlord Kolaghan (dtk) 218 [Creature]
1x Dragonlord Ojutai (ncc) 337 [Creature]
1x Dreamstone Hedron (cmm) 945 [Ramp]
1x Forest (mh3) 308 [Land]
1x Fusion Elemental (dmc) 150 [Sideboard,Creature]
1x Galerider Sliver (cmm) 849 [Sliver]
1x Gift of Immortality (ths) 14 [Recursion]
1x Goblin Bombardment (mh2) 279 [Recursion]
1x Grand Arbiter Augustin IV (2x2) 221 [Ramp]
1x Groundshaker Sliver (m14) 177 [Sliver]
1x Haven of the Spirit Dragon (scd) 304 [Land]
1x Heroes' Podium (dmc) 185 [Draw]
1x Hixus, Prison Warden (ori) 19 [Removal]
1x Horde of Notions (mm2) 178 [Sideboard]
1x Ink-Eyes, Servant of Oni (plst) BOK-71 [Creature]
1x Island (mh3) 305 [Land]
1x Jace Beleren (cmm) 850 [Draw]
1x Jungle Hollow (mom) 270 [Land]
1x Kamahl, Pit Fighter (dds) 39 [Creature]
1x Kazandu Refuge (scd) 307 [Land]
1x Kiora, the Crashing Wave (ddo) 34 *F* [Draw]
1x Kolaghan, the Storm's Fury (c17) 176 [Creature]
1x Manaweft Sliver (cmm) 900 [Sliver]
1x Mardu Banner (ktk) 224 [Ramp]
1x Mountain (blb) 274 [Land]
1x Narset Transcendent (dtk) 225 [Draw]
1x Negate (mom) 68 [Sideboard,Removal]
1x Neutralizing Blast (frf) 44 [Sideboard,Instant]
1x Nicol Bolas, Planeswalker (e01) 85 [Removal]
1x Obzedat, Ghost Council (mm3) 176 [Creature]
4x Opaline Unicorn (cn2) 213 [Ramp]
1x Pariah (plst) 10E-33 [Protection]
1x Plains (mh3) 304 [Land]
1x Polukranos, World Eater (plst) THS-172 [Removal]
4x Predatory Sliver (m14) 189 [Sliver]
2x Rugged Highlands (mom) 271 [Land]
1x Sentinel Sliver (cmm) 835 [Sliver]
1x Serra Avatar (dmr) 26 [Creature]
1x Shu Yun, the Silent Tempest (frf) 52 [Creature]
1x Sliver Hive (m15) 247 [Land]
1x Soul Tithe (rtr) 23 [Sideboard,Removal]
1x Spinal Embrace (dmr) 201 [Removal]
1x Statute of Denial (m15) 79 [Sideboard,Instant]
1x Steelform Sliver (m14) 38 [Sliver]
1x Striking Sliver (cmm) 882 [Sliver]
1x Sun Titan (mkc) 87 [Recursion]
1x Swamp (mh3) 306 [Land]
2x Swiftwater Cliffs (mom) 273 [Land]
1x Temple of Malice (scd) 326 [Land]
1x Thraximundar (2x2) 287 [Removal]
1x Tibalt, the Fiend-Blooded (ddk) 41 *F* [Draw]
1x Tranquil Cove (mom) 275 [Land]
3x Transguild Promenade (cmr) 499 [Land]
1x Vraska the Unseen (c19) 207 [Removal]
2x Wind-Scarred Crag (mom) 276 [Land]
1x Xenagos, the Reveler (clb) 853 [Ramp]
"""
