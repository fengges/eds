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
var admin;
$(function() {
admin= new Vue({
  el : '#admin',
  // 修改文本插值的定界符。
  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],
    /*
  * 声明需要的变量
  */
  data : function() {

        return {
             menu:[],
             url:""
        }
   },
    methods: {
        menuClick:function(index,num){
        this.url=this.menu[index]['subMenu'][num]["url"];
    },

    },
     created:function() {
         this.menu=[];
         this.menu.push({class:"el-icon-message","name":"用户",subMenu:[{name:"用户管理",url:"/admin/user"},{name:"留言查看",url:"/admin/message"}]});
         this.menu.push({class:"el-icon-menu","name":"数据",subMenu:[{name:"数据统计",url:"/statistics/statistics"},{name:"百度",url:"https://www.baidu.com/"}]})
         this.menu.push({class:"el-icon-setting","name":"首页",subMenu:[{name:"领域管理",url:"/admin/field"},{name:"vue",url:"https://cn.vuejs.org/"}]})
         this.menuClick(0,0)
     },
  });

});