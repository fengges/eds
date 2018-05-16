$(function() {
var vm = new Vue({
  el : '#app',
  extends: CommonTools,

  data : function() {
    return {
       keyword:'',
       name:'',
	   institution:'',
	   search_type:'高级',
	   adv:true,
	   list:['数据挖掘','机器学习','社交网络','深度学习','医疗健康','人工智能','数据库','云计算'],
	  }
  },
  methods: {
     open:function(t){
       if (t=='KEKE TEAM'){
            content = ['/static/aboutus.html', 'yes']
       }else if(t=='Need'){
            content = ['/static/publicNeed.html', 'yes']
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
    search_word:function(event){
        t=event.target.innerText;
        this.keyword=t;
        this.go_search();
    },
    go_search:function(){

        this.page=1;
        this.field='';
        this.h_index='';
        url='/static/searchreasult.html?keyword='+encodeURI(encodeURI(this.keyword))+'&name='+encodeURI(encodeURI(this.name))+'&institution='+encodeURI(encodeURI(this.institution));
//        window.location.href=url
        $(window).attr('location',url);
    },
    change_search:function(){
        if(this.search_type=='高级'){
            this.search_type='简单';
            this.adv=false;
        }else{
            this.search_type='高级';
            this.adv=true;
        }
    },
  },
  created:function() {
  },
});
});