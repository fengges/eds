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
	   hindexs:[{
	       value:'',
	       num:0,
	   }],
	   h_index:'',
	   fields:[{
	       value:'',
	       num:0,
	   }],
	   field:'',
	   order:'all',
	   results:[{
	       name:'',
           school:'',
           institution:'',
           h_index:'',
           paper_num:'',
           link:'',
           citation:'',
           abstract:'',
           title:'',
           fields:[],
           light_abstract:'',
	   }],
	   show:false,
	   page:1,
	   pPageNum:5,
	   num:0,
	   search_type:'高级',
	   adv:true,
	   accurate_search:false,
	   hot_word:['数据挖掘','机器学习','社交网络','深度学习','医疗健康','人工智能','数据库','云计算'],
    }
   },
    methods: {
       search_word:function(){
        window.location="/search/searchall?keyword="+encodeURI(encodeURI(this.keyWord));
     },
    /*
    *点击超链接搜索
    */
    click_word:function(event){
        t=event.target.innerText;
        this.keyword=t;
        this.institution=''
        this.name=''
        this.go_search();
     },
     /*
     *点击搜索
     */
    go_search:function(){
        this.page=1;
        this.field='';
        this.h_index='';
        this.reload();
    },
        do_search:function(){
        this.page=1;
        this.reload();
    },
      handleSizeChange(val) {
        this.pPageNum=val;
        this.reload();
      },
      handleCurrentChange(val) {
        this.page=val;
        this.reload();
      },
      reload:function() {
        url='/search/search';
        self=this;
        params=['keyword','name','institution','h_index','field','order','page','pPageNum','accurate_search']
        var data= {};
        params.forEach(function(value,index,array){
            data[value]=self[value];
        });
        var data= {
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
                self.results=re['result'];
                if(navigator.userAgent.indexOf("Firefox")>0){
                    self.results.forEach(function(value,index,array){
                        if (value["light_abstract"].length>120){
                            value["light_abstract"]=value["light_abstract"].substring(0,120);
                        }
                    });
                }
                self.hindexs=re['filter']['hindexs'];
                self.fields=re['filter']['fields'];
                self.num=re['num'];
                layer.closeAll('loading');
            },
            error:function (res) {
                layer.closeAll('loading');
            }
        });
    },
      search:function(){
        url='/search/index';
        self=this;
        params={'keyword':this.keyword};

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
        self=this;
    params=['keyword','name','institution','h_index','field','order','page','pPageNum','accurate_search']
    var data= {};
    params.forEach(function(value,index,array){
        temp=self.getQueryParam(value);
        if (temp!=null){
            temp=decodeURI(temp)
            self[value]=temp;
        }
    });
    var num=0;
    if (this.pPageNum==5){
        num=0;
    }else if(this.pPageNum==10){
        num=1;
    }else{
        num=2;
    }
    $($('#page').siblings()[num]).css({color:'#00d3d4'});
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