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
    }
   },
    methods: {
    //开启错误提示
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
                alert(data.msg);
                }
                layer.closeAll('loading');
             },
            error:function (res) {
                layer.closeAll('loading');
            }
           })
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
                alert(data.msg);
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

     },
  });

});