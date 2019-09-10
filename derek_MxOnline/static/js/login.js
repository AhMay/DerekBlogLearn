var zyemail="",
    zyUname="",
    hash={
        'qq.com': 'http://mail.qq.com',
        'gmail.com': 'http://mail.google.com',
        'sina.com': 'http://mail.sina.com.cn',
        '163.com': 'http://mail.163.com',
        '126.com': 'http://mail.126.com',
        'yeah.net': 'http://www.yeah.net/',
        'sohu.com': 'http://mail.sohu.com/',
        'tom.com': 'http://mail.tom.com/',
        'sogou.com': 'http://mail.sogou.com/',
        '139.com': 'http://mail.10086.cn/',
        'hotmail.com': 'http://www.hotmail.com',
        'live.com': 'http://login.live.com/',
        'live.cn': 'http://login.live.cn/',
        'live.com.cn': 'http://login.live.com.cn',
        '189.com': 'http://webmail16.189.cn/webmail/',
        'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
        'yahoo.cn': 'http://mail.cn.yahoo.com/',
        'eyou.com': 'http://www.eyou.com/',
        '21cn.com': 'http://mail.21cn.com/',
        '188.com': 'http://www.188.com/',
        'foxmail.coom': 'http://www.foxmail.com'
    },
    zy_c_num=60,
    zy_str="";

// 登录表单提交
function login_form_submit(){
    var $jsLoginBtn = $("#jsLoginBtn"),
        $jsLoginTips = $("#jsLoginTips")
        $account_1 = $("#account_l"),
        args = window.location.search.substr(1,window.location.search.length).split('&'), //从问号(?)开始的URL查询部分
        arg=[],
        verify = verifyDialogSubmit(
            [
                {id: '#account_1', tips: Dml.Msg.epUserName, errorTips: Dml.Msg.erUserName, regName: 'phMail', require: true},
                 {id: '#password_l', tips: Dml.Msg.epPwd, errorTips: Dml.Msg.erPwd, regName: 'pwd', require: true}
            ]
        );

    if(!verify){
        return;
    }
    var autoLogin = false;
    if ($('#jsAutoLogin').is(':checked')){
        autoLogin = true; //自动登录复选框 (目前窗口没有)
    }
    $.each(args, function(key, value){
        arg = value.split('=');
        if(arg[0]=='name'){
            return false; // 找到name 参数？ 目前 name='username'
        }
    }); //each

    $.ajax({
        cache: false,
        type: 'post',
        dataType: 'json',
        url: {% url 'login' %},
        data: $('#jsLoginForm').serialize() + '&autologin=' + autoLogin + '&' + arg[0] + '=' + arg[1], // jsLoginForm 没有?
        async: true,
        beforeSend: function(XMLHttpRequest){
            $jsLoginBtn.val("登录中");
            $jsLoginBtn.attr("disabled","disabled");
        },
        success: function(data){
            if(data.account_1){
                Dml.fun.showValidateError($accountl, data.account_l);
            }else if(data.password_l){
                 Dml.fun.showValidateError($("#password_l"),data.password_l);
            }else{
                if(data.status == 'success'){
                    $('#jsLoginForm')[0].reset();
                    window.location.href = data.url;
                }else if(data.status == 'failure'){
                    // 注册账户处于未激活状态:
                    if(data.msg == 'no_active'){
                        zyemail = $accountl.val();
                        zyUname = zyemail;
                        $("#jsEmailToActive").html(zyemail); //替换邮件内容
                        var url = zyemail.split('@')[1],
                            $jsGoToEmail = $("#jsGoToEmail");
                        $jsGoToEmail.attr('href', hash[url]);
                        if(hash[url]== undefined || hash[url] == null){
                            $jsGoToEmail.parent().hide();
                        }
                        Dml.func.showDialog('#jsUnactiveForm')；
                    }else{
                        $jsLoginTips.html("账号或者密码错误，请重新输入").show();
                    }
                }
            }
        },
        complete: function(XMLHttpRequest){
            $jsLoginBtn.val('登录');
            $jsLoginBtn.remvoeAttr("disabled");
        }
    });// ajax
} //login_form_submit