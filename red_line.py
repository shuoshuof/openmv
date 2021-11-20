enable_lens_corr = False # turn on for straighter lines...打开以获得更直的线条…
import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) #灰度更快
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

min_degree = 70
max_degree = 110

red_threshold = (0, 79, 20, 127, -4, 127)
def find_line(x,y,w,h,py):
    roi=[x,y,w,h]
    min_degree1 = 0
    max_degree1 = 20
    flag = 0
    error = 0
    for l in img.find_lines(roi =roi, threshold = 1000, theta_margin = 25, rho_margin = 25):
        if (min_degree1 <= l.theta()) and (l.theta() <= max_degree1):
            img.draw_line(l.line(), color = (0, 255, 0))
            x0,y0,x1,y1 = l.line()
            flag = 1
            if x1-x0 !=0:
                k = (y1-y0)/(x1-x0)
                b = y1-k*x1
                px= (py-b)/k
                error = 80 - px
            else :
                px = x1
                error = 80 - px
            img.draw_cross(int(px), int(py), color = (255,0,0), size = 10, thickness = 2)
    if flag ==0:
        min_degree2 = 160
        max_degree2 = 179
        for l in img.find_lines(roi =roi, threshold = 1000, theta_margin = 25, rho_margin = 25):
            if (min_degree2 <= l.theta()) and (l.theta() <= max_degree2):
                img.draw_line(l.line(), color = (0, 255, 0))
                x0,y0,x1,y1 = l.line()
                if x1-x0 !=0:
                    k = (y1-y0)/(x1-x0)
                    b = y1-k*x1
                    px= (py-b)/k
                    error = 80 - px
                else :
                    px = x1
                    error = 80 - px
                img.draw_cross(int(px), int(py), color = (255,0,0), size = 10, thickness = 2)
                break
    img.draw_rectangle(x,y,w,h, color = (255, 0, 0), thickness = 1, fill = False)
    return error
def find_ten(x,y,w,h):
    flag = 0
    roi=[x,y,w,h]
    min_degree1 = 70
    max_degree1 = 110
    for l in img.find_lines(roi =roi, threshold = 1000, theta_margin = 25, rho_margin = 25):
        if (min_degree1 <= l.theta()) and (l.theta() <= max_degree1):
            img.draw_line(l.line(), color = (0, 0, 255))
            flag =1
            break
    img.draw_rectangle(x,y,w,h, color = (255, 0, 0), thickness = 1, fill = False)
    return flag
while(True):
    clock.tick()
    img = sensor.snapshot()
    img.binary([red_threshold])
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...
    py = 100#越小以越前的直线误差为基准
    error = find_line(60,0,40,120,py)
    if (find_ten(0,50,160,20)):#参数为roi区域
        print("十字路口")
    # if (find_ten(0, 80, 160, 20)):
    #     find_number(img)
    print("error=",error)
    #print("FPS %f" % clock.fps())
# About negative rho values:
# 关于负rho值:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].
# A [theta+0:-rho]元组与[theta+180:+rho]相同。
