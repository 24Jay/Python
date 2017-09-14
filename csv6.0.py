# 其中一个list名为original,用于保存初始数据，以便于查询名称
# 另外一个list名为result，用于在其中构建json格式数据


#统计每一行的级别，保存到rank中
def computeRank(fileName):
    lines = open(fileName)
    r = []
    for line in lines:
        line = line.replace("\n", "")
        lis= line.split(',')
        for i in range(len(lis)):
            if lis[i]=="":
                pass
            else:
                r.append(i)
                break
    return r




#对数据进行初步处理,另外一个构建json格式数据
def createJsonList(filepath):
    result=[]
    lines=open(filepath)
    for line in lines:
        # print(line)
        line=line.replace("\n","")
        spline = line.split(',')
        pline = line.split(',')

        for i in range(len(spline)-1):
            spline[i] = {spline[i]:[]}

        for i in range(len(spline)-1,0,-1):
            if spline[i-1]=={"":[]}:
                spline[i-1]=None
            else:
                string = str(pline[i-1])
                dictt = dict(spline[i-1])
                lis = list(dictt[string])
                lis.append(spline[i])
                dictt[string]=lis
                spline[i-1] = dictt
        result.append(spline)
    return  result



#构建一个original　list来保存各个位置的名词
def createOringalList(filepath):
    original=[]
    lines = open(filepath)
    for line in lines:
        line = line.replace("\n", "")
        pline = line.split(',')

        original.append(pline)
    return original


#找到每行数据的其父亲节点的位置
def findFather(num,rank):
    for i in range(num-1,-1,-1):
        if rank[num]>rank[i]:
            return i


#插入到父亲节点之后，父亲行的内容会发生变化，也需要更新
def updatFather(row,column,rankOfFather,original,result,rank):
    # print("updateFather Row!")
    if(rankOfFather == column):
        return
    for i in range(column,rankOfFather,-1):
        if result[row][i-1]==None:
            pass
        else:
            #父亲节点的名称和内容
            fa_name = str(original[row][i-1])
            fa_dict = dict(result[row][i-1])

            #子节点的名称和内容
            son_name = str(original[row][i])
            son = result[row][i]

            fa_dict_list = list(fa_dict[fa_name])
            for en in fa_dict_list:
                old_dict = dict(en)
                if old_dict.__contains__(son_name):
                    # print("You got it")
                    fa_dict_list.remove(en)
            fa_dict_list.append(son)
            fa_dict[fa_name]=fa_dict_list
            # print(">>>>>>>>" + str(fa_dict))
            result[row][i-1] = fa_dict
    # print(result)




#在result中构建json格式的数据
def createResult(rank,result,original):
    num=len(rank)-1
    for line in reversed(result):
        if num==0:
            break
        # print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< "+str(num),end="\n")

        lis=list(line)
        son = line[rank[num]]
        # print(son)
        fatherRow= findFather(num,rank)
        fatherCol= rank[num]-1

        father = result[fatherRow][fatherCol]
        father = dict(father)
        va = original[fatherRow][fatherCol]
        lisf = list(father[va])
        lisf.append(son)
        father[va]=lisf

        result[fatherRow][fatherCol]=father
        updatFather(fatherRow,fatherCol,rank[fatherRow],original,result,rank)

        num=num-1
    return result[0][0]



def csv2json(filepath):
    #保存每行的数据级别
    rank = computeRank(filepath)
    original = createOringalList(filepath)
    result = createJsonList(filepath)
    # print("rank = "+str(rank))
    # print("orig = "+str(original))
    # print("result = "+str(result))
    jsonList = createResult(rank,result,original)
    # print("\nGET FINAL RESULT:\n")
    print(jsonList)
    return jsonList


csv2json("his.csv")