import sys

import sqlite3
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import pygame
import time
from buttons_bar import button_sur


while True:

    cap = cv2.VideoCapture(0)
    scanned = False
    while not scanned:
        _, frame = cap.read()
        for code in decode(frame):
            data = code.data.decode('utf-8')
            scanned = True

            conn = sqlite3.connect('table_mint_2.db')
            cursor = conn.cursor()
            cursor.execute("SELECT number, sur, w_c, w_s, vin FROM list_2 WHERE user_id = ?", (data,))
            res = cursor.fetchone()

            def window_info(a):
                pygame.init()
                width, height = 600, 400
                screen = pygame.display.set_mode((width, height))
                image = pygame.image.load(a)
                screen.blit(image, (0, 0))
                pygame.display.flip()
                time.sleep(2)
                pygame.quit()

            if res:
                if res[1] == "+":
                    tims = datetime.now()
                    r = button_sur()
                    if r == "Виски кола":
                        cursor.execute("UPDATE list_2 SET w_c = ? WHERE number = ?", (int(res[2]) + 1, res[0]))
                    elif r == "Виски сок":
                        cursor.execute("UPDATE list_2 SET w_s = ? WHERE number = ?", (int(res[3]) + 1, res[0]))
                    elif r == "Вино":
                        cursor.execute("UPDATE list_2 SET vin = ? WHERE number = ?", (int(res[4]) + 1, res[0]))
                    cursor.execute("UPDATE list_2 SET sur = ? WHERE number = ?", ('---', res[0]))
                    cursor.execute("UPDATE list_2 SET time = ? WHERE number = ?", (tims, res[0]))
                    conn.commit()
                    conn.close()
                    window_info('photo_2023-05-31_16-24-01.jpg')
                else:
                    window_info('photo_2023-05-31_10-24-02.jpg')
            else:
                window_info('photo_2023-05-31_18-28-23.jpg')

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()
