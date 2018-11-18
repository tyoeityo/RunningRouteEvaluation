#coding:utf-8
#输入location_EachArea_x[i]（第i+1个区域的全部端点的x坐标）
#输入location_EachArea_y[i]（第i+1个区域的全部端点的y坐标）
#判断用户所点的坐标的所属区域并给出评价结果
#输出所属区域及评价结果
#判断用户所点坐标的所属区域
#用户点在区域的边上时判断为在区域外部

def judge_area(polyCorners,location_EachArea_x,location_EachArea_y,location_user_x,location_user_y):
    l = 0
    m = polyCorners-1
    x = 0
    num_cross = 0

    max_x = max(location_EachArea_x)
    min_x = min(location_EachArea_x)
    max_y = max(location_EachArea_y)
    min_y = min(location_EachArea_y)

    if location_user_x < min_x or location_user_x > max_x or location_user_y < min_y or location_user_y > max_y:
        return False   
    
    for l in range(polyCorners):
        if location_EachArea_y[l] == location_EachArea_y[m]: #射线与区域边界重合，此处不应计数
            m = l
            continue
        if location_user_y < min(location_EachArea_y[l],location_EachArea_y[m]):
            m = l
            continue
        if location_user_y > max(location_EachArea_y[l],location_EachArea_y[m]):
            m = l
            continue

        x = (location_user_y-location_EachArea_y[m])*(location_EachArea_x[l]-location_EachArea_x[m])/(location_EachArea_y[l]-location_EachArea_y[m])+location_EachArea_x[m]
        if x > location_user_x: #从用户点处画水平线 计算在用户点右边与区域边相交的点数
            num_cross += 1
        m = l
    
    if num_cross%2 == 1:
        return True
    else:
        return False
