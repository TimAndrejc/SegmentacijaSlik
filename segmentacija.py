import cv2 as cv
import random
mouseX, mouseY = -1, -1
clicked = False

def draw_circle(event,x,y,flags,param): #https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture
    global mouseX, mouseY, clicked
    if event == cv.EVENT_LBUTTONDOWN:
        clicked = True
        mouseX, mouseY = x, y


def kmeans(slika, dimenzija, k=3, iteracije=10):
    height, width = slika.shape[:2]

    centres = izracunaj_centre(slika, 0, dimenzija, 100, k)
    centreImage = np.zeros((height, width), np.uint8)
    for i in range(width -1):
        for j in range(height -1):
            closest = 10000000
            index = -1
            for x in range(len(centres)):
                if dimenzija == 3:
                    temp = abs(int(slika[j, i][0]) - int(centres[x][0])) + abs(int(slika[j, i][1]) - int(centres[x][1])) + abs(int(slika[j, i][2]) - int(centres[x][2]))
                    if closest > temp:
                        index = x
                        closest = temp
                else:
                    temp = abs(int(j) - int(centres[x][0])) + abs(int(i) - int(centres[x][1])) + abs(int(slika[j, i][0]) - int(centres[x][2])) + abs(int(slika[j, i][1]) - int(centres[x][3])) + abs(int(slika[j, i][2]) - int(centres[x][4]))
                    if closest > temp:
                        index = x
                        closest = temp
            centreImage[j][i] = index
    print(centreImage)
    pass

def meanshift(slika, velikost_okna, dimenzija):

    pass

def izracunaj_centre(slika, izbira, dimenzija_centra, T):
    height, width = slika.shape[:2]
    global mouseX, mouseY, clicked
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
        else:
            while (1):
                cv.namedWindow("slika")
                cv.setMouseCallback("slika", draw_circle)
                cv.imshow("slika",slika)
                k = cv.waitKey(20) & 0xFF
                if clicked:
                    pixel = slika[mouseY, mouseX]
                    if dimenzija_centra == 5:
                        centeres.append([mouseY, mouseX, int(pixel[0]), int(pixel[1]), int(pixel[2])])
                    else:
                        centeres.append([int(pixel[0]), int(pixel[1]), int(pixel[2])])
                    clicked = False
                    cv.circle(img, (mouseX, mouseY), 5, (255, 0, 0), -1)
                if len(centeres) >= 3:
                    break

    print(centeres)

if __name__ == "__main__":
    img = cv.imread('types-of-peppers-1.jpg')
    izracunaj_centre(img, 1, 5, 100)

    cv.destroyAllWindows()
    pass