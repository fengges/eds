/**
 *  author   ：feng
 *  time     ：2018/5/30
 *  function : 搜索
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
var index;
$(function() {
index= new Vue({
  el : '#index_search',
  // 修改文本插值的定界符。
  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],
    /*
  * 声明需要的变量
  */
  data : function() {
    return {
        num:0,
        keyWord:'',
          results:[{
                   name:'',
                   school:'',
                   institution:'',
                   h_index:'',
                   paper_num:'',
                   id:'',
                   citation:'',
                   title:'',
                   field:[],
               }],

    }
   },
    methods: {
    openMessage:function(isLogin){
        self=this;
        title="留言";
        content = ['/static/message.html', 'yes']
        if (isLogin){
            this.open(content,title);

        }else{
            layer.confirm('您未登录是否登录', {
              btn: ['登录留言','匿名留言']
            }, function(){
               window.location="/login/gologin";
            }, function(){
                self.open(content,title);
            });
        }

    },
    open:function(content,t){
       layer.open({
          type: 2,
          title:t,
          area: ['500px', '300px'], //宽高
          content: content
       });
    },
    closeSearchDiv:function (){
    $("#mySearch").css("visibility","hidden");
    $("#mySearchResult").css("visibility","hidden");
},
    openSearchDiv:function(){

    $("#mySearch").css("visibility","");
},
     search_word:function(){
       window.location="/search/searchall3?keyword="+encodeURI(encodeURI(this.keyWord));
     },
      search:function(){
        url='/search/search3';
        self=this;
        params={'keyword':this.keyWord,'filer':{}};

        var data= {
            data: JSON.stringify(params),
        };
        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:data,
            dataType: 'json',
            success:function(data){
                re=data.obj;
                self.results=re['result'].splice(0,5);
                self.num=re['num']
                layer.closeAll('loading');
                $("#mySearchResult").css("visibility","");
            },
            error:function (res) {
                layer.closeAll('loading');
            }
        });
    },
    },
     created:function() {
     this.results=[];
     },
  });

});