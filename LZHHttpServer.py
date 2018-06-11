#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = '__Lizhenghao__'


from  http.server import HTTPServer,BaseHTTPRequestHandler  
import chardet
import sys
import urllib

import weiboAPI

  
class ServerHTTP(BaseHTTPRequestHandler):
    #处理GET请求
    def do_GET(self):  
        path = self.path
        #将获url解析成utf-8编码格式
        requestUTF = urllib.parse.unquote(path)

        res = ''
        try:
            #分离请求头
            requestType = requestUTF.split('?')[0][1:]
            #分离参数至字典
            argvs = requestUTF.split('?')[1]
            argvs = urllib.parse.parse_qs(argvs)
            print('requestType = '+requestType, type(argvs), argvs)
            if( requestType ==  'login'):
                #接收到登陆请求
                pass
            
            elif( requestType ==  'enroll' ):
                #接收到注册请求
                pass
            
            elif( requestType ==  'checkByTime' ):
                #接收到时序查看微博请求
                #checkByTime?userID=[用户id]&time=[时间]&check=[验证码]&requestNumber=[请求微博数]
                print("正在按时序查看微博")
                try:
                    userID = argvs['userID'][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    requestNumber = argvs['requestNumber'][0]
                    
                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        #请求哈希验证通过
                        try:
                            print("正在按照时序查看微博中........")
                            res = weiboAPI.checkByTime(int(requestNumber), userID)
                        except:
                            #requestNumber样式不正确,请求遭到攻击!
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})

                    else:
                        #请求哈希验证不通过,请求遭到攻击!
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"哈希验证失败,请求失败!"})
                except:
                    #请求数据格式错误,请求遭到攻击!
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"请求遭受攻击,参数异常!"})


                
            
            elif( requestType ==  'checkByAgreement' ):
                #接收到按热度查看微博请求
                #checkByAgreement?userID=[用户id]&time=[时间]&check=[验证码]&requestNumber=[请求微博数]
                print("正在按热度查看微博")
                try:
                    userID = argvs['userID'][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    requestNumber = argvs['requestNumber'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            #请求哈希验证通过 
                            print("正在按照热度查看微博中........")
                            res = weiboAPI.checkByAgreement(int(requestNumber))
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        #请求哈希验证不通过,请求遭到攻击!
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"哈希匹配失败"})
                except:
                    #请求数据格式错误,请求遭到攻击!
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数丢失"})
                pass
            
            elif( requestType ==  'publishNewWeibo' ):
                #接收到发布新微博请求
                print("正在向数据库中添加微博")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    detail = argvs['detail'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            #print(userID + '\n' + time + '\n' + check + '\n' + detail + '\n')
                            print("验证通过，正在添加微博")
                            res = weiboAPI.publishNewWeibo(userID, detail)
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止微博发送')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止微博发送')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                pass
            
            elif( requestType ==  'agreeWeibo' ):
                #接收到点赞请求
                #agreeWeibo?userID=[用户id]&time=[时间]&check=[验证码]&weiboID=[微博编号]
                print("正在响应点赞微博请求")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    weiboID = argvs['weiboID'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            print("验证通过，正在点赞微博")
                            res = weiboAPI.agreeWeibo(userID, weiboID)
                            ############################################################################################################
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止微博发送')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止微博发送')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                pass
            
            elif( requestType ==  'commentWeibo' ):
                #接收到评论微博请求
                #commentWeibo?userID=[用户id]&time=[时间]&check=[验证码]&weiboID=[微博编号]&commentDetail=[评论详情]
                print("正在响应添加评论请求")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    weiboID = argvs['weiboID'][0]
                    commentDetail = argvs['commentDetail'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            #print(userID + '\n' + time + '\n' + check + '\n' + detail + '\n')
                            print("验证通过，正在评论微博")
                            res = weiboAPI.commentWeibo(userID, weiboID, commentDetail)
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止微博发送')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止微博发送')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                pass
            
            elif( requestType ==  'checkComments' ):
                #接收到查看评论请求
                #checkComments?userID=[用户id]&time=[时间]&check=[验证码]&weiboID=[微博编号]
                print("正在检索微博下方评论")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    weiboID = argvs['weiboID'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            #print(userID + '\n' + time + '\n' + check + '\n' + detail + '\n')
                            print("验证通过，检索评论")
                            res = weiboAPI.checkComments(weiboID)
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止微博发送')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止微博发送')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                
                pass
            
            elif( requestType ==  'deleteWeibo' ):
                #接收到删除微博请求
                #deleteWeibo?userID=[用户id]&time=[时间]&check=[验证码]&weiboID=[微博编号]
                print("正在响应取删除微博请求")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    weiboID = argvs['weiboID'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            print("验证通过，正在删除微博")
                            res = weiboAPI.deleteWeibo(weiboID)
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止删除微博')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止删除微博')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                pass
            
            elif( requestType ==  'deleteComment' ):
                #接收到删除评论请求
                #deleteComment?userID=[用户id]&time=[时间]&check=[验证码]&commentID=[评论编号]&weiboID=[微博ID]
                print("正在响应取删除评论请求")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    commentID = argvs['commentID'][0]
                    weiboID = argvs['weiboID'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            print("验证通过，正在取消点赞微博")
                            res = weiboAPI.deleteComment(commentID, weiboID)
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止取消点赞')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止取消点赞')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                pass
            
            elif( requestType ==  'disagreeWeibo' ):
                #接收到删除点赞请求
                #disagreeWeibo?userID=[用户id]&time=[时间]&check=[验证码]&weiboID=[微博编号]
                print("正在响应取消点赞微博请求")
                try:
                    #获取发送微博所需的参数
                    userID = argvs["userID"][0]
                    time = argvs['time'][0]
                    check = argvs['check'][0]
                    weiboID = argvs['weiboID'][0]

                    if(check == weiboAPI.getCheckCode(requestType, time)):
                        try:
                            print("验证通过，正在取消点赞微博")
                            res = weiboAPI.disagreeWeibo(weiboID, userID)
                        except:
                            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"向服务器请求数据失败,请联系管理员!"})
                    else:
                        print('验证码验证不匹配，终止取消点赞')
                        res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"验证码不匹配"})
                except:
                    print('发送微博过程中检测到参数错误，终止取消点赞')
                    res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"参数错误"})
                pass

            else:
                print("请求头错误!")
                res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"请求遭到攻击,请求头不存在!"})

            
        except:
            print("请求过程中出现错误!")
            res = weiboAPI.getResponseJson(requestType, {"isSuccess":"FALSE" ,"error":"请求过程中服务器出现未知错误,请联系系统管理员!"})
        
        #发送请求信息
        #设置状态响应码为200
        self.send_response(200)
        #发送请求头
        self.send_header("Content-type","text/html")  
        #self.send_header("test","This is test!")  
        self.end_headers()  
        buf = res

        #输出响应内容
        self.wfile.write(buf.encode(encoding="utf-8"))

    #处理POST请求
    def do_POST(self):  
        path = self.path  
        print("POST_------------------------_"+str(path))
        #获取post提交的数据  
        datas = self.rfile.read(int(self.headers['content-length']))  
        datas = datas.decode("utf-8", 'ignore')
          
        self.send_response(200)  
        self.send_header("Content-type","text/html")  
        self.send_header("test","This is test!")  
        self.end_headers()  
        buf = '''<!DOCTYPE HTML> 
        <html> 
            <head><title>Post page</title></head> 
            <body>Post Data:%s  <br />Path:%s</body> 
        </html>'''%(datas,self.path)  
        self.wfile.write(buf.encode(encoding="utf-8"))  


#开启http服务
def start_server(port):
    http_server = HTTPServer(('', int(port)), ServerHTTP)
    #设置一直监听请求
    http_server.serve_forever()


if __name__ == "__main__":
    weiboAPI.startDataBaseService()
    #监听8000端口
    start_server(8000)
    
