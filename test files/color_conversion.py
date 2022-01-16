def gimp_to_opencv_hsv(gimp_h, gimp_s, gimp_v):
    opencv_h = float(gimp_h / 2)
    opencv_s = float(gimp_s / 100) * 255
    opencv_v = float(gimp_v / 100) * 255

    print(f"({opencv_h}, {opencv_s}, {opencv_v})")


gimp_to_opencv_hsv(0, 57, 64)
gimp_to_opencv_hsv(15, 100, 90)
gimp_to_opencv_hsv(350, 57, 64)
gimp_to_opencv_hsv(360, 100, 65)
gimp_to_opencv_hsv(50, 25, 65)
gimp_to_opencv_hsv(70, 100, 85)
