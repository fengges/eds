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
    }
   },
    methods: {
     register:function(evt){
        url='/login/register';
        evt.preventDefault();
        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:$("#registerForm").serialize(),
            dataType: 'json',
            success:function(data){
                re=data.success;
                if (re){
                alert("注册成功");

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
        url='/login/login';
        evt.preventDefault();
        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:$("#loginForm").serialize(),
            dataType: 'json',
            success:function(data){
                re=data.success;
                if (re){
                alert("注册成功");
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