import cv2
import os


import numpy as np
#path = r'D:\陽程ocr'
#path = r'D:\oli\paddle\PaddleOCR\StyleText\examples\style_images'
#path = r'D:\ocrex'
#path = r'D:\oli\stefann\release\sample_images'
#path = r'D:\oli\test\caption.jpg'
#savepath = r'D:\oli\paddle\PaddleOCR\StyleText\dataset'
#sp = ''


def draw(event, x, y, flags, param):
    global x1,x2,y1,y2,imggg,cut,first,xz,yz,z,imgg,zoom,counterx,countery,imgbu,bu
    #imggg = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN or flags == cv2.EVENT_FLAG_LBUTTON:
        zoom = False
        if first == True:
            counterx=[]
            countery=[]
            counterxs.append(counterx)
            counterys.append(countery)
            first =False
        x1 = x
        y1 = y
        cv2.circle(imggg, (x, y), 2, (0, 0, 255), -1)
        counterx.append(x)
        countery.append(y)
        '''else :
            cv2.line(imggg,(x1,y1),(x,y),(0,0,255),5)
            counterx.append(x)
            countery.append(y)'''
    elif event == cv2.EVENT_LBUTTONUP:
        #cut = img[y1-1:y2+1,x1-1:x2+1]############****
        #cv2.circle(imggg, (x1, y1), (x2, y2), (0, 255, 0), 10)
        #cv2.imshow('cut',cut)  
        imgg = img.copy()
        imggg = imgg[int(yz/10)*z:h-int((h-yz)/10)*z,int(xz/10)*z:w-int((w-xz)/10)*z]

        for n in range(0,len(counterxs)):
            for m in range(0,len(counterxs[n])-1):
                cv2.line(imggg,(counterxs[n][m],counterys[n][m]),(counterxs[n][m+1],counterys[n][m+1]),(255,255,255),2)

        x1 = x
        y1 = y
    elif event == cv2.EVENT_RBUTTONDOWN:
        imgg = imggg.copy()
        imgbu= imggg.copy()
        bu.append(imgbu)
        first = True
    elif event==cv2.EVENT_MOUSEWHEEL:
        if zoom== True:
            xz = int(xz/10)*z+x
            yz = int(yz/10)*z+y
            if flags >= 0:
                if (h-int((h-yz)/10)*z)-(int(yz/10)*z)>=0 and  (w-int((w-xz)/10)*z)-(int(xz/10)*z)>=0 and z <=9:
                    z+=1
                    imggg = imgg[int(yz/10)*z:h-int((h-yz)/10)*z,int(xz/10)*z:w-int((w-xz)/10)*z]
            if flags <= 0:
                if z >=1 :
                    z-=1
                    imggg = imgg[int(yz/10)*z:h-int((h-yz)/10)*z,int(xz/10)*z:w-int((w-xz)/10)*z]
def roi(carplate):
    global img,imggg,first,counterx,countery,zoom,h,w,z,imgg,xz,yz,cut,counterxs,counterys,imgbu,bu,xmin,ymin,xmax,ymax
    img = carplate.copy()
    imgg = img.copy()
    imgbu = img.copy()
    bu =[]
    bu.append(imgbu)
    h,w,_ = img.shape
    z = 0
    yz = int(h/2)
    xz = int(w/2)
    xmin = None
    ymin = None
    xmax= None
    ymax = None##################################################################################
    imggg = imgg[int(yz/10)*z:h-int((h-yz)/10)*z,int(xz/10)*z:w-int((w-xz)/10)*z]
    cv2.namedWindow('pic', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('pic',draw)
    zoom = True
    first = True
    counterxs = []
    counterys = []
    while True:
        #cv2.imshow('picc',imgg)
        cv2.imshow('pic',imggg)

        k1 = cv2.waitKey(1)
        if k1 == 27 or k1 == ord('q'):
            xmin = None
            ymin = None
            xmax= None
            ymax = None
            cv2.destroyAllWindows()
            break
        elif k1 == 13:
            xmins = []
            xmaxs = []
            ymins= []
            ymaxs = []
            for n in range(0,len(counterxs)):
                xmin = min(counterxs[n])
                xmax = max(counterxs[n])
                ymin = min(counterys[n])
                ymax = max(counterys[n])
                xmins.append(xmin)
                ymins.append(ymin)
                ymaxs.append(ymax)
                xmaxs.append(xmax)
            xmin = min(xmins)
            xmax = max(xmaxs)
            ymin = min(ymins)
            ymax = max(ymaxs)
            #print(z)
            cut = img[ymin+int(yz/10)*z:ymax + int(yz/10)*z,int(xz/10)*z+xmin:int(xz/10)*z+xmax]
            cutdraw = cut.copy()
            for n in range(0,len(counterxs)):
                for m in range(0,len(counterxs[n])-1):
                    cv2.line(cutdraw,(counterxs[n][m]-(xmin-1),counterys[n][m]-ymin-1),(counterxs[n][m+1]-xmin-1,counterys[n][m+1]-ymin-1),(255,255,255),2)
                
            #cv2.imshow('cut',cut)  
            cv2.imshow('cutdraw',cutdraw)
            k2 = cv2.waitKey()
            if k2 == 27 or k2 == ord('q') or k2 == 13:
                cv2.destroyAllWindows()
                break
            cv2.destroyWindow('cutdraw')
            imgg = img.copy()
        elif k1 == ord('c'):
            imgg = img.copy()
            imggg = imgg[int(yz/10)*z:h-int((h-yz)/10)*z,int(xz/10)*z:w-int((w-xz)/10)*z]
            counterxs.clear()
            counterys.clear()
            first = True
            zoom = True   
        elif k1 == 8:
            if first == True:
                
                if len(bu)>0:
                    bu = bu[:-1]
                    imgg = bu[len(bu)-1].copy()
                    
                    #
                else:
                    imgg = img.copy()
            else:
                if len(bu)>0:
                    
                    imgg = bu[len(bu)-1].copy()
                    #
                else:
                    imgg = img.copy()
                first = True
                
            imggg = imgg[int(yz/10)*z:h-int((h-yz)/10)*z,int(xz/10)*z:w-int((w-xz)/10)*z]
            counterx.clear()
            countery.clear()
            
            counterxs=counterxs[:-1]
            counterys=counterys[:-1]
            first = True
            
    return xmin,ymin,xmax,ymax,cut
            
def puttxt(fix,tp):
    fix2 = fix.copy()
    h,w,d =fix.shape
    text = ''
    piclist =[]
    global numbers,number
    
    while True:
        
        cv2.imshow('fix2',fix2) 
        kp = cv2.waitKey()
        if kp == 27 or kp == 13:
            cv2.destroyAllWindows()
            break
        elif kp == 8:
            text = text[:-1]            
            piclist = piclist[:-1]
            numbers = np.zeros([0,0,3],np.uint8)
            if len(piclist)>=1:
                
                for picloca in piclist:
                    pic = cv2.imread(picloca)
                    if numbers.shape[0]==0:
                        numbers = pic.copy()
                    else:
                        numbers =  np.concatenate((numbers, pic), axis=1)
            else:
                numbers = np.zeros(fix.shape,np.uint8)
                numbers[:,:,:]=255
        else:
            text = text + chr(kp)
            picname  = tp + "\\"+ chr(kp) +'.jpg'
            piclist.append(picname)
            numbers = np.zeros([0,0,3],np.uint8)
            for picloca in piclist:
                pic = cv2.imread(picloca)
                if numbers.shape[0]==0:
                    numbers = pic.copy()
                else:
                    numbers =  np.concatenate((numbers, pic), axis=1)
        numbers = cv2.resize(numbers,(w,h),interpolation=cv2.INTER_AREA)
        fix2 = fix.copy()
        fix2[numbers<=125]=numbers[numbers<=125]
        cv2.imshow('n',numbers) 
    return fix2
def draw4p(event, x, y, flags, param):
    global img,l
    
    if event == cv2.EVENT_LBUTTONDOWN :
        x1 = x
        y1 = y
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        l.append([x1,y1])
    if event == cv2.EVENT_RBUTTONDOWN :
        img = img_ori.copy()
        l.clear()

def getcarplate(path):
    global img , img_ori
    img = cv2.imread(path,1)
    img_ori = cv2.imread(path,1)
    global l , points1,M
    l = []
    cv2.namedWindow('picf', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('picf',draw4p)
    while True:
        cv2.imshow('picf',img)
        k = cv2.waitKey(1)
        points1 = np.array(l,np.float32)
        points2 = np.float32([[0,0], [720,0], [720,360], [0,360]])
        if k == 13 :
            
            
            try:
                M = cv2.getPerspectiveTransform(points1, points2)
                cut = cv2.warpPerspective(img_ori,M,(720, 360))
                
                break
            except:
                img = img_ori.copy()
                l.clear()
                pass
                

            
        elif k ==27:
            cv2.destroyAllWindows()
            cut = None
            break
    
    return cut

            
def  inpaint(path,tp)   :
    global mask,counters,fix,img
    carplate =  getcarplate(path)

    xmin,ymin,xmax,ymax,cut = roi(carplate)   

            
    imgg = img.copy()
    imgcut = cut.copy()
    gray = cv2.cvtColor(imgcut,cv2.cv2.COLOR_BGR2GRAY)
    mask = np.ones(gray.shape,np.uint8)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask[::]= 0
    counters=[]
    counterss = []
    for n in range(0,len(counterxs)):
        counterss = []
        for m in range(0,len(counterxs[n])-1):
            cv2.line(mask,(counterxs[n][m]-(xmin-1),counterys[n][m]-ymin-1),(counterxs[n][m+1]-xmin-1,counterys[n][m+1]-ymin-1),(255,255,255),2)
            counterss.append([counterxs[n][m]-(xmin-1),counterys[n][m]-ymin-1]) 
        counterss = np.array(counterss)
        counters.append(counterss)
    mask = cv2.cvtColor(mask,cv2.cv2.COLOR_BGR2GRAY)
    mask2 = mask.copy()
    for counterss in counters:
        mask3=mask2.copy()
        cv2.fillPoly(mask3, [counterss], (255,255,255))
        if mask3.shape == mask2.shape and not(np.bitwise_xor(mask3,mask2).any()):
            cv2.fillPoly(mask2, [counterss], (0,0,0))
        else:
            cv2.fillPoly(mask2, [counterss], (255,255,255))
            
    #mask[gray.shape[0]-2:gray.shape[0]-1,:]=0
        
        
        cv2.imshow('finalmask2', mask2)
        cv2.waitKey()
    cv2.destroyAllWindows()
    fix = cv2.inpaint(imgcut, mask2, 10, cv2.INPAINT_TELEA)
    fix2 = puttxt(fix,tp)
    imgg[int(yz/10)*z+ymin:int(yz/10)*z+ymax,int(xz/10)*z+xmin:int(xz/10)*z+xmax] = fix2
    cv2.namedWindow('finalimg', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('merge', cv2.WINDOW_NORMAL)
    #cv2.namedWindow('ori', cv2.WINDOW_NORMAL)
    #cv2.imshow('ori',img) 
    #cv2.imshow('finalmask', mask)
    
    #cv2.imshow('finalimg',imgg) 
    
    #savepath = sp + "\\final.jpg"
    #cv2.imwrite(savepath, imgg)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    h, w, dim = imgg.shape

    pst_src = np.array(
        [
            [5,5],
            [w-5,5],
            [w-5,h-5],
            [5,h-5]
         ],dtype=float
    )
    h, status = cv2.findHomography(pst_src, points1)
    im_temp = cv2.warpPerspective(imgg, h, (img_ori.shape[1], img_ori.shape[0]))
    img_final = img_ori.copy()
    cv2.fillConvexPoly(img_final, points1.astype(int), 0)
    img_final = cv2.add(img_final, im_temp)
    
    cv2.imshow('finalimg',img_final) 
    cv2.waitKey()
    cv2.destroyAllWindows()
    return img_final
    
#inpaint(path,sp)
    
    
    
    
    