import cv2 as cv
import random
import numpy as np
mouseX, mouseY = -1, -1
clicked = False


def draw_circle(event,x,y,flags,param): #https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture
    global mouseX, mouseY, clicked
    if event == cv.EVENT_LBUTTONDOWN:
        clicked = True
        mouseX, mouseY = x, y


def kmeans(slika, dimenzija, k=3, iteracije=10):
    height, width = slika.shape[:2]

    centres = izracunaj_centre(slika, 1, dimenzija, (300/k), k)
    newCentres = np.zeros((k, dimenzija), dtype=np.int32)
    numOfPixels = [0]*k
    diff = [0] * k
    centreImage = np.zeros((height, width), np.uint8)
    for m in range(iteracije):
        for i in range(width):
            for j in range(height):
                closest = 10000000
                index = -1
                for x in range(len(centres)):
                    if dimenzija == 3:
                        try:
                            temp =razdalja3d(centres[x], slika[j,i])
                        except:
                            print(str(slika[j, i][0])+ " " + str(centres[x][0])+ " "+ str(slika[j, i][1]) + " " +str(centres[x][1])+ " " +str(slika[j, i][2]) +" " +str(centres[x][2]))
                        if closest > temp:
                            index = x
                            closest = temp
                    else:
                        temp = razdalja5d(j,i,centres[x][0], centres[x][1], slika[j, i], centres[x][2:5])
                        if closest > temp:
                            index = x
                            closest = temp
                centreImage[j][i] = index
                if(dimenzija == 3):
                    newCentres[index] += slika[j][i]
                else:
                    newCentres[index][0] += j
                    newCentres[index][1] += i
                    newCentres[index][2:5] += slika[j][i]

                numOfPixels[index] += 1
        brk = True
        print(centres)
        for i in range(0,k):
            diff[i] = centres[i]
            centres[i] = newCentres[i] / numOfPixels[i]
            diff[i] = abs(diff[i] - centres[i])
            if sum(diff[i]) > k:
                brk = False
        if brk:
            print(m)
            break

    newImg = cv.cvtColor(slika, cv.COLOR_BGR2GRAY)
    for i in range(width):
        for j in range(height):
            newImg[j,i] = centreImage[j][i]*(255/k)

    cv.imshow("seg", newImg)
    cv.waitKey(0)
    pass

def razdalja3d(t1, t2):
    return abs(int(t1[0]) - int(t2[0])) + abs(int(t1[1]) - int(t2[1])) + abs(int(t1[2]) - int(t2[2]))

def razdalja5d(j,i,x,y, t1, t2):
    return (abs(int(t1[0]) - int(t2[0])) + abs(int(t1[1]) - int(t2[1])) + abs(int(t1[2])
            - int(t2[2]) + abs(j)- y) + abs(x - i))

def izracunaj_centre(slika, izbira, dimenzija_centra, T, k):
    height, width = slika.shape[:2]
    global mouseX, mouseY, clicked
    centeres = []
    while len(centeres) < k:
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
            selectImage = slika.copy()
            while (1):
                cv.namedWindow("slika")
                cv.setMouseCallback("slika", draw_circle)
                cv.imshow("slika", selectImage)
                key = cv.waitKey(20) & 0xFF
                if clicked:
                    pixel = slika[mouseY, mouseX]
                    if dimenzija_centra == 5:
                        centeres.append([mouseY, mouseX, int(pixel[0]), int(pixel[1]), int(pixel[2])])
                    else:
                        centeres.append([int(pixel[0]), int(pixel[1]), int(pixel[2])])
                    clicked = False
                    cv.circle(selectImage, (mouseX, mouseY), 5, (255, 0, 0), -1)
                if len(centeres) >= k:
                    cv.destroyWindow("slika")
                    break

    return centeres

def meanshift(slika, velikost_okna, dimenzija):


    pass

if __name__ == "__main__":
    img = cv.resize(cv.imread("types-of-peppers-1.jpg"), (50,50))
    #kmeans(img, 5, 6)
    meanshift(img, 3, 5)
    cv.destroyAllWindows()
    pass