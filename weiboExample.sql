#DatabaseName = LZHSCUWeiboDataBase

################################################ 创建用户表 ################################################
#user_id 			用户 id
#user_password 		用户密码 MD5值
#user_name 			用户名
#user_enroll_time 	用户注册时间
#user_sexual		用户性别.0代表女,1代表男
#user_introduction	用户简介
#user_email			用户邮箱
CREATE TABLE UserTable(
	user_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, 
	user_password VARCHAR(128) NOT NULL, 
	user_name VARCHAR(50) NOT NULL, 
	user_enroll_time VARCHAR(128) NOT NULL, 
	user_sexual BOOLEAN, 
	user_introduction VARCHAR(128), 
	user_email VARCHAR(128) NOT NULL
)ENGINE=InnoDB  DEFAULT CHARSET=utf8; 


################################################ 创建微博池 ################################################
#weibo_id 				微博 id
#user_id 				用户 id
#weibo_detail 			微博详情
#weibo_published_time 	微博发表时间
#weibo_comment_number 	微博评论数目
#weibo_agree_number 	微博点赞数目
CREATE TABLE WeiboTable(
	weibo_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	user_id INTEGER NOT NULL,
	weibo_detail VARCHAR(850) NOT NULL,
	weibo_published_time VARCHAR(128) NOT NULL,
	weibo_comment_number INTEGER NOT NULL,
	weibo_agree_number INTEGER NOT NULL,
	FOREIGN KEY(user_id) REFERENCES UserTable(user_id)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8;


################################################ 创建评论池 ################################################
#comment_id 				评论 id
#weibo_id 					微博 id
#user_id 					用户 id
#comment_detail	     		评论详情
#comment_published_time 	评论发表时间
CREATE TABLE CommentTable(
	comment_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	weibo_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	comment_detail VARCHAR(850) NOT NULL,
	comment_published_time VARCHAR(128) NOT NULL,
	FOREIGN KEY(weibo_id) REFERENCES WeiboTable(weibo_id),
	FOREIGN KEY(user_id) REFERENCES UserTable(user_id)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8;


################################################ 创建点赞池 ################################################
#weibo_id 	微博 id
#user_id 	用户 id
CREATE TABLE AgreeTable(
	weibo_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	FOREIGN KEY(weibo_id) REFERENCES WeiboTable(weibo_id),
	FOREIGN KEY(user_id) REFERENCES UserTable(user_id),
	PRIMARY KEY(weibo_id, user_id)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8;










################################################ 添加用户 ################################################
#user_id 			用户 id
#user_password 		用户密码 MD5值
#user_name 			用户名
#user_enroll_time 	用户注册时间
#user_sexual		用户性别.0代表女,1代表男
#user_introduction	用户简介
#user_email			用户邮箱
INSERT INTO UserTable VALUES(NULL, "password", "微博管理员", "2018-5-27 15:00:00", 1, "暂无介绍", "example@scuweibo.com");
INSERT INTO UserTable VALUES(NULL, "password", "用户1", "2018-5-27 15:01:00", 1, "用户1介绍", "example1@scuweibo.com");
INSERT INTO UserTable VALUES(NULL, "password", "用户2", "2018-5-27 15:02:00", 0, "用户2介绍", "example2@scuweibo.com");
INSERT INTO UserTable VALUES(NULL, "password", "用户3", "2018-5-27 15:03:00", 1, "用户3介绍", "example3@scuweibo.com");
INSERT INTO UserTable VALUES(NULL, "password", "用户4", "2018-5-27 15:04:00", 0, "用户4介绍", "example4@scuweibo.com");




################################################ 添加微博 ################################################
#weibo_id 				微博 id
#user_id 				用户 id
#weibo_detail 			微博详情
#weibo_published_time 	微博发表时间
#weibo_comment_number 	微博评论数目
#weibo_agree_number 	微博点赞数目
INSERT INTO WeiboTable VALUES(NULL, 1, "这条微博是管理员发的", "2018-5-27 15:05:28", 3, 1);
INSERT INTO WeiboTable VALUES(NULL, 2, "俺是用户1,今天天气不错啊!", "2018-5-27 15:05:13", 0, 0);
INSERT INTO WeiboTable VALUES(NULL, 3, "俺是用户2,今天天气不错啊!", "2018-5-27 15:06:34", 0, 0);
INSERT INTO WeiboTable VALUES(NULL, 4, "俺是用户3,今天天气不错啊!", "2018-5-27 15:08:26", 0, 0);
INSERT INTO WeiboTable VALUES(NULL, 5, "俺是用户4,今天天气不错啊!", "2018-5-27 15:12:08", 1, 0);

INSERT INTO WeiboTable VALUES(NULL, 2, "俺是用户1,这微博真有意思,再发一条好了", "2018-5-27 15:15:38", 0, 0);




################################################ 添加评论 ################################################
#comment_id 				评论 id
#weibo_id 					微博 id
#user_id 					用户 id
#comment_detail	     		评论详情
#comment_published_time 	评论发表时间
INSERT INTO CommentTable VALUES(NULL, 1, 1, "给自己评论一下,蹭蹭热度[傻笑]", "2018-5-27 15:05:52");
INSERT INTO CommentTable VALUES(NULL, 1, 2, "管理员大哥,以后多关照啊,俺是用户1,你最老的用户!", "2018-5-27 15:06:22");
INSERT INTO CommentTable VALUES(NULL, 1, 3, "大哥,以后也罩罩小弟用户2,感激不尽!", "2018-5-27 15:06:48");

INSERT INTO CommentTable VALUES(NULL, 5, 5, "只有我用户4是萌新,害怕,哭~", "2018-5-27 15:05:52");



################################################ 添加点赞 ################################################
#agree_id 	点赞 id
#weibo_id 	微博 id
#user_id 	用户 id
INSERT INTO AgreeTable VALUES(1, 5);


























