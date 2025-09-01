import speech_recognition as sr

deck_file = "deck.txt"
r = sr.Recognizer()

print("Voice deck builder started!")
print("Press 'c' to say a card, 'q' to quit.")

while True:
    key = input("Press 'c' to speak a card, 'q' to quit: ").lower()

    if key == 'c':
        with sr.Microphone() as source:
            print("Listening... say the card name clearly.")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        try:
            card_name = r.recognize_google(audio)
            print("You said:", card_name)

            # Append to file in Archidekt-friendly format
            with open(deck_file, "a", encoding="utf-8") as f:
                f.write(f"1x {card_name}\n")

            print(f"Added '{card_name}' to {deck_file}")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    elif key == 'q':
        print("Final deck saved to", deck_file)
        break
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
