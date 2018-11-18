#coding:utf-8
import os
import JudgeArea

#读取文件（各区域编号 评价分数 评价结果（Good Normal Bad））
test_file = open('area_evaluation.txt','r')
area_ID = []
area_point = []
area_evaluation = []
for line in test_file.readlines():
    line_split = line.split()
    area_ID.append(line_split[0])
    area_point.append(line_split[1])
    area_evaluation.append(line_split[2])

test_file.close()

#locate-xy文件夹与程序放入同一文件夹中 读取locate-xy文件夹中各区域端点坐标txt文件并合并存入locate_xy_all.txt  
path = 'C:\\Users\\eityo\\Desktop\\Running_Route\\locate-xy' 
filenames = os.listdir(path) #filenames为包含文件夹内所有文件的文件名的列表
filenames = sorted(filenames,key=len) #文件名排序（先按key值长度排序）
file_in_one = open('locate_xy_all.txt','w') #创建locate_xy_all.txt

for filename in filenames:
    filepath = path + '\\' + filename
    for line in open(filepath,'r'):
        file_in_one.writelines(line)
    file_in_one.write('\n')

file_in_one.close()

test_file = open('locate_xy_all.txt','r') 
num_area = 0 #记录区域数
num_points = 0 #记录一个区域的端点数
num_EdgePoint = [] #记录每个区域的端点数
location_EdgePoint = [] #记录每个区域的端点坐标 
location_EachArea_x = [] #记录每个区域的端点x坐标 location_EachArea[0]记录第一个区域的全部端点的x坐标 ...
location_EachArea_y = [] #记录每个区域的端点x坐标 location_EachArea[0]记录第一个区域的全部端点的y坐标 ...

for line in test_file.readlines():
    if line == '\n':
        num_EdgePoint.append(num_points)
        num_points = 0
        num_area += 1
        continue        
    location_EdgePoint.append(line.strip().split(','))
    num_points += 1

test_file.close()

#将location_EdgePoint按对应区域分块 对应区域的所有端点的x坐标存入location_EachArea_x 对应区域的所有端点的y坐标存入location_EachArea_y
a = []
b = []
num_EP_EachArea = 0 
index = 0

for j in range(len(location_EdgePoint)):
    a.append(location_EdgePoint[j][0]) #端点的x坐标
    b.append(location_EdgePoint[j][1]) #端点的y坐标
    num_EP_EachArea += 1
    if num_EP_EachArea == num_EdgePoint[index]: #当a列表的元素数等于对应区域的端点数（由列表num_EdgePoint存储）时将其一并作为一个元素存入列表b
        location_EachArea_x.append(a)
        location_EachArea_y.append(b)
        a = []
        b = []
        num_EP_EachArea = 0
        index += 1

#读取文件（用户所点坐标）
location_user = []    # location of user points  
location_user_x = []  # latitude of user points 
location_user_y = []  # longitude of user points

test_file = open('userpoint.txt','r')  
for line in test_file.readlines():
    location_user.append(line.replace('(','').replace(')','').strip().split(','))

location_user_x = [float(location_user[i][0]) for i in range(len(location_user))]
location_user_y = [float(location_user[i][1]) for i in range(len(location_user))]

#判断用户所点坐标的所属区域
location_judge = []
result_list = []
badpoint_list = []
result = False
index_True = 0

for i in range(len(location_user)): #一共有len(location_user)个用户点 i表示第i+1个用户点
    for j in range(num_area): #一共有len(num_area)个区域j表示第j+1个区域
        result = JudgeArea.judge_area(num_EdgePoint[j],list(map(float,location_EachArea_x[j])),list(map(float,location_EachArea_y[j])),location_user_x[i],location_user_y[i])
        result_list.append(result)
        if result == True:
            if area_evaluation[j] == 'Bad':
                location_judge.append([location_user_x[i],location_user_y[i],area_ID[j],area_evaluation[j]])
                badpoint_list.append([location_user_x[i],location_user_y[i],area_evaluation[j]])
                print('Location {0}, {1} is Bad!'.format(location_user_x[i],location_user_y[i]))
            else:
                location_judge.append([location_user_x[i],location_user_y[i],area_ID[j],area_evaluation[j]])

    if True not in result_list:
        location_judge.append([location_user_x[i],location_user_y[i],'Not included in any area','No evaluation'])   

    result_list = []            
                
test_file.close()

#创建用户点环境评价txt文件（用户点x坐标 用户点y坐标 所属区域 环境评价）
test_file = open('userpoint_evaluation.txt','w')
for line in location_judge:
    strline = str(line)
    strline = strline.replace('[','').replace(']','')
    test_file.write('{0}\n'.format(strline))

test_file.flush()
test_file.close()

#环境评价结果为差的用户点放入txt文件（用户点x坐标 用户点y坐标 环境评价='Bad'）
test_file = open('bad_userpoint.txt','w')
for line in badpoint_list:
    strline = str(line)
    strline = strline.replace('[','').replace(']','')
    test_file.write('{0}\n'.format(strline))

test_file.flush()
test_file.close()

#评价路径
route_point = 0
for i in range(len(location_judge)):
    if location_judge[i][3] == 'Good':
        route_point += 8
    elif location_judge[i][3] == 'Normal':
        route_point += 6
    elif location_judge[i][3] == 'Bad':
        route_point += 2
    else:
        print(location_judge[i])
route_point_average = route_point/len(location_user)

print('Score of running route is %.4f' %route_point_average)
