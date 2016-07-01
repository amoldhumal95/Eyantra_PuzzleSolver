'''
Written by: Arohi Gupta
'''
import numpy as np
import numpy
import cv2

def play(img):
    '''
    img-- a single test image as input argument
    No_pos_D1 -- List containing detected numbers in Division D1
    No_pos_D2 -- List of pair [grid number, value]

    '''
    
    h, w, c = img.shape #computing size of test image to draw mask

    '''........draw mask to exclude the horizontal and vertical lines..............'''

    numb = np.zeros((h,w,c), np.uint8) #creating a black image to draw the mask on
    for q in range (0,3):
        for p in range (0,4):
            cv2.rectangle(numb,(76+p*84,104+q*84),(125+p*84,163+q*84),(255,255,255),-1) #ROI D1 : exploiting thick blobs to draw a black mask to pass only numbers
        q=q+1
    for q in range (0,4):
        for i in range(0,6):
            cv2.rectangle(numb,(532+i*84,100+q*84),(600+i*84,167+q*84),(255,255,255),-1)#ROI D2 : exploiting thick blobs to draw a black mask to pass only numbers
        q=q+1
    #cv2.imshow('Number MASK',numb)
    m = 255- numb

    '''extracting the numbers by masking the above image '''
    img2 = cv2.bitwise_or(img,m) #Bitwise or operation between image and mask m 

    '''.................countouring........................'''
    gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) #converting image to grayscale
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #using cv2.findCountors to find countours and calculating the length
    length=len(contours)

    '''this for loop eliminates the largest contour, which is the border contour of the image'''

    for i in range(1,length): 
        cv2.drawContours(img2,contours,i,(0,255,0),2)

    cv2.drawContours(img2,contours,1,(0,255,0),2)
    #cv2.imshow("contour image",img2)


    #Extracting grids by inverting the original mask
    tog= 255 - m
    #cv2.imshow("GRID MASK",tog)
    grid = cv2.bitwise_or(img,tog)
    #cv2.imshow("GRID",grid)

    #adding the grid and the contoured area
    dst = cv2.bitwise_and(img2,grid)
    cv2.imshow('output',dst)

    ###################################################D1 :  DETECTING SINGLE NUMBERS###################################
    #importing template of numbers
    num1 = cv2.imread('1.jpg')
    num0 = cv2.imread('0.jpg')
    num2 = cv2.imread('2.jpg')
    num3 = cv2.imread('3.jpg')
    num4 = cv2.imread('4.jpg')
    num5 = cv2.imread('5.jpg')
    num6 = cv2.imread('6.jpg')
    num7 = cv2.imread('7.jpg')
    num8 = cv2.imread('8.jpg')
    num9 = cv2.imread('9.jpg')

    #Cropping regions of input image and assigning them regions
    #compairing the cropped regions and templates
    #___________________________________________________________________________________
    ex = [0 for i in range(12)] #creating an array to store cropped regions
    l=0
    for q in range (0,3): #cropping regions
        for p in range (0,4):
            ex[l] = img[104+q*84:163+q*84,76+p*84:125+p*84] ##[y1:y2,x1:x2]
            l=l+1
        q=q+1
                   
    array = [num0,num1,num2,num3,num4,num5,num6,num7,num8,num9] #creating an array to store templates
    No_pos_D1=[0 for i in range(12)]
    v=0
    #compare every template with every cropped region that is 120 combinations to find a match
    for j in range (0,12): #checking possible 120 combinations for a match
        for i in range(0,10):
            template = array[i]     
            res = cv2.matchTemplate(ex[j],array[i],cv2.TM_CCOEFF_NORMED)
            minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(res)
            if maxVal >= 0.8: #if match is >0.8
                No_pos_D1[v]=i
                v=v+1
        j=j+1

    
    ########################################################D2: DETECTING 2 DIGIT NUMBERS#################################

    ex2 = [0 for i in range(24)]#creating an array to store double digit region 2
    ex1 = [0 for i in range(24)]#creating an array to store double digit region 1
    tens = [0 for i in range(24)] #stores all tens place digits
    unit = [0 for i in range(24)]# stores all unit place digits
    single = [0 for i in range(24)] # creating an array to store single regions
    black = [0 for i in range(24)] #an array for storing no of black pixels
    l=0

    #CROPPING THE FIRST HALF OF THE AREA ENCLOSED WITHIN A GRID
    for q in range (0,4):
        for p in range (0,6):
            ex1[l] = img[68+q*91:184+q*91,502+p*91:561+p*89] #y1:y2,x1:x2]
            l=l+1
        q=q+1
    #CROPPING THE SECOND HALF OF THE AREA ENCLOSED WITHIN A GRID
    l=0
    for q in range (0,4):
        for p in range (0,6):
            ex2[l] = img[69+86*q:189+86*q,560+85*p:620+89*p] #y1:y2,x1:x2]
            l=l+1
        q=q+1
    l=0
    #CROPPING THE AREA ENCLOSED WITHIN A GRID
    for q in range (0,4):
        for p in range (0,6):
            single[l] = img[100+q*84:167+q*84,532+p*84:600+p*84] ##[y1:y2,x1:x2]
            l=l+1
        q=q+1

    ''' FOR THE TOTAL AREA WITHIN THE GRID,CALCULATING NO OF BLACK PIXELS TO DETERMINE IF A SINGLE DIGIT OR A DOUBLE DIGIT IS PRESENT.'''
    for l in range (0,24):
        gray = cv2.cvtColor(single[l], cv2.COLOR_BGR2GRAY)
        height,width=gray.shape
        count=0
        for i in range (0,height):
            for j in range (0,width):
                if gray[i][j]<20:
                    count = count+1 #calculating the number of black pixels
        black[l]= count
    '''FINDING EVERY REGION WHERE NO. OF PIXELS <THRESHOLD AND APPLYING TEMPLATE MATCHING ON IT'''
    for l in range (0,24):
        if black[l] < 900: #if pixels< thresh value apply template matching
            for i in range(0,10):
                template = array[i] 
                res = cv2.matchTemplate(single[l],array[i],cv2.TM_CCOEFF_NORMED)
                minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(res)
                if maxVal >= 0.9: #if a match is found it means a single digit number is present. As single digits fall at unit place, store it in unit array
                    unit[l]=i
        else :
            pass
    pp=0
    '''for other numbers which are not single digit numbers , extracting the tens part'''
    D=[0 for i in range(24)]
    for j in range (0,24): #checking possible 240 combinations for a match
        for i in range(0,10):
            template = array[i]     
            res = cv2.matchTemplate(ex1[j],array[i],cv2.TM_CCOEFF_NORMED)
            minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(res)
            if maxVal >= 0.9:
                tens[j]=i
    '''for other numbers which are not single digit numbers , extracting the unit part'''
    for j in range (0,24): #checking possible 240 combinations for a match
        for i in range(0,10):
            template = array[i]     
            res = cv2.matchTemplate(ex2[j],array[i],cv2.TM_CCOEFF_NORMED)
            minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(res)
            if maxVal >= 0.8:
                unit[j]=i            
    for pp in range (0,24):
        D[pp] = 10*tens[pp]+unit[pp] # adding tens and unit array to form a 2 digit number
    c=0
    p=0
    '''finding the index of the box and assigning it to respective numbers found'''
    D2=[[0 for row in range(0,1)] for col in range(0,24)]
    for i in range(0,24):
        if D[i]!=0:
            c=c+1
            D2[p]=[i,D[i]]
            p=p+1
    No_pos_D2=[[0 for row in range(0,1)] for col in range(0,c)]
    for i in range (0,c):
        No_pos_D2[i]=D2[i]
        
      
    return No_pos_D1, No_pos_D2


if __name__ == "__main__":
    #code for checking output for single image
    img = cv2.imread('test_image1.jpg')
    No_pos_D1,No_pos_D2 = play(img)
    print 'D1=',No_pos_D1
    print 'D2=',No_pos_D2
cv2.waitKey(0)
