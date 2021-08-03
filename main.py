import cv2 as cv
import numpy as np


class Cropper:

    def __init__(self):
        self.filename = "test.png"
        self.extension = self.filename.split('.')[-1]
        self.src = cv.imread(self.filename, -1)

        if len(self.src.shape) == 2:  # If the source image is gray scale
            self.temp = cv.cvtColor(self.src, cv.COLOR_GRAY2BGR)
        else:
            self.temp = self.src.copy()

        print(self.temp.shape)
        self.points = []

    def mousePoint(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            print(x, y)
            self.points.append((x, y))
            cv.circle(self.temp, center=(x, y), radius=10, color=(0, 0, 255), thickness=-1)

    def main(self):
        while True:
            cv.imshow("input", self.temp)

            cv.setMouseCallback("input", self.mousePoint)

            key = cv.waitKey(1) & 0xFF
            if key == ord("c"):  # 'C' to crop and show cropped
                self.polygonCropper(self.src, self.points)
                break
            elif key == ord("q"):  # 'Q' to quit
                break

    def polygonCropper(self, img, points):
        points = np.asarray(points)

        # (1) Crop the bounding rect
        rect = cv.boundingRect(points)
        x, y, w, h = rect
        croped = img[y:y + h, x:x + w].copy()

        # (2) make mask
        points = points - points.min(axis=0)
        mask = np.zeros(croped.shape[:2], np.uint8)
        cv.drawContours(mask, [points], -1, (255, 255, 255), -1, cv.LINE_AA)

        # (3) do bit-op
        dst = cv.bitwise_and(croped, croped, mask=mask)

        while True:
            cv.imshow("output", dst)
            key = cv.waitKey(1) & 0xFF
            if key == ord("s"):  # 'S' to save
                if self.extension == 'tif':
                    cv.imwrite("cropped." + self.extension, dst, ((int(cv.IMWRITE_TIFF_RESUNIT), 2,
                                                                   int(cv.IMWRITE_TIFF_COMPRESSION), 1,
                                                                   int(cv.IMWRITE_TIFF_XDPI), 100,
                                                                   int(cv.IMWRITE_TIFF_YDPI), 100)))
                else:
                    cv.imwrite("cropped." + self.extension, dst)

                break
            elif key == ord("q"):  # 'Q' to quit
                break


if __name__ == '__main__':
    c = Cropper()
    c.main()
