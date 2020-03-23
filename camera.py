x1 = 0
y1 = 0
x2 = 600
y2 = 300
origWidth = 600
origHeight = 300
maxWidth = 800
maxHeight = 400
moveSpeed = 10
growSpeedX = 10
growSpeedY = 5
moveX = [0, 0, 1, 2, 3, 5, 8, 13, 21, 34]
moveY = [0, 0, 0, 0, 1, 2, 4, 6, 9, 12]
growX = [-4, -2, -2, 0, 0, 0, 2, 2, 4, 8]
growY = [-2, -1, -1, 0, 0, 0, 1, 1, 2, 4]

def adjustCamera(center, width, height):
    global x1, x2, y1, y2
    midX = (x2 + x1)/2
    midY = (y2 + y1)/2
    disX = (x2 - x1)/2
    disY = (y2 - y1)/2
    percentLX = 0
    percentGX = 0
    percentY = 0
    
    if center[0] > midX:
        percentGX = int(((center[0] - midX)/disX)*10)
        if percentGX > 9: percentGX = 9
        if x2 < width:
            x1 += moveX[percentGX]
            x2 += moveX[percentGX]
    elif center[0] < midX:
        percentLX = int(((midX - center[0])/disX)*10)
        if percentLX > 9: percentLX = 9
        if x1 > 0:
            x1 -= moveX[percentLX]
            x2 -= moveX[percentLX]
    if center[1] > midY:
        percentY = int(((center[1] - midY)/disY)*10)
        if percentY > 9: percentY = 9
        if y2 < height:
            y1 += moveY[percentY]
            y2 += moveY[percentY]
    elif center[1] < midY:
        percentY = int(((midY - center[1])/disY)*10)
        if percentY > 9: percentY = 9
        if y1 > 0:
            y1 -= moveY[percentY]
            y2 -= moveY[percentY]

    percent = max(percentLX, percentGX)
    if (percent > 4 and x2-x1 < maxWidth) or (percent < 5 and x2-x1 > origWidth):
        if x1 > 0 and x2 < width and y1 > 0 and y2 < height:
            x1 -= growX[percent]
            x2 += growX[percent]
            y1 -= growY[percent]
            y2 += growY[percent]
        elif percent < 5:
            x1 -= growX[percent]
            x2 += growX[percent]
            y1 -= growY[percent]
            y2 += growY[percent]
        elif (percentLX > 4 and x1 <= 0 and x2-x1 > origWidth) or (percentGX > 4 and x2 >= width and x2-x1 > origWidth):
            percentN = 9 - percent
            x1 -= growX[percentN]
            x2 += growX[percentN]
            y1 -= growY[percentN]
            y2 += growY[percentN]
        elif percent > 4 and x1 > 0 and x2 < width:
            if x1 <=0:
                x2 += 2*growX[percent]
            elif x2 >= width:
                x1 -= 2*growX[percent]
            else:
                x1 -= growX[percent]
                x2 += growX[percent]
            if y1 <=0:
                y2 += 2*growY[percent]
            elif y2 >= width:
                y1 -= 2*growY[percent]
            else:
                y1 -= growY[percent]
                y2 += growY[percent]
    

    if(x1 < 0):
        x2 += -x1
        x1 += -x1
    elif(x2 > width):
        x1 -= x2-width
        x2 -= x2-width

    return x1, y1, x2, y2