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
  el : '#global_header',
  extends: CommonTools,
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
                   link:'',
                   citation:'',
                   title:'',
                   field:[],
               }],

    }
   },
    methods: {
      search:function(){
        url='/search/index';
        self=this;
        params={'keyword':this.keyWord};

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
                self.results=re['result'];
                self.num=re['num']
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
     },
  });
      $("#search").click(function(){
      $(".animation-fade-in").toggleClass('display-none');
    });

    $("#cancel").click(function(){
      $(".animation-fade-in").toggleClass('display-none');
    });
});