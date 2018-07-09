/**
 *  author   ：feng
 *  time     ：2018/6/14
 *  function : 搜索
 */

/*
    vue框架
*/
var vm;
$(function() {


vm = new Vue({
  el : '#user',

  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],

  data : function() {
    return {
       userData: [],
       page:1,
	   pPageNum:5,
	   num:0,
    }
   },

     methods: {
         reload(){
                url='/admin/getUser';
                self=this;
                var data= {page:this.page,pPageNum:this.pPageNum};
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
                        self.userData=re["result"]
                        self.num=re["num"]
                        layer.closeAll('loading');
                    },
                    error:function (res) {
                        layer.closeAll('loading');
                    }
                });
         },
         handleSizeChange(val) {
            this.pPageNum=val;
            this.reload();
          },
          handleCurrentChange(val) {
            this.page=val;
            this.reload();
          },
        formatDate :function (date, fmt) {
              if (/(y+)/.test(fmt)) {
                 fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
               }
               let o = {
                'M+': date.getMonth() + 1,
               'd+': date.getDate(),
                 'h+': date.getHours(),
               'm+': date.getMinutes(),
                 's+': date.getSeconds()
              }
           for (let k in o) {
                 if (new RegExp(`(${k})`).test(fmt)) {
                 let str = o[k] + ''
                   fmt = fmt.replace(RegExp.$1, RegExp.$1.length === 1 ? str : this.padLeftZero(str))
               }
          }
     return fmt
    },

    },

     created:function() {
          this.reload();
     },
  });
});