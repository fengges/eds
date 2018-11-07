
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
var repassword;
$(function() {
repassword= new Vue({
  el : '#repassword',
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
        password:"",
        password2:"",
    }
   },
    methods: {

    validate:function(type){
           if (this.account==""){
            layer.alert("账号不能为空");
            return false;
           }
           if (this.password==""){
            layer.alert("密码不能为空");
            return false;
           }

            if(this.password!=this.password2){
               layer.alert("密码不一致");
               return false;
           }
           return true;
     },

    rePassword:function(evt){
        evt.preventDefault();
        if (!this.validate(0)){
            return ;
        }
        url='/usercenter/repassword';

        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:$("#repasswordForm").serialize(),
            dataType: 'json',
            success:function(data){
                re=data.success;
                if (re){
                layer.alert("更改成功");
                setTimeout(function(){window.location="/index/index"},1000);
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