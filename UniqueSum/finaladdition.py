import itertools

D1=[3,1,5,5,9,2,7,6,8,4,0,0] #output of image processing algorithm
D2=[11,16,11,10]

D1_array = D1
D1_array = [x for x in D1 if x != 0] #removing zeros to avoid redundant pairs

number=[w for w in range(1,10) if D1.count(w)>1]#counting the number of times a digit is repeated  

solution = []

#for adding distinct solutions
def possible(testA,testB,testC,testD):
    if(len(D2)==3):
        solution.append(testA)
        solution.append(testB)
        solution.append(testC)

    if(len(D2)==4):
        solution.append(testA)
        solution.append(testB)
        solution.append(testC)
        solution.append(testD)
    solution.append('$')
    return solution

#checking for more than given number of digit repetitions
def screening(testA,testB,testC,testD):
    count=0
    if len(D2)==3:
       test = testA + testB + testC
    elif len(D2)==4:
       test = testA + testB + testC + testD
    for r in range(0,len(test)):
        for z in range(0,len(number)):
          if (test[r]==number[z]):
            count=count+1
          if (count>D1_array.count(number[z])):
            return 0
    return 1

#comparing pairs for near distinct solutions    
def compare(test1,test2):
    flag=0
    for p in range(0,len(test1)): #extracting columns of test1 for comparison
        for q in range(0,len(test2)): #extracting columns of test2 for comparison
            if (test1[p]==test2[q]):
                flag=flag+1
                for z in range(0,len(number)):
                    if(test1[p]==number[z]): #the repeated digit is to be excluded
                       flag=flag-1
    return flag

#forming addition pairs
def make_pairs(req_num):
 uniquelist = set(D1_array)
 #for n in itertools.combinations(uniquelist, 1): #single digit answer
  #if n[0] == req_num:                          ##giving error becuase its a integer value being compared as an array in compare()
    #pairs.append(n[0])
 for n in itertools.combinations(uniquelist, 2): #two digit pairs
    if n[0] + n[1] == req_num:
        pairs.append((n[0] , n[1]))
 for n in itertools.combinations(uniquelist, 3): #three digit pairs
    if n[0] + n[1] + n[2]== req_num:
        pairs.append(((n[0] , n[1], n[2])))
    if pairs == []:
       for n in itertools.combinations(uniquelist, 4): #if no two and three digit pairs find four digit pairs
        if n[0] + n[1] + n[2] + n[3]== req_num:
           pairs.append((((n[0] , n[1], n[2], n[3]))))
 return pairs


#Main function
for i in range(0,len(D2)): #generating pairs for different values of D2
    pairs=[]
    make_pairs(D2[i]);
    if i==0:
     answer0 = pairs
     print answer0
    if i==1:
     answer1 = pairs
     print answer1
    if i==2:
     answer2 = pairs
     print answer2
    if i==3:
     answer3 = pairs
     print answer3

if (len(D2)==3):
    for s in range(0,len(answer0)): #extracting rows of addition pairs
        testA = answer0[s]
        for j in range(0,len(answer1)):
            testB = answer1[j]
            for k in range(0,len(answer2)):
                testC = answer2[k]
                flag1=compare(testA,testB) #comaparing possible pairs for uniqueness 
                flag2=compare(testA,testC)
                flag4=compare(testB,testC)
                if(flag1==0 and flag2==0 and flag4==0):
                    allowed = screening(testA,testB,testC,0) #takes care of repeated digits
                    if allowed==1:
                        possible(testA,testB,testC,0) #appends the filtered outcomes
    print "Possible distinct solutions ",solution
    output1=solution[0] #ready to be sent to bfs
    output2=solution[1]
    output3=solution[2]
    print "Distinct Solution ",output1,output2,output3
    
if (len(D2)==4): #same procedure for 4 elements in D2
    for s in range(0,len(answer0)):
        testA = answer0[s]
        for j in range(0,len(answer1)):
            testB = answer1[j]
            for k in range(0,len(answer2)):
                testC = answer2[k]
                for l in range(0,len(answer3)):
                    testD = answer3[l]
                    flag1=compare(testA,testB)
                    flag2=compare(testA,testC)
                    flag3=compare(testA,testD)
                    flag4=compare(testB,testC)
                    flag5=compare(testB,testD)
                    flag6=compare(testC,testD)
                    if (flag1==0 and flag2==0 and flag3==0 and flag4==0 and flag5==0 and flag6==0):
                        allowed = screening(testA,testB,testC,testD)
                        if allowed==1:
                            possible(testA,testB,testC,testD)
    print "Possible distinct solutions ",solution
    output1=solution[0]
    output2=solution[1]
    output3=solution[2]
    output4=solution[3]
    print "Distinct Solution ",output1,output2,output3,output4


    
        
