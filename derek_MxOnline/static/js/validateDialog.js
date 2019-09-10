function verifyDialogSubmit(array){
    var i =0,
        length = array.length,
        validdata = true;
    for(i;i<length;i++){
        var obj = array[i],
            _this = $(obj.id);
        validdata = valid(obj,_this);
        if(!validdata){
            return validdata;
        }
    }

    return validdata;
} // verifyDialogSubmit

function valid(obj, _this){
    var tips = obj.tips,
        errorTips = obj.errorTips,
        regName = obj.regName,
        require = obj.require,
        repwd = obj.repwd,
        minlength = obj.minlength,
        strlength = obj.strlength,
        value = $.trim(_this.val());
    //为空验证
    if(require && !value ){
        return Dml.fun.showValidateError(_this, tips);
    }else {
        if(regName && !Dml.regExp[regName].test(value)){
            return Dml.fun.showValidateError(_this, errorTips);
        }

        // 最小长度
        if(minlength != undefined && value.length <minlength ){
            return Dml.fun.showValidateError(_this, '输入长度需要大于'+ minlength +'位')
        }
         //长度
        if(strlength != undefined && value.length != strlength){
            return Dml.fun.showValidateError(_this,'输入长度必须为'+strlength+'位');
        }


        //重复密码校验
        if(repwd != undefined && value != $(repwd).val()){
            return Dml.fun.showValidateError(_this,Dml.Msg.erRePwd);
        }
    }

    _this.parent().removeClass('errorput');
    _this.parent().siblings('.error').hide();
    return true;
}// valid

$(function(){
    $('input[type=text]').focus(function(){
       this.parent().removeClass('errorput');
       this.parent().siblings('.error').hide();
    });
});