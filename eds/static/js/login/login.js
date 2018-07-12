/**
 *  author   ：feng
 *  time     ：2018/5/30
 *  function : 登陆
 */

 /**
 阻止回车的时候表单提交
 */
function ClearSubmit(e) {
    if (e.keyCode == 13) {
        return false;
    }
}
/*
    vue框架
*/
var login;
$(function() {
login= new Vue({
  el : '#login',
  // 修改文本插值的定界符。
  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],
    /*
  * 声明需要的变量
  */
  data : function() {
    return {
        isLogin:true,
        account:"",
        username:"",
        password:"",
        password2:"",
        countLable:"验证码",
        time:0,

        isDisabled:false,
    }
   },
    methods: {
    changeCode:function(){
        $("#smsCaptchaImage").attr("src","/code/getCode?time="+Date.parse(new Date()))
    },
    countDown:function(num){
        let me = this;
        me.time=parseInt(num);
        me.isDisabled = true;
        let interval = window.setInterval(function() {
            me.countLable = me.time + 's';
            --me.time;
            if(me.time < 0) {
                me.countLable = "重新发送";
                me.time = 10;
                me.isDisabled = false;
                window.clearInterval(interval);
            }
        }, 1000);
    },
    sendSms:function(phone){
        if (this.isDisabled==true){
            layer.msg(this.countLable);
            return ;
        }
        url='/code/sendSms';
        self=this;
        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:{phone:phone},
            dataType: 'json',
            success:function(data){
                re=data.success;
                if (re){
                    layer.msg("发送成功");
                    self.countDown(60);
                }else{
                    layer.alert(data.msg);
                    if (data.msg=="发送太频繁"){
                        self.countDown(data["obj"]["second"]);
                    }
                    self.changeCode();
                }
                layer.closeAll('loading');
             },
            error:function (res) {
                layer.closeAll('loading');
            }
           });
    },
    checkSms:function(){
        var code=$("#partnerYzm").val();
        if(code==""){
            this.showError("请输入验证码");
            $("#partnerYzm").focus();
            return
         }
        var phone=$("#partnerPhone").val();
        if(phone==""){
            this.showError("请输入手机号");
            $("#partnerPhone").focus();
            return
         }else if (this.isPoneAvailable(phone)==false){
            this.showError("请输入正确手机号");
            $("#partnerPhone").focus();
            return
         }
        url='/code/validate_code';
        self=this
        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:{code:code},
            dataType: 'json',
            success:function(data){
                re=data.success;
                if (re){
                    self.sendSms(phone);
                }else{
                    layer.alert(data.msg);
                    self.changeCode();
                }
                layer.closeAll('loading');
             },
            error:function (res) {
                layer.closeAll('loading');
            }
           });

    },
   isPoneAvailable:function(str) {
        var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;
        if (!myreg.test(str)) {
            return false;
        } else {
            return true;
        }
     },
    moible:function(open){
        if(open){
           $("#common").hide();
           $("#mobile").show();
        }else{
           $("#common").show();
           $("#mobile").hide();
        }
    },
    showError:function(error){
	$(".form-error").find("label").html(error);
	$(".form-error").show();
},
    validate:function(type){
       if (this.account==""){
        this.showError("账号不能为空");
        return false;
       }
       if (this.password==""){
        this.showError("密码不能为空");
        return false;
       }
       if(type==1){
            if(this.username==""){
                   this.showError("用户名不能为空");
                   return false;
            }
            if(this.password!=this.password2){
                   this.showError("密码不一致");
                   return false;
            }
       }
       return true;
 },
    register:function(evt){
   evt.preventDefault();
    if (!this.validate(1)){
        return ;
    }
    url='/login/register';

    layer.load(2);
    $.ajax({
        url:url,
        type:'POST',
        data:$("#registerForm").serialize(),
        dataType: 'json',
        success:function(data){
            re=data.success;
            if (re){
            layer.alert("注册成功");

            }else{
            layer.alert(data.msg);
            }
            layer.closeAll('loading');
         },
        error:function (res) {
            layer.closeAll('loading');
        }
       });
     },
   login:function(evt){
     evt.preventDefault();
    if (!this.validate(0)){
        return ;
    }
    url='/login/login';

    layer.load(2);
    $.ajax({
        url:url,
        type:'POST',
        data:$("#loginForm").serialize(),
        dataType: 'json',
        success:function(data){
            re=data.success;
            if (re){
            layer.alert("登陆成功");
            window.location="/index/index"
            }else{
            layer.alert(data.msg);
            }
            layer.closeAll('loading');
         },
        error:function (res) {
            layer.closeAll('loading');
        }
       })
     },
   phonelogin:function(evt){
     evt.preventDefault();
    if($("#partnerPhone").val()==""){
       this.showError("输入手机号");
       return;
     }
     if($("#partnerJym").val()==""){
       this.showError("输入验证码");
       return;
     }
    url='/login/phonelogin';
    layer.load(2);
    $.ajax({
        url:url,
        type:'POST',
        data:$("#mobileLoginForm").serialize(),
        dataType: 'json',
        success:function(data){
            re=data.success;
            if (re){
            layer.alert("登陆成功");
            window.location="/index/index"
            }else{
            layer.alert(data.msg);
            }
            layer.closeAll('loading');
         },
        error:function (res) {
            layer.closeAll('loading');
        }
       })
     },
    },
     created:function() {
           this.moible(true)
     },
  });

});