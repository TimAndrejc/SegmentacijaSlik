import cv2 as cv
import random

def kmeans(slika, k=3, iteracije=10):

    pass

def meanshift(slika, velikost_okna, dimenzija):

    pass

def izracunaj_centre(slika, izbira, dimenzija_centra, T):
    height, width = slika.shape[:2]
    centeres = []
    while len(centeres) < 3:
        if izbira == 0:
            x = random.randint(0, height -1)
            y = random.randint(0, width-1)
            add = True
            G, R, B = slika[x, y][:3]
            for it in centeres:

                if dimenzija_centra == 5:
                    if ((abs(it[0] - x) + abs(it[1] - y) +
                         abs(int(it[2]) - int(B)) +
                         abs(int(it[3]) - int(G)) +
                         abs(int(it[4]) - int(R))) < T):
                        add = False
                        break
                else:
                    if ((abs(int(it[0]) - int(B)) +
                         abs(int(it[1]) - int(G)) +
                         abs(int(it[2]) - int(R))) < T):
                        add = False
                        break
            if add:
                if dimenzija_centra==5:
                    centeres.append([x, y, int(B), int(G), int(R)])
                else:
                    centeres.append([int(B),int(G),int(R)])
    print(centeres)

if __name__ == "__main__":
    img = cv.imread('types-of-peppers-1.jpg')
    izracunaj_centre(img, 0, 3, 100)
    pass