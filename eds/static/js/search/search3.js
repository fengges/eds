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
var vm;
$(function() {


vm = new Vue({
  el : '#app',
  extends: CommonTools,
    // 修改文本插值的定界符。
  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],
    /*
  * 声明需要的变量
  */
  data : function() {
    return {
       isActive:1,
       types:["专家","平台","学校"],
       type:"专家",
       hotWord:[],
       keyWord:"",
    }
   },
   watch:{
    isActive:function (newQuestion, oldQuestion) {
        this.type=this.types[newQuestion-1];
        this.getHot(this.type);
    }
   },
   methods: {
        search_word:function(event){
            event.preventDefault();
            window.location="/search/searchall?keyword="+encodeURI(encodeURI(this.keyWord));
       },
       getHot:function(type){
            this.hotWord=[];
            url='/search/hotsearch';
            self=this;
            var data= {type:type,page:1,pPageNum:5};
            data= {
                data: JSON.stringify(data),
            };
            layer.load(2);
            $.ajax({
                url:url,
                type:'POST',
                data:data,
                dataType: 'json',
                success:function(data){
                    re=data.obj;
                    self.hotWord=re;
                    layer.closeAll('loading');
                },
                error:function (res) {
                    layer.closeAll('loading');
                }
            });
       }
   },
   created:function() {
   this.getHot(this.type);
   }
});

});