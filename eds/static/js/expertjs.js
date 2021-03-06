

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


//    var myDirection = echarts.init(document.getElementById('direction'));
    var myWordCloud = echarts.init(document.getElementById('wordcloud'));
    var myPaperBar = echarts.init(document.getElementById('paperbar'));
    $.post('/getdrawdata', {"id":getId()}, function(data){
        data=data.obj;

//        //主题单轴图
//        theme=data['theme']
//        directionOption = {
//            tooltip: {
//                position: 'top'
//            },
//            title: [],
//            singleAxis: [],
//            series: []
//        };
//
//        echarts.util.each(data['theme']['themes'], function (day, idx) {
//            directionOption.title.push({
//                textBaseline: 'middle',
//                top: (idx + 0.5) * 100 / 7 + '%',
//                text: day
//            });
//            directionOption.singleAxis.push({
//                left: 150,
//                type: 'category',
//                boundaryGap: false,
//                data: data['theme']['years'],
//                top: (idx * 100 / 7 + 5) + '%',
//                height: (100 / 7 - 10) + '%',
//                axisLabel: {
//                    interval: 2
//                }
//            });
//            directionOption.series.push({
//                singleAxisIndex: idx,
//                coordinateSystem: 'singleAxis',
//                type: 'scatter',
//                data: [],
//                symbolSize: function (dataItem) {
//                    return dataItem[1] * 4;
//                }
//            });
//        });
//
//        echarts.util.each(data['theme']['data'], function (dataItem) {
//            directionOption.series[dataItem[0]].data.push([dataItem[1], dataItem[2]]);
//        });
//            if (directionOption && typeof directionOption === "object") {
//                myDirection.setOption(directionOption, true);
//                }

        //词云图
        topics = data['wordcloud']

        cloudOption = {
            title: {
                text: '专家标签云',
//                link: 'https://www.baidu.com/s?wd=' + encodeURIComponent('ECharts'),
                x: 'left',
                padding:[20, 20],
                textStyle: {
                    fontSize: 23,
                    color: '#656969'
                }

            },
            backgroundColor: '#F0F0F0',
            tooltip: {
                show: true
            },

            series: [{
                name: '标签权重',
                type: 'wordCloud',
                // size: ['9%', '99%'],
                // sizeRange: [6, 66],//最小文字——最大文字
                // textRotation: [0, 45, 90, -45],
                 rotationRange: [0, 0],//旋转角度区间
                // rotationStep: 90,//旋转角度间隔
                // shape: 'circle',
                 gridSize: 25,//字符间距
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 6
                },
                textStyle: {
                    normal: {
//                        color: function() {
//                            return 'rgb(' + [
//                                Math.round(Math.random() * 105)+150,
//                                Math.round(Math.random() * 105)+150,
//                                Math.round(Math.random() * 105)+150
//                            ].join(',') + ')';
//                        }
                            color: '#656969'
                    },
                    emphasis: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                data: []
            }]
        };

        var cloudJosnList = topics;

        cloudOption.series[0].data = cloudJosnList;

        if (cloudOption && typeof cloudOption === "object") {
            myWordCloud.setOption(cloudOption, true);
            }


        //历年成果图
        xy = data['paperbar']
        paperbarOption = {
            backgroundColor: '#fff',
            xAxis: {
                data: xy['x'],
                axisLine: {
                    lineStyle: {
                        color: '#000'
                    }
                },
                axisLabel: {
                    color: '#000',
                    fontSize: 14
                }
            },
            yAxis: {
                name: "（篇）",
                nameTextStyle: {
                    color: '#000',
                    fontSize: 16
                },
                axisLine: {
                    lineStyle: {
                        color: '#000'
                    }
                },
                axisLabel: {
                    color: '#000',
                    fontSize: 16
                },
                splitLine: {
                    show:false,
                    lineStyle: {
                        color: '#000'
                    }
                },
                interval:500,
                max: xy['maxy']

            },
            series: [{
                type: 'bar',
                barWidth: 18,
                itemStyle:{
                    normal:{
                        color:new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: '#00b0ff'
                        }, {
                            offset: 0.8,
                            color: '#7052f4'
                        }], false)
                    }
                },
                data: xy['y']
            }]
        };

        if (paperbarOption && typeof paperbarOption === "object") {
            myPaperBar.setOption(paperbarOption, true);
            }
    }, "json");



    function getId(){
            var reg = /expert\/([0-9]*)/
            return reg.exec(document.URL)[1];
        };




});
