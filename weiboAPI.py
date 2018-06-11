#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySqlService as MS
import json
import time
import hashlib

global ms

dbName = "lzhweibotest"


################################################################################################################################################
#接口函数,此范围内的函数为直接接口函数,为外部允许调用的方法

# 登陆函数，传入用户名与密码，返回网络反馈(Json 格式)
def login(loginStr, passwd):
    global ms
    requestType = "login"
    userID = 0
    # 假设 loginStr  中存储的是用户 id
    loginState = ms.select("SELECT user_password FROM UserTable WHERE user_id=%s;" %str(loginStr))
    if( bool(loginState)==True ):
        userID = int(loginStr)
    if( bool(loginState)==False ):
        print("正在尝试使用用户名进行登陆")
        loginState = ms.select("SELECT user_password FROM UserTable WHERE user_name='%s';" %str(loginStr))
        if( bool(loginState)==True ):
            userID = ms.select("SELECT user_id FROM UserTable WHERE user_name='%s';" %str(loginStr))[0][0]

    # 查无此人
    if( bool(loginState)==False ):
        print("该用户不存在")
        userID = -1
        return getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"用户不存在"})
    
    print(loginState, userID)
    if( loginState[0][0] == passwd ):
        print('登陆成功')
        return getResponseJson(requestType, {"isSuccess":"TRUE", "username":getUsernameByID(userID), "userID":str(userID), "user_enroll_time":getEnrollTimeByID(userID), "user_sexual":getSexualByID(userID), "user_introduction":getIntroductionByID(userID), "user_email":getEmailByID(userID)})

# 注册函数, 传入用户名,密码,时间,验证码,性别,用户简介,用户邮箱等信息后,反馈网络格式( JSON 格式)
def enroll(userName='', passwdMD5='', time='', check='', sexual='', introduction='', email=''):
    global ms
    requestType = "enroll"
    doesTheNameExisted = bool( ms.select("SELECT user_name FROM UserTable WHERE user_name='%s';" %str(userName)) )
    if(doesTheNameExisted):
        #已存在该用户名
        return getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":" 该用户名已被占用"})
    
    ms.insert( "INSERT INTO UserTable VALUES(%s, '%s', '%s', '%s', %s, '%s', '%s');" % ("NULL", passwdMD5, userName, time, sexual, introduction, email) )
    userID = ms.select("SELECT user_id FROM UserTable WHERE user_name='%s';" %str(userName))[0][0]
    return getResponseJson(requestType, {"isSuccess":"TRUE", "responseNumber":userName, "userID":str(userID), "user_enroll_time":time, "user_sexual":sexual, "user_introduction":introduction, "user_email":email})


# 按照时序获取微博
def checkByTime(requestNumber, userID):
    global ms
    requestType = "checkByTime"
    weiboList = ms.select("SELECT * FROM WeiboTable ORDER BY weibo_id DESC LIMIT %s;" %str(requestNumber))
    likeList = ms.select("SELECT * FROM AgreeTable WHERE user_id=%s;"%str(userID) )
    userLikeList = []
    for i in likeList:
        userLikeList.append( str(i[0]) ) 

    weiboDict = {}
    for i in range(len(weiboList)):
        userLiked = 'TRUE' if ( str(weiboList[i][0]) in userLikeList ) else "FALSE"
        weiboDict[str(i)] = str('{"weiboID":"%s", "userID":"%s", "userName":"%s", "weiboTime":"%s", "weiboDetail":"%s", "commentNumber":"%s", "agreeNumber":"%s", "liked":"%s"}'%(weiboList[i][0], weiboList[i][1], getUsernameByID(weiboList[i][1]), weiboList[i][3], weiboList[i][2], weiboList[i][4], weiboList[i][5], userLiked))

    weiboListJson = json.dumps(weiboDict, ensure_ascii=False)
    response = getResponseJson(requestType, {"isSuccess":"TRUE", "responseNumber":str(len(weiboList)), "weiboList":weiboListJson})
    return response

#  按照热度获取微博
def checkByAgreement(requestNumber):
    global ms
    requestType = "checkByAgreement"
    weiboList = ms.select("SELECT * FROM WeiboTable ORDER BY weibo_agree_number DESC LIMIT %s;" %str(requestNumber))
    weiboDict = {}
    for i in range(len(weiboList)):
        weiboDict[str(i)] = str('{"weiboID":"%s", "userID":"%s", "userName":"%s", "weiboTime":"%s", "weiboDetail":"%s", "commentNumber":"%s", "agreeNumber":"%s"}'%(weiboList[i][0], weiboList[i][1], getUsernameByID(weiboList[i][1]), weiboList[i][3], weiboList[i][2], weiboList[i][4], weiboList[i][5]))

    weiboListJson = json.dumps(weiboDict, ensure_ascii=False)
    response = getResponseJson(requestType, {"isSuccess":"TRUE", "responseNumber":str(len(weiboList)), "weiboList":weiboListJson})
    return response


# 发布新微博
def publishNewWeibo(userID, detail):
    global ms
    requestType = "publishNewWeibo"
    publishedTime = getStandardTime()
    ms.insert( "INSERT INTO WeiboTable VALUES(%s, %s, '%s', '%s', %s, %s);"%('NULL', str(userID), str(detail), publishedTime, str(0), str(0)) )
    weiboID = ms.select("SELECT weibo_id FROM WeiboTable WHERE user_id=%s AND weibo_published_time='%s';" %(str(userID), publishedTime))[0][0]
    return getResponseJson(requestType, {"isSuccess":"TRUE", "weiboID":weiboID})

    

# 发布新评论
def commentWeibo(userID, weiboID, commentDetail):
    global ms
    requestType = "commentWeibo"
    publishedTime = getStandardTime()
    ms.insert( "INSERT INTO CommentTable VALUES(%s, %s, %s, '%s', '%s');"%('NULL', str(weiboID), str(userID), commentDetail, publishedTime ) )
    commentID = ms.select("SELECT comment_id FROM CommentTable WHERE user_id=%s AND comment_published_time='%s';" %(str(userID), publishedTime))[0][0]
    numberOfComment = json.loads(json.loads(checkComments(weiboID))['response'])['responseNumber']
    updateWeibo = ms.updateDatabase("UPDATE WeiboTable SET weibo_comment_number=%s WHERE weibo_id=%s"%(str(numberOfComment), str(weiboID)))
    return getResponseJson( requestType, {"isSuccess":"TRUE", "weiboID":str(weiboID), "numberOfComments":str(numberOfComment)} )


# 点赞
def agreeWeibo(userID, weiboID):
    global ms
    requestType = "agreeWeibo"
    #publishedTime = getStandardTime()
    likeRequest = ms.insert( "INSERT INTO AgreeTable VALUES(%s, %s);"%(str(weiboID), str(userID) ) )
    likeList = ms.select("SELECT * FROM AgreeTable WHERE weibo_id=%s;"%str(weiboID) )
    numberOfLike = len(likeList)
    updateWeibo = ms.updateDatabase("UPDATE WeiboTable SET weibo_agree_number=%s WHERE weibo_id=%s"%(str(numberOfLike), str(weiboID)))

    rep = ''
    if(likeRequest and updateWeibo):
        rep = getResponseJson( requestType, {"isSuccess":"TRUE", "weiboID":str(weiboID), "numberOfAgreement":str(numberOfLike)} )
    else:
        rep = getResponseJson( requestType, {"isSuccess":"FALSE", "weiboID":str(weiboID), "numberOfAgreement":str(numberOfLike)} )
    return rep


# 查看评论
def checkComments(weiboID):
    global ms
    requestType = "checkComments"
    #publishedTime = getStandardTime()
    commentList = ms.select("SELECT * FROM CommentTable WHERE weibo_id=%s ORDER BY comment_id DESC;"%str(weiboID) )
    commentDic = {}
    for i in range(len(commentList)):
        commentDic[str(i)] = str('{"userID":"%s", "userName":"%s", "weiboID":"%s", "commentDetail":"%s", "commentTime":"%s", "commentID":"%s"}'%(commentList[i][2], getUsernameByID(commentList[i][2]), commentList[i][1], commentList[i][3], commentList[i][4], commentList[i][0]))

    commentListJson = json.dumps(commentDic, ensure_ascii=False)
    response = getResponseJson(requestType, {"isSuccess":"TRUE", "responseNumber":str(len(commentList)), "commentList":commentListJson})
    return response

#删除微博
def deleteWeibo(weiboID):
    global ms
    requestType = "deleteWeibo"

    #删除评论池中,所有关于该微博ID的评论
    deleteCommentRequest = ms.deleteTuple('CommentTable', 'weibo_id=%s'%(str(weiboID)) )
    #删除点赞池中,所有关于该微博ID的点赞记录
    deleteLikeRequest = ms.deleteTuple('AgreeTable', 'weibo_id=%s'%(str(weiboID)) )
    #从微博池中,删除该条微博
    deleteWeiboRequest = ms.deleteTuple('WeiboTable', 'weibo_id=%s'%(str(weiboID)) )

    if(deleteCommentRequest and deleteLikeRequest and deleteWeiboRequest):
        rep = getResponseJson( requestType, {"isSuccess":"TRUE", "weiboID":str(weiboID)} )
    else:
        rep = getResponseJson( requestType, {"isSuccess":"FALSE", "weiboID":str(weiboID)} )
    return rep
    pass


#删除评论
def deleteComment(commentID, weiboID):
    global ms
    requestType = "deleteComment"
    deleteCommentRequest = ms.deleteTuple('CommentTable', 'comment_id=%s AND weibo_id=%s'%(str(commentID), str(weiboID)) )
    commentList = ms.select("SELECT * FROM CommentTable WHERE weibo_id=%s;"%str(weiboID) )
    numberOfComment = len(commentList)
    updateWeibo = ms.updateDatabase("UPDATE WeiboTable SET weibo_comment_number=%s WHERE weibo_id=%s"%(str(numberOfComment), str(weiboID)))
    rep = ''
    if(deleteCommentRequest and updateWeibo):
        rep = getResponseJson( requestType, {"isSuccess":"TRUE", "weiboID":str(weiboID), "numberOfComments":str(numberOfComment)} )
    else:
        rep = getResponseJson( requestType, {"isSuccess":"FALSE", "weiboID":str(weiboID), "numberOfComments":str(numberOfComment)} )
    return rep


#取消点赞
def disagreeWeibo(weiboID, userID):
    global ms
    requestType = "disagreeWeibo"
    #publishedTime = getStandardTime()
    dislikeRequest = ms.deleteTuple('AgreeTable', 'weibo_id=%s AND user_id=%s'%(str(weiboID), str(userID)) )

    likeList = ms.select("SELECT * FROM AgreeTable WHERE weibo_id=%s;"%str(weiboID) )
    numberOfLike = len(likeList)
    updateWeibo = ms.updateDatabase("UPDATE WeiboTable SET weibo_agree_number=%s WHERE weibo_id=%s"%(str(numberOfLike), str(weiboID)))

    rep = ''
    if(dislikeRequest and updateWeibo):
        rep = getResponseJson( requestType, {"isSuccess":"TRUE", "weiboID":str(weiboID), "numberOfAgreement":str(numberOfLike)} )
    else:
        rep = getResponseJson( requestType, {"isSuccess":"FALSE", "weiboID":str(weiboID), "numberOfAgreement":str(numberOfLike)} )
    return rep
    pass

'''

#获取反馈的 JSON 列表
#requestType:请求类型
#response:反馈数据
def getResponseJson(requestType, response):

#获取标准格式时间
#'2018-05-27 22:41:14'
def getStandardTime():

#获取验证码
#验证规则:请求信息字符串与标准时间字符串进行连接后,计算 MD5值全部大写,最后取 MD5值的后5位再做 MD5运算.
def getCheckCode(request, time):

def getMD5(s):
'''

################################################################################################################################################
# 以下是 UserTable 的 get 方法

#通过 用户ID 获取用户名
#eg:'用户1'
def getUsernameByID(userID):
    global ms
    userName = ms.select("SELECT user_name FROM UserTable WHERE user_id=%s;" %str(userID))
    userName = userName[0][0]
    return str(userName)

#通过 用户ID 获取用户注册时间
#eg:'2018-5-27 15:01:00'
def getEnrollTimeByID(userID):
    global ms
    enrollTime = ms.select("SELECT user_enroll_time FROM UserTable WHERE user_id=%s;" %str(userID))
    enrollTime = enrollTime[0][0]
    return str(enrollTime)

#通过 用户ID 获取用户性别
#eg:'1'(0 = 女;1 = 男)
def getSexualByID(userID):
    global ms
    sexual = ms.select("SELECT user_sexual FROM UserTable WHERE user_id=%s;" %str(userID))
    sexual = sexual[0][0]
    return str(sexual)

#通过 用户ID 获取用户简介
#eg:'用户1介绍'
def getIntroductionByID(userID):
    global ms
    introduction = ms.select("SELECT user_introduction FROM UserTable WHERE user_id=%s;" %str(userID))
    introduction = introduction[0][0]
    introduction = introduction.encode("utf8")
    return str(introduction)

#通过 用户ID 获取用户邮箱
#eg:'example1@scuweibo.com'
def getEmailByID(userID):
    global ms
    email = ms.select("SELECT user_email FROM UserTable WHERE user_id=%s;" %str(userID))
    email = email[0][0]
    return str(email)


################################################################################################################################################
# 以下是 WeiboTable 的 get方法

#通过 微博ID 获取用户id
def getUserIDByWeiboID(weiboID):
    global ms
    userID = ms.select("SELECT user_id FROM WeiboTable WHERE weibo_id=%s;" %str(weiboID))
    userID = userID[0][0].encode('utf8')
    return str(userID)

#通过 微博ID 获取微博详情
def getWeiboDetailByWeiboID(weiboID):
    global ms
    userID = ms.select("SELECT user_id FROM WeiboTable WHERE weibo_id=%s;" %str(weiboID))
    userID = userID[0][0]
    return str(userID)

#通过 微博ID 获取微博公布时间
def getWeiboPublishedTimeByWeiboID(weiboID):
    pass

#通过 微博ID 获取评论数
def getCommentNumberByWeiboID(weiboID):
    pass

#通过 微博ID 获取点赞数
def getAgreeNumberByWeiboID(weiboID):
    pass

#通过 微博ID 获取用户昵称
def getUsernameByWeiboID(weiboID):
    pass

################################################################################################################################################
# 以下是常用接口函数.

#获取反馈的 JSON 列表
#requestType:请求类型
#response:反馈数据
def getResponseJson(requestType, response):
    response = json.dumps(response, ensure_ascii=False)
    
    time = getStandardTime()
    dic = {"request":requestType, "time":time, "check":getCheckCode(requestType, time), "response":response}
    return json.dumps(dic, ensure_ascii=False)


#获取标准格式时间
#'2018-05-27 22:41:14'
def getStandardTime():
    return str( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )


#获取验证码
#验证规则:请求信息字符串与标准时间字符串进行连接后,计算 MD5值全部大写,最后取 MD5值的后5位再做 MD5运算.
def getCheckCode(request, time):
    linker = str(request) + str(time)
    checkSource = getMD5(linker)
    ans = getMD5(checkSource[-5:])
    return ans

def getMD5(s):
    return str( hashlib.md5(str(s).encode('utf-8')).hexdigest().upper() )

################################################################################################################################################


def startDataBaseService():
    global ms
    print("ServiceStart!")
    ms = MS.MySqlService(dbName)


if __name__ == '__main__':
    global ms
    print("ServiceStart!")
    ms = MS.MySqlService(dbName)
    login('用户1', 'password')
    #disagreeWeibo(28, 3)
    deleteComment(28, 28)


'''

def login(user, passwd):
    global ms
    loginMode = {'LoginByID':0, 'LoginByUserName':1}
    
    ans = ms.select("SELECT passwd FROM users WHERE ID=%s;" %str(user))
    mode = 0
    if ans == False:
        ans = ms.select("SELECT passwd FROM users WHERE username='%s';" %str(user))
        mode = 1
    
    if ans[0][0] == passwd:
        CURR_USER_NAME = (ms.select("SELECT username FROM users WHERE ID=%s;" %str(user))[0][0] if mode == 0 else user)
        CURR_USER_ID   = (ms.select("SELECT id FROM users WHERE username='%s';" %str(user))[0][0] if mode == 1 else user)
        return True
    return False

def addDiary(diary):
    global ms
    cursor = ms.db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT MAX(diaryID) FROM diary;")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()[0]
    ms.insert( "INSERT INTO diary VALUES(%s, %s, NOW(), '%s');" % (int(data)+1, str(CURR_USER_ID), diary) )


def addUser(userName, passwd, sex):
    global ms
    cursor = ms.db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT MAX(id) FROM users;")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()[0]
    sex = 'true' if sex == 'Male' else "false"
    ms.insert( "INSERT INTO users VALUES(%s, '%s', '%s', %s);" % (int(data)+1, userName, passwd, sex) )

def viewDiary():
    global ms
    global CURR_USER_ID
    if (CURR_USER_ID==None):
        return "Please Login"
    ans = ms.select("SELECT diaryID, time, data FROM diary WHERE userID=%s;" %str(CURR_USER_ID))
    return ans


def deleteDiary(diaryID):
    global ms
    global CURR_USER_ID
    if (CURR_USER_ID==None):
        return "Please Login"
    ans = ms.deleteTuple('diary', "diaryID = %s"%str(diaryID))
    return True

def editDiary(diaryID, newDiary):
    global ms
    global CURR_USER_ID
    if (CURR_USER_ID==None):
        return "Please Login"
    ans = ms.updateDatabase("UPDATE diary SET data = '%s', time = NOW() WHERE diaryID=%s" % (newDiary, str(diaryID)) )
    print("UPDATE diary SET data = '%s' WHERE userID=%s" % (newDiary, str(CURR_USER_ID)) )
    return ans


'''





    

