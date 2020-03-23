import argparse
import cv2
import camera
import color_filter
from timeit import default_timer as timer

x1 = 0
y1 = 0
x2 = 0
y2 = 0
target = [0,0]
centerList = [None,  None, [75,420], None, None, None, None, None, None, None, None, None]
areaList = [1,2,3,4,5,6,7,8,9,10,11,12]
preT = [0,0]
prePT = [0,0]
pre2T = [0,0]
pre3T = [0,0]
pre4T = [0,0]

parser = argparse.ArgumentParser()
parser.add_argument("-v", required=True)
args = vars(parser.parse_args())

vs = cv2.VideoCapture(args["v"])
# out = cv2.VideoWriter('ridgeback0.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (1280,720))
backSub = cv2.createBackgroundSubtractorMOG2()
value, frame = vs.read()
# frame = cv2.flip(frame, 0 )
# frame = cv2.flip(frame, 1 )
frame = cv2.resize(frame, (1280, 720))
# num = 0
# file1 = open("MyFile.txt","a") 

while frame is not None:
	# out.write(frame)
	start = timer()
	oHeight, oWidth = frame.shape[:2]
	crop_img = frame[128:540, 0:1280]
	height, width = crop_img.shape[:2]
	subMask = backSub.apply(crop_img)
	subtracted = cv2.bitwise_and(crop_img,crop_img,mask = subMask)

	combined = color_filter.filter_color(subtracted)

	colored = cv2.bitwise_and(subtracted,subtracted,mask = combined)

	erodeMask = cv2.erode(combined, None)

	dilateMask = cv2.dilate(erodeMask, None)

	contours, hierarchy = cv2.findContours(dilateMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	center = None 
	radius = None
	if len(contours) > 0:
		biggestContour = None
		if all(x is None for x in centerList):
			biggestContour = max(contours, key=cv2.contourArea)
			(centerC, radiusC) = cv2.minEnclosingCircle(biggestContour)
		else:
			areaContours = []
			lastCenter = None
			position = 0
			for i, centerPoint in enumerate(reversed(centerList)):
				if centerPoint is not None:
					lastCenter = centerPoint
					position = i
			factor = areaList[position]
			for contour in contours:
				(centerC, radiusC) = cv2.minEnclosingCircle(contour)
				if centerC[0] > lastCenter[0] - width/factor and centerC[0] < lastCenter[0] + width/factor and centerC[1] > lastCenter[1] - width/factor and centerC[1] < lastCenter[1] + width/factor:
					areaContours.append(contour)
			if len(areaContours) > 0:
				biggestContour = max(areaContours, key=cv2.contourArea)
		if biggestContour is not None:	
			(center, radius) = cv2.minEnclosingCircle(biggestContour)
			if radius > 1.99:
				centerList.insert(0, centerList.pop())
				centerList[0] = center
				if abs(center[0] - preT[0]) < width/50 and abs(center[1] - preT[1]) < height/50 and abs(center[0] - prePT[0]) < width/40 and abs(center[1] - prePT[1]) < height/40:
					if abs(center[0] - pre2T[0]) < width/30 and abs(center[1] - pre2T[1]) < height/30 and abs(center[0] - pre3T[0]) < width/20 and abs(center[1] - pre3T[1]) < height/20:
						if abs(center[0] - pre4T[0]) < width/10 and abs(center[1] - pre4T[1]) < height/10:
							target = center
							cv2.circle(frame, (int(center[0]), int(center[1]+128)), int(radius), (0, 0, 255), 2)
				preT = center
				prePT = preT
				pre2T = prePT
				pre3T = pre2T
				pre4T = pre3T
	else:
		centerList.insert(0, centerList.pop())
		centerList[0] = None
	for x in range(1):
		x1, y1, x2, y2 = camera.adjustCamera(target, width, height)
		
		cv2.rectangle(frame, (x1, y1+128), (x2, y2+128), (255,0,0), 2)

		# cv2.imshow("subtract", subtracted)
		# cv2.imshow("color", colored)
		# cv2.imshow("erode", erodeMask)
		# cv2.imshow("dilate", dilateMask)
		# cv2.imshow("camera", frame[y1+128:y2+128, x1:x2])
		cv2.imshow("frame", frame)

		value, frame = vs.read()
		# value, frame = vs.read()
		# value, frame = vs.read()
		# value, frame = vs.read()

		# frame = cv2.flip(frame, 0 )
		# frame = cv2.flip(frame, 1 )
		frame = cv2.resize(frame, (1280, 720))
		# file1.write(str(num) +"\t\t"+ str("{0:.1f}".format(target[0])) +"\t\t"+ str("{0:.1f}".format(target[1])) + "\n")
		# num = num+1
	key = cv2.waitKey(1) & 0xFF
	duration = timer() - start
	print(duration)

out.release()



	