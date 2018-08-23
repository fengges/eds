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
       visible: false,
       keyword:'',
       name:'',
	   institution:'',
	   num:0,
	   school:[],
	   schools:[{
	       name:'',
	       value:'',
	       num:0,
	   }],
	   subject:[],
	   subjects:[{
	       name:'',
	       value:'',
	       num:0,
	   }],
	   results:[{
	       name:'',
           school:'',
           institution:'',
           link:'',
           citation:'',
           abstract:'',
           title:'',
           fields:[],
	   }],
	   show:false,
	   adv:true,
	   hot_word:['数据挖掘','机器学习','社交网络','深度学习','医疗健康','人工智能','数据库','云计算'],
    }
   },
   watch: {
          subject:function (newQuestion, oldQuestion) {
               if (this.subject.indexOf('all')>=0&& this.subject.length<this.subjects.length){
                 this.subject=['all']
                 self=this
                 this.subjects.forEach(function(value,index,array){
                    self.subject.push(value["value"])
                });
               }
          },
          school:function (newQuestion, oldQuestion) {
               if (this.school.indexOf('all')>=0&& this.school.length<this.schools.length){
                 this.school=['all']
                 self=this
                 this.schools.forEach(function(value,index,array){
                    self.school.push(value["value"])
                });
               }
          }
     },
    methods: {
       search_word:function(){
        window.location="/search/searchall3?keyword="+encodeURI(encodeURI(this.keyWord));
     },
    /*
    *点击超链接搜索
    */
    click_word:function(event){
        t=event.target.innerText;
        this.keyword=t;
        this.school=[];
        this.subject=[];
        this.name='';
        this.reload();
     },

      reload:function() {
        url='/search/search3';
        self=this;
        var data= {
            data: JSON.stringify({"filer":{"school":this.school,"code":this.subject,"name":this.name},'keyword':this.keyword}),
        };
        layer.load(2);
        $.ajax({
            url:url,
            type:'POST',
            data:data,
            dataType: 'json',
            success:function(data){
                re=data.obj;
                self.results=re['result'];
                self.schools=re['filter']['schools'];
                self.subjects=re['filter']['codes'];
                self.num=re["num"]
                layer.closeAll('loading');
            },
            error:function (res) {
                layer.closeAll('loading');
            }
        });
    },
    },

     created:function() {
        this.results=[];
        self=this;
        params=['keyword']
        var data= {};
        params.forEach(function(value,index,array){
            temp=self.getQueryParam(value);
            if (temp!=null){
                temp=decodeURI(temp)
                self[value]=temp;
            }
        });
        this.reload();
     },
  });
      $("#search").click(function(){
      $(".animation-fade-in").toggleClass('display-none');
    });

    $("#cancel").click(function(){
      $(".animation-fade-in").toggleClass('display-none');
    });
});