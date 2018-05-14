
/**
 *  author   ：feng
 *  time     ：2018/3/14
 *  function : 搜索控制
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
           field:[],
           light_abstract:'',
	   }],
	   pageList:[],
	   page:1,
	   pPageNum:10,
	   allPage:1,
	   num:0,
	   search_type:'高级',
	   adv:true,
	   accurate_search:false,
	   hot_word:['数据挖掘','机器学习','社交网络','深度学习','医疗健康','人工智能','数据库','云计算'],
    }
  },

  methods: {
    /*
    *  弹出项目简介和团队介绍
    */

    open:function(t){
       if (t=='KEKE TEAM'){
            content = ['/static/aboutus.html', 'yes']
       }
       else{
            content = ['/static/aboutproject.html', 'yes']
       }
      layer.open({
          type: 2,
          title:t,
          area: ['40%', '80%'], //宽高
          content: content
       });
    },
    /*
    * 弹出完整论文摘要
    */
    show_paper:function(item){
        div="<div class='paper'><h6>"+item.title+"</h6>"
        div+='<div class="innerCtn"><span class="mui-ellipsis">'+item.abstract+'</span></div></div>'
        layer.open({
          type: 1,
          title:item.name,
          skin: 'layui-layer-rim',
          area: ['40%', '80%'], //宽高
          content: div
        });
    },
    /*
    * 输入框回车使搜索
    */
    enter_search:function(){
        this.page=1;
        this.field='';
        this.h_index='';
        this.reload();
    },
    /*
    * 该变每页显示条数
    */
    change_page:function(event,num){
        t=event.target
        $(t).css({color:'#00d3d4'});
        $(t).siblings().css({color:'#777'});
        this.pPageNum=num;
        this.page=1;
        this.reload();
    },
    /*
    *点击超链接搜索
    */
    search_word:function(event){
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
    /*
    *切换搜索模式
    */
    change_search:function(){
        if(this.search_type=='高级'){
            this.search_type='简单';
            this.adv=false;
        }else{
            this.search_type='高级';
            this.adv=true;
        }
    },
    /*
    * 排序方式
    */
    change_order:function(s){
      this.order=s;
      this.reload();
    },
    /*
    *  上一页
    */
    pre:function(){
        num=this.page;
        num--;
        this.go(num);
    },
    /*
    *下一页
    */
    next:function(num){
        num=this.page;
        num++;
        this.go(num);
    },
    /*
    * 页面跳转
    */
    go:function(num){
        if (num<=0){
            alert('已经是第一页');
        }else if(num>this.allPage){
            alert('已经是最后一页');
        }else{
            this.page=num;
            this.reload();
        }
    },
    /*
    * 筛选领域
    */
    click_fields:function(event){
        t=event.target.innerText;
        if (t!="全部"){
            index=t.indexOf('(');
            this.field=t.substring(0,index);
        }else{
            this.field=''
        }
        this.page=1;
        this.reload();
    },
    /*
    * 筛选 h_index值
    */
    click_index:function(event){
        t=event.target.innerText;
        if (t!="全部"){
            index=t.indexOf('(');
            this.h_index=t.substring(0,index);
        }else{
            this.h_index=''
        }
        this.page=1;
        this.reload();
    },
    /*
    *  请求数据
    */
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
                self.allPage=re['allPage'];
                self.pageList=[];
                s=self.page-3;
                e=self.page+3;
                if (s<=0){
                    s=1
                    e=self.allPage>7?7:self.allPage;
                }else if(e>self.allPage){
                    e=self.allPage
                    s=(e-6>=1)?(e-6):1
                }
                for (i=s;i<=e;i++){
                    self.pageList.push(i);
                }
                layer.closeAll('loading');
            },
            error:function (res) {
                layer.closeAll('loading');
            }
        });
    },
  },
  /*
  *  初始化页面
  */
  created:function() {
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
});