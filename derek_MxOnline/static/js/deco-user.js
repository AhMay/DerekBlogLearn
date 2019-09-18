// 修改个人中心邮箱验证码
function sendCodeChangeEmail($btn){
    var verify = verifyDialogSubmit([
    {id:'#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true }
    ]);
    if(!verify){
        return;
    }
    $.ajax({
        cache: false,
        type: 'get',
        dataType: 'json',
        url: '/users/sendemail_code/',
        data: $('#jsChangeEmail').serialize(),
        async: true,
        beforeSend: function(XMLHttpRequest){
            $btn.val("发送中");
            $btn.attr('disabled', true);
        },
        success: function(data){
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == 'success'){
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱验证码已发送");
            }else if(data.status == 'failure'){
                 Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱验证码发送失败");
            }
        },
        complete: function(XMLHttpRequest){
             $btn.val("获取验证码");
            $btn.removeAttr('disabled');
        }
    });
}// 修改个人中心邮箱验证码

//个人资料邮箱修改
function changeEmailSubmit($btn){
    var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/users/update_email/ ",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
            $("#jsChangeEmailTips").html("验证中...").show(500);
        },
        success:function(data) {
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == "success"){
                $("#jsChangeEmailTips").html("信息更新成功").show(500);
                setTimeout(function(){location.reload();},1000);
            }else{
                 Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱信息更新失败");
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
} //个人资料邮箱修改
$(function(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings){
            if(settings.type=='POST'){
                 xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
            }
        }
    }); // csrf token
    // 个人资料头像
    $('.js-img-up').uploadPreview({Img:".js-img-show", Width:94,Height:94, Callback:function(){
        $('#jsAvatarForm').submit();
    }});

    //修改密码, 点击跳出窗口
    $('#jsUserResetPwd').on('click', function(){
        Dml.fun.showDialog('#jsResetDialog',"#jsResetPwdTips");
    }); //修改密码

    //提交修改密码请求
    $('#jsResetPwdBtn').click(function(){
        $.ajax({
            cache:false,
            type: 'POST',
            dataType: 'json',
            url:"/users/update/pwd/",
            data:$('#jsResetPwdForm').serialize(),
            async:true,
            success: function(data) {
                if(data.password1){
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                }else if(data.password2){
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title:'提交成功',
                        h2:'修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                }else if(data.msg){
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });//提交修改密码请求

    // 修改邮箱，点击跳出窗口
    $('.changeemai_btn').click(function(){
        Dml.fun.showDialog('#jsChangeEmailDialog','#jsChangeEmailTips');
    });//修改邮箱

    //获取验证码
    $('#jsChangeEmailCodeBtn').on('click', function(){
        sendCodeChangeEmail($(this));
    }); // 点击发送邮箱修改验证码
    $('#jsChangeEmailBtn').click(function(){
        changeEmailSubmit($(this));
    });//提交修改邮箱请求

    //用户信息保存
   $('#jsEditUserBtn').on('click', function(){
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
            verify = verifySubmit(
            [
                {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
            ]
        );
        if(!verify){
           return;
        }
         $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/users/info/",
            data:$jsEditUserForm.serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("保存中...");
                _self.attr('disabled',true);
            },
            success: function(data) {
                if(data.nick_name){
                    _showValidateError($('#nick_name'), data.nick_name);
                }else if(data.birthday){
                   _showValidateError($('#birth_day'), data.birthday);
                }else if(data.address){
                   _showValidateError($('#adress'), data.address);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    setTimeout(function(){window.location.href = window.location.href;},1500);
                }else{
                    console.log(data);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });

   }); //用户信息保存
 })