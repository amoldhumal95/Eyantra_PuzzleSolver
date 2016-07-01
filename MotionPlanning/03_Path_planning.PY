'''
*
* Team Id: 		eYRCPlus-PS1#301
* Author List: 		Arohi Gupta, Dharini Dutia, Vishnu Chandrasenan, Vivek Venkatram
* Filename: 		Path_Planning
* Theme: 		<eYRC-Plus (Puzzle Solver 1)>
* Functions: 		bfs(),routing()
* Global Variables:	queue, my_list, path
'''
import serial
import time

port = "COM1"
budrate=9600
ser=serial.Serial(port,9600)


'''
Output Solution of program "02_Arithmetic_Algorithm" is passed on to this code.
Here let us consider a particular condition for understanding the wokring of code
'''

elem_D2 = 3 #no of elements in D2 will be passed from 01image_processing.py code

n_ele_a = 2 ## number of elements in a (will be passed from previous code)
s1 = '19' ## the index according to map of the first destination (will be passed from previous code)
#similarly, taking a specific example...
a1 = '6'
a3= '4'

av1 = '1'
av2 = '7'
a2 = '9'

#defining the node adjacency graph

graph = {'0': ['1', '5'],
             '1': ['2', '6', '0'],
         '2': ['1', '7', '3'],
             '3': ['2', '4', '8'],
             '4': ['9', '3'],
             '5': ['0', '10', '6'],
             '6': ['1','5', '7', '11'],
             '7': ['6','8', '12', '2'],
             '8': ['3','13', '7','9'],
         '9': ['8','4', '14'],
         '10': ['5', '11', '22'],
         '11': ['6','23', '12', '10'],
         '12': ['13','7', '24', '11'],
         '13': ['8','14','25','12'],
         '14': ['13','15','9','26'],
         '15': ['35','42','16','14'],
         '16': ['15','17','36','43'],
         '17': ['37','44','16','18'],
         '18': ['17','19','38','45'],
         '19': ['18','39','20','46'],
         '20': ['19','40','21','47'],
         '21': ['20','41','48'],
         '22': ['10','23'],
         '23': ['11','22','24'],
         
         '24': ['27','12','25','23'],
         '25': ['24','13','26'],
         '26' : ['25','14'],
         '27' : ['24'],


         '28': ['29','35'],
         '29': ['28','30','36'],
         '30': ['29','31','37'],
         '31': ['38','32','30'],
         '32': ['31','33','39'],
         '33': ['32','34','40'],
         
         '34': ['41','33'],
         '35': ['36','15','28'],
         '36': ['35','37','29','16'],
         '37': ['36','38','30','17'],
         '38': ['31','18','37','39'],
         '39': ['38','32','40','19'],
         '40': ['33','41','20','39'],
         '41': ['34','21','40'],
         '42': ['43','49','15'],
         '43': ['16','50','44','42'],
         
         '44': ['17','51','43','45'],
         '45': ['18','52','44','46'],
         '46': ['19','53','45','47'],
         '47': ['20','54','46','48'],
         '48': ['21','55','47'],
         '49': ['42','50'],
         '50': ['43','51','49'],
         '51': ['52','50','44'],
         '52': ['45','51','53'],
         '53': ['46','52','54'],
         
         '54': ['47','53','55'],
         '55': ['54','48']}


'''

* Function Name:	bfs
* Input:		graph-> adjacency list
                        start-> starting node
                        end-> ending node
* Output:		path array
* Logic:		Using BFS to find shortest path between nodes
* Example Call:	arr = bfs(graph, '14', '15')
*
'''



def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


'''
Multiple Routing Functions are defined here to find shortest paths between multiple nodes
'''

def routing1(source,dest):

    arr =  bfs(graph, source, '14')
    arr = map(int, arr)
    #print arr
    n= len(arr)

    my_list = list()

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')
                
    arr = bfs(graph, '14', '15')
    arr = map(int, arr)
    #print arr
    n= len(arr)

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')


    arr = bfs(graph, '15', dest)
    arr = map(int, arr)
    #print arr
    n= len(arr)

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')
    

    return my_list
##################################################CALL this to traverse from D2 to D1####################################
def routing2(source,dest):

    arr =  bfs(graph, source, '15')
    arr = map(int, arr)
    #print arr
    n= len(arr)

    my_list = list()

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')
                
    arr = bfs(graph, '15', '14')
    arr = map(int, arr)
    #print arr
    n= len(arr)

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')


    arr = bfs(graph, '14', dest)
    arr = map(int, arr)
    #print arr
    n= len(arr)

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')
        

    return my_list

'''
This function gives final complete path
'''

def first(a):
    
    arr =  bfs(graph, '27', a)
    arr = map(int, arr)
    #print arr
    n= len(arr)

    my_list = list()

    for i in range (0,n-1):
        
        if (arr[i]-arr[i+1]>0):
            if (arr[i]-arr[i+1] ==1):
                my_list.append('W')
            else:
                my_list.append('N')
        elif (arr[i]-arr[i+1]<0):
             if (arr[i]-arr[i+1] == -1):
                my_list.append('E')
             else :
                my_list.append('S')
    my_list.append('E')
    
    return my_list
n_ele_a =2
n_ele_b = 2
n_ele_c =2
n_ele_d2 = 3
b1 = '13'
bv1 = '6'
s2 = '47'
b2 = '14'
bv2 = '9'
s3 = '34'
c1 = '11'
cv1='6'
c2= '6'
cv2 = '1'
if (n_ele_d2 == 3):
    if (n_ele_a == 2 and n_ele_b == 2 and n_ele_c ==2):   
        #############for going to node from start position##############
        a1 = int(a1)
        
        p1 = first(str(a1-1))
        p1.append(av1)
        a1 = str(a1)
        #print 'path1 = ',p1
        s1 = int(s1)
        #############             for going to deposit zone from node   #################
        p2 = routing1(a1,str(s1-1))
        p2.append('E')
        p2.append('D')
        #print 'path 2 =',p2
        a2 = int(a2)
        ###############  for going to d1 from d2 ###############
        p3 = routing2(str(s1),str(a2-1))
        p3.append('E')
        p3.append(av2)
        #print 'path 3 = ',p3
        a2 = str(a2)
        ################for picking up next number ####################
        p4 = routing1(a2,str(s1-1))
        p4.append('E')
        p4.append('D')
        #print 'path 4 =',p4
        b1 = int(b1)
        p5 = routing2(str(s1),str(b1-1))
        p5.append('E')
        p5.append(bv1)
        #print 'path 5 = ',p5
        s2 = int(s2)
        p6 = routing1(str(b1),str(s2-1))
        p6.append('E')
        p6.append('D')
        #print 'path 6 =',p6
        b2 = int(b2)
        p7 = routing2(str(s2),str(b2-1))
        p7.append('E')
        p7.append(bv2)
        #print 'path 7 = ',p7
        s2 = int(s2)
        p8 = routing1(str(b2),str(s2-1))
        p8.append('E')
        p8.append('D')
        #print 'path 8 =',p8 
        c1 = int(c1)
        p9 = routing2(str(s2),str(c1-1))
        p9.append('E')
        p9.append(cv1)
        #print 'path 9 = ',p9
        s3 = int(s3)
        p10 = routing1(str(c1),str(s3-1))
        p10.append('E')
        p10.append('D')
        #print 'path 10 =',p10
        c2 = int(c2)
        p11 = routing2(str(s3),str(c2-1))
        p11.append('E')
        p11.append(cv2)
        #print 'path 11 = ',p11
        s3 = int(s3)
        p12 = routing1(str(c2),str(s3-1))
        p12.append('E')
        p12.append('D')
        p12.append('B')
        #print 'path 12 =',p12
        path = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12
        print 'path = ',path
        
    elif (n_ele_a == 3 and n_ele_b == 2 and n_ele_c ==2): ###100
        a1 = int(a1)
        
        p1 = first(str(a1-1))
        p1.append(av1)
        a1 = str(a1)
        #print 'path1 = ',p1
        s1 = int(s1)
        #############             for going to deposit zone from node   #################
        p2 = routing1(a1,str(s1-1))
        p2.append('E')
        p2.append('D')
        #print 'path 2 =',p2
        a2 = int(a2)
        ###############  for going to d1 from d2 ###############
        p3 = routing2(str(s1),str(a2-1))
        p3.append('E')
        p3.append(av2)
        #print 'path 3 = ',p3
        a2 = str(a2)
        ################for picking up next number ####################
        p4 = routing1(a2,str(s1-1))
        p4.append('E')
        p4.append('D')
        #print 'path 4 =',p4
        a3 = int(a3)
        ###############  for going to d1 from d2 ###############
        p5 = routing2(str(s1),str(a3-1))
        p5.append('E')
        p5.append(av3)
        #print 'path 3 = ',p3

        ## going from a3 to s1 ###
        p6 = routing1(str(a3),str(s1-1))
        p6.append('E')
        p6.append('D')
        
        ## going from s1 to b1 #######
        b1 = int(b1)
        p7 = routing2(str(s1),str(b1-1))
        p7.append('E')
        p7.append(bv1)
        #print 'path 5 = ',p5

        ## going from b1 to s2 ######
        s2 = int(s2)
        p8 = routing1(str(b1),str(s2-1))
        p8.append('E')
        p8.append('D')
        #print 'path 6 =',p6

        ##going from s2 to b2 ######
        b2 = int(b2)
        p9 = routing2(str(s2),str(b2-1))
        p9.append('E')
        p9.append(bv2)
        #print 'path 7 = ',p7

        ### going from b2 to s2 ###
        s2 = int(s2)
        p10 = routing1(str(b2),str(s2-1))
        p10.append('E')
        p10.append('D')
        #print 'path 8 =',p8

        ######## GOING FROM S2 TO C1 ##########
        c1 = int(c1)
        p11 = routing2(str(s2),str(c1-1))
        p11.append('E')
        p11.append(cv1)
        #print 'path 9 = ',p9

        ########## GOING FROM C1 TO S3 ########
        s3 = int(s3)
        p12 = routing1(str(c1),str(s3-1))
        p12.append('E')
        p12.append('D')
        #print 'path 10 =',p10

        ########### GOING FROM S3 TO C2 ###
        c2 = int(c2)
        p13 = routing2(str(s3),str(c2-1))
        p13.append('E')
        p13.append(cv2)
        #print 'path 11 = ',p11

        ############ GOING FROM C2 TO S3 ##
        s3 = int(s3)
        p14 = routing1(str(c2),str(s3-1))
        p14.append('E')
        p14.append('D')
        p14.append('B')        
        
        path = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14
        print 'path = ',path

    elif (n_ele_a == 3 and n_ele_b == 3 and n_ele_c ==2):
        a1 = int(a1)
        
        p1 = first(str(a1-1))
        p1.append(av1)
        a1 = str(a1)
        #print 'path1 = ',p1
        s1 = int(s1)
        #############             for going to deposit zone from node   #################
        p2 = routing1(a1,str(s1-1))
        p2.append('E')
        p2.append('D')
        #print 'path 2 =',p2
        a2 = int(a2)
        ###############  for going to d1 from d2 ###############
        p3 = routing2(str(s1),str(a2-1))
        p3.append('E')
        p3.append(av2)
        #print 'path 3 = ',p3
        a2 = str(a2)
        ################for picking up next number ####################
        p4 = routing1(a2,str(s1-1))
        p4.append('E')
        p4.append('D')
        #print 'path 4 =',p4
        a3 = int(a3)
        ###############  for going to d1 from d2 ###############
        p5 = routing2(str(s1),str(a3-1))
        p5.append('E')
        p5.append(av3)
        #print 'path 3 = ',p3

        ## going from a3 to s1 ###
        p6 = routing1(str(a3),str(s1-1))
        p6.append('E')
        p6.append('D')
        
        ## going from s1 to b1 #######
        b1 = int(b1)
        p7 = routing2(str(s1),str(b1-1))
        p7.append('E')
        p7.append(bv1)
        #print 'path 5 = ',p5

        ## going from b1 to s2 ######
        s2 = int(s2)
        p8 = routing1(str(b1),str(s2-1))
        p8.append('E')
        p8.append('D')
        #print 'path 6 =',p6

        ##going from s2 to b2 ######
        b2 = int(b2)
        p9 = routing2(str(s2),str(b2-1))
        p9.append('E')
        p9.append(bv2)
        #print 'path 7 = ',p7

        ### going from b2 to s2 ###
        s2 = int(s2)
        p10 = routing1(str(b2),str(s2-1))
        p10.append('E')
        p10.append('D')
        
        ### going from s2 to b3 ####
        b3 = int(b3)
        p11 = routing2(str(s2),str(b3-1))
        p11.append('E')
        p11.append(bv3)
        
        ### going from b3 to s2 ####
        s2 = int(s2)
        p12 = routing1(str(b3),str(s2-1))
        p12.append('E')
        p12.append('D')
        #print 'path 6 =',p6

        ### going from s2 to c1
        c1 = int(c1)
        p13 = routing2(str(s2),str(c1-1))
        p13.append('E')
        p13.append(cv1)
        #print 'path 9 = ',p9

        ########## GOING FROM C1 TO S3 ########
        s3 = int(s3)
        p14 = routing1(str(c1),str(s3-1))
        p14.append('E')
        p14.append('D')
        #print 'path 10 =',p10

        ########### GOING FROM S3 TO C2 ###
        c2 = int(c2)
        p15 = routing2(str(s3),str(c2-1))
        p15.append('E')
        p15.append(cv2)
        #print 'path 11 = ',p11

        ############ GOING FROM C2 TO S3 ##
        s3 = int(s3)
        p16 = routing1(str(c2),str(s3-1))
        p16.append('E')
        p16.append('D')
        p16.append('B')        
        
        path = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16
        print 'path = ',path
    
    elif(n_ele_a == 3 and n_ele_b == 3 and n_ele_c ==3):  ### 111
        a1 = int(a1)
        
        p1 = first(str(a1-1))
        p1.append(av1)
        a1 = str(a1)
        #print 'path1 = ',p1
        s1 = int(s1)
        #############             for going to deposit zone from node   #################
        p2 = routing1(a1,str(s1-1))
        p2.append('E')
        p2.append('D')
        #print 'path 2 =',p2
        a2 = int(a2)
        ###############  for going to d1 from d2 ###############
        p3 = routing2(str(s1),str(a2-1))
        p3.append('E')
        p3.append(av2)
        #print 'path 3 = ',p3
        a2 = str(a2)
        ################for picking up next number ####################
        p4 = routing1(a2,str(s1-1))
        p4.append('E')
        p4.append('D')
        #print 'path 4 =',p4
        a3 = int(a3)
        ###############  for going to d1 from d2 ###############
        p5 = routing2(str(s1),str(a3-1))
        p5.append('E')
        p5.append(av3)
        #print 'path 3 = ',p3

        ## going from a3 to s1 ###
        p6 = routing1(str(a3),str(s1-1))
        p6.append('E')
        p6.append('D')
        
        ## going from s1 to b1 #######
        b1 = int(b1)
        p7 = routing2(str(s1),str(b1-1))
        p7.append('E')
        p7.append(bv1)
        #print 'path 5 = ',p5

        ## going from b1 to s2 ######
        s2 = int(s2)
        p8 = routing1(str(b1),str(s2-1))
        p8.append('E')
        p8.append('D')
        #print 'path 6 =',p6

        ##going from s2 to b2 ######
        b2 = int(b2)
        p9 = routing2(str(s2),str(b2-1))
        p9.append('E')
        p9.append(bv2)
        #print 'path 7 = ',p7

        ### going from b2 to s2 ###
        s2 = int(s2)
        p10 = routing1(str(b2),str(s2-1))
        p10.append('E')
        p10.append('D')
        
        ### going from s2 to b3 ####
        b3 = int(b3)
        p11 = routing2(str(s2),str(b3-1))
        p11.append('E')
        p11.append(bv3)
        
        ### going from b3 to s2 ####
        s2 = int(s2)
        p12 = routing1(str(b3),str(s2-1))
        p12.append('E')
        p12.append('D')
        #print 'path 6 =',p6

        ### going from s2 to c1
        c1 = int(c1)
        p13 = routing2(str(s2),str(c1-1))
        p13.append('E')
        p13.append(cv1)
        #print 'path 9 = ',p9

        ########## GOING FROM C1 TO S3 ########
        s3 = int(s3)
        p14 = routing1(str(c1),str(s3-1))
        p14.append('E')
        p14.append('D')
        #print 'path 10 =',p10

        ########### GOING FROM S3 TO C2 ###
        c2 = int(c2)
        p15 = routing2(str(s3),str(c2-1))
        p15.append('E')
        p15.append(cv2)
        #print 'path 11 = ',p11

        ############ GOING FROM C2 TO S3 ##
        s3 = int(s3)
        p16 = routing1(str(c2),str(s3-1))
        p16.append('E')
        p16.append('D')
        ########### going from s3 to c3    
        c3 = int(c3)
        p17 = routing2(str(s3),str(c3-1))
        p17.append('E')
        p17.append(bv3)
        
        ### going from c3 to s3 ####
        s3 = int(s3)
        p18 = routing1(str(c3),str(s3-1))
        p18.append('E')
        p18.append('D')
        p18.append('B')
        #print 'path 6 =',p6

        path = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16
        print 'path = ',path #grand final path


length=len(path)

for i in range (0,length):
    
    ser.write(array[i])
    time.sleep(0.1) #bursting the data serially to firebird
