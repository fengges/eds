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
  el : '#mychart',

  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],

  data : function() {
    return {
        type:"",
        types:[],
        startDate:'',
        endDate:'',
        timeType:'',
    }
   },
     watch: {
      timeType: function (newQuestion, oldQuestion) {
            if (newQuestion=="最近一周"){
               this.startDate=this.add_date(-8);
               this.endDate=this.add_date(-1);
            }else if (newQuestion=="最近一月"){
               this.startDate=this.add_date(-31);
               this.endDate=this.add_date(-1);
            }
      }
     },
     methods: {
        padLeftZero:function (str) {
           return ('00' + str).substr(str.length)
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
        add_date:function (aa){
            var date1 = new Date();
            var date2 = new Date(date1);
            date2.setDate(date1.getDate()+aa);
            return date2;
        },
        search:function(){
        if (this.type==""){
            layer.alert('请选择类型');
            return;
        }
        if (this.startDate==""){
            layer.alert('请选择开始时间');
             return;
        }
        if (this.endDate==""){
            layer.alert('请选择结束时间');
             return;
        }
        if (this.endDate<this.startDate){
            layer.alert('结束时间应大于开始时间');
             return;
        }
        data={type:this.type,startDate:this.formatDate(this.startDate,"yyyy-MM-dd"),endDate:this.formatDate(this.endDate,"yyyy-MM-dd")};
        data= {
            data: JSON.stringify(data),
        };
        url="/statistics/search"
        layer.load(2);
        self=this;
        $.ajax({
            url:url,
            type:'POST',
            data:data,
            dataType: 'json',
            success:function(data){
                re=data.obj;
                title=self.formatDate(self.startDate,"yyyy-MM-dd")+" 到 "+self.formatDate(self.endDate,"yyyy-MM-dd")+" "+self.type+"热点图";
                option=self.ininZhu(title,re);
                chart = echarts.init(document.getElementById('chart'));
                chart.setOption(option);
                layer.closeAll('loading');
            },
            error:function (res) {
                layer.closeAll('loading');
            }
        });
    },
        ininZhu:function(title,data){
        option = {
            title: {
                x: 'center',
                text:title,
            },
            tooltip: {
                trigger: 'item'
            },
            toolbox: {
                show: true,
                feature: {
                    dataView: {show: true, readOnly: false},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: true,
            grid: {
                borderWidth: 0,
                y: 80,
                y2: 60
            },
            xAxis: [
                {
                    type: 'category',
                    show: false,
                    data: data["xAxis"]
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    show: false
                }
            ],
            series: [
                {
                    name: title,
                    type: 'bar',
                    itemStyle: {
                        normal: {
                            color: function(params) {
                                // build a color map as your need.
                                var colorList = [
                                  '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                                   '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                                   '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                                ];
                                return colorList[params.dataIndex]
                            },
                            label: {
                                show: true,
                                position: 'top',
                                formatter: '{b}\n{c}'
                            }
                        }
                    },
                    data: data["data"],
                    markPoint: {
                        tooltip: {
                            trigger: 'item',
                            backgroundColor: 'rgba(0,0,0,0)',
                        },
                        data:data["markPoint"]
                    }
                }
            ]
        };
        return option;
        },
    },

     created:function() {
        this.types=["搜索前5","搜索全部","专家","学校","登陆","注册"];

     },
  });
});