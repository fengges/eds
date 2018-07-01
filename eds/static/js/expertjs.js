

$(function() {
	/**
 	*
 	* accordion
 	*
 	*/


    /**
 	*
 	* 河流图
 	var myDirection = echarts.init(document.getElementById('direction'));
 	$.post('/getdrawdata', {"id":getId()}, function(data){
        data=data.obj;

        theme=data['theme']
        option = {
        title: {
            show: true,
            text: '研究领域趋势',
//            subtext: '领域河流图描述了该学者各领域研究成果随时间变化的趋势',
            left: 'right',
            textStyle: {
                fontSize: 22,
            },
            subtextStyle: {
                fontSize: 16,
            },
            padding:[5, 10]
        },

        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'line',
                lineStyle: {
                    color: 'rgba(0,0,0,0.2)',
                    width: 1,
                    type: 'solid'
                }
            }
        },
        legend: {
            data: data['theme']['themelist'],
            orient: 'vertical',
            left: 'right',
            top: 'middle',
            right: 100,

            // backgroundColor:'#000',
            padding: [
                5, // 上
                10, // 右
                5, // 下
                10, // 左
            ],
            itemGap: 30,
            itemWidth: 35,
            itemHeight: 20,

            formatter: function(name) {
                return echarts.format.truncateText(name, 150, '18px Microsoft Yahei', '…');
            },
            tooltip: {
                show: true
            },

            textStyle:{
              fontSize:16,
            },
        },
        singleAxis: {

            top: '10%',
            left: '3%',
            right: '33%',
            min: 'dataMin',
            max: 'dataMax',

            axisTick: {},

            axisLabel: {},

            type: 'value',

            // position: 'top',

            splitLine: {
                show: true,
                lineStyle: {
                    type: 'dashed',
                    opacity: 0.2
                }
            }
        },
        series: [{
            type: 'themeRiver',
            label: {
                normal: {
                    show: false,
                    // position: 'inner'
                }
            },
            itemStyle: {
                emphasis: {
                    shadowBlur: 20,
                    shadowColor: 'rgba(0, 0, 0, 0.8)'
                },

            },
            data: data['theme']['theme_year']
        }]
    };
        if (option && typeof option === "object") {
            myDirection.setOption(option, true);
            }
    }, "json");
 	*
 	*/


    var myDirection = echarts.init(document.getElementById('direction'));
        $.post('/getdrawdata', {"id":getId()}, function(data){
            data=data.obj;

            theme=data['theme']
            option = {
                tooltip: {
                    position: 'top'
                },
                title: [],
                singleAxis: [],
                series: []
            };

            echarts.util.each(data['theme']['themes'], function (day, idx) {
                option.title.push({
                    textBaseline: 'middle',
                    top: (idx + 0.5) * 100 / 7 + '%',
                    text: day
                });
                option.singleAxis.push({
                    left: 150,
                    type: 'category',
                    boundaryGap: false,
                    data: data['theme']['years'],
                    top: (idx * 100 / 7 + 5) + '%',
                    height: (100 / 7 - 10) + '%',
                    axisLabel: {
                        interval: 2
                    }
                });
                option.series.push({
                    singleAxisIndex: idx,
                    coordinateSystem: 'singleAxis',
                    type: 'scatter',
                    data: [],
                    symbolSize: function (dataItem) {
                        return dataItem[1] * 4;
                    }
                });
            });

            echarts.util.each(data['theme']['data'], function (dataItem) {
                option.series[dataItem[0]].data.push([dataItem[1], dataItem[2]]);
            });
            if (option && typeof option === "object") {
                myDirection.setOption(option, true);
                }
        }, "json");
    function getId(){
            var reg = /expert\/([0-9]*)/
            return reg.exec(document.URL)[1];
        };




});
