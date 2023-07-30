import sys
from datetime import datetime

import cv2
import psycopg2
from pyzbar.pyzbar import decode
import pygame
import time

from test_button import button_yes_no

while True:

    cap = cv2.VideoCapture(0)
    scanned = False
    while not scanned:
        _, frame = cap.read()
        for code in decode(frame):
            data = code.data.decode('utf-8')
            scanned = True

            #conn = sqlite3.connect('tele_table_mint.db')
            conn = psycopg2.connect(host='141.8.199.12', port=5432, user='postgres',
                                    password='20rasputin23', database='rasputin_base.db')

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM list_1 WHERE user_id = %s", (data,))
            res = cursor.fetchone()
            #conn.close()

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
                tims = datetime.now()
                sur = '---'
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS list_2
                                                       (number SERIAL PRIMARY KEY, name VARCHAR, username VARCHAR, 
                                                       user_id NUMERIC(20), sex VARCHAR, time TIMESTAMP, sur VARCHAR, 
                                                       w_c NUMERIC(2), w_s NUMERIC(2), vin NUMERIC(2), manager VARCHAR)""")
                cursor.execute("SELECT * FROM list_2 WHERE user_id = %s", (data,))
                res2 = cursor.fetchone()
                if res2:
                    window_info('photo_2023-05-19_21-57-41.jpg')
                else:
                    if res[5] == "Ж":
                        r = button_yes_no()
                        if r == "Нет":
                            sur = 'нет'
                        sur_select = '0'
                        cursor.execute(
                            'INSERT INTO list_2 (name, username, user_id, sex, time, sur, w_c, w_s, vin, manager)'
                            ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (res[1], res[3], res[4], res[5], tims, sur, sur_select, sur_select, sur_select, res[-1]))
                        conn.commit()
                        conn.close()
                        window_info('photo_2023-05-19_21-45-51.jpg')
                    else:
                        sur = 'нет'
                        sur_select = '0'
                        cursor.execute(
                            'INSERT INTO list_2 (name, username, user_id, sex, time, sur, w_c, w_s, vin, manager) '
                            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (res[1], res[3], res[4], res[5], tims, sur, sur_select, sur_select, sur_select, res[-1]))
                        conn.commit()
                        conn.close()
                        window_info('photo_2023-05-19_21-45-51.jpg')

            else:
                window_info('photo_2023-05-19_22-32-12.jpg')


        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()



