

$(function() {
	/**
 	*
 	* accordion
 	*
 	*/
	var dom = document.getElementById("direction");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;

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
            data: ['机器学习', '人工智能', '深度学习', '社会网络', '自然语言处理'],
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
            data: [
                ['2000', 10, '机器学习'],
                ['2001', 15, '机器学习'],
                ['2002', 35, '机器学习'],
                ['2003', 35, '机器学习'],
                ['2004', 20, '机器学习'],
                ['2005', 17, '机器学习'],
                ['2006', 17, '机器学习'],
                ['2007', 40, '机器学习'],
                ['2008', 32, '机器学习'],
                ['2009', 26, '机器学习'],
                ['2010', 26, '机器学习'],
                ['2011', 26, '机器学习'],
                ['2012', 32, '机器学习'],
                ['2013', 22, '机器学习'],
                ['2000', 10, '人工智能'],
                ['2001', 15, '人工智能'],
                ['2002', 35, '人工智能'],
                ['2003', 70, '人工智能'],
                ['2004', 20, '人工智能'],
                ['2005', 17, '人工智能'],
                ['2006', 33, '人工智能'],
                ['2012', 32, '人工智能'],
                ['2013', 22, '人工智能'],
                ['2005', 17, '深度学习'],
                ['2006', 33, '深度学习'],
                ['2007', 40, '深度学习'],
                ['2008', 32, '深度学习'],
                ['2009', 26, '深度学习'],
                ['2010', 35, '深度学习'],
                ['2011', 40, '深度学习'],
                ['2012', 32, '深度学习'],
                ['2013', 22, '深度学习'],
                ['2000', 10, '社会网络'],
                ['2001', 15, '社会网络'],
                ['2002', 35, '社会网络'],
                ['2008', 32, '社会网络'],
                ['2009', 26, '社会网络'],
                ['2010', 35, '社会网络'],
                ['2011', 40, '社会网络'],
                ['2012', 32, '社会网络'],
                ['2013', 22, '社会网络'],
                ['2000', 10, '自然语言处理'],
                ['2001', 15, '自然语言处理'],
                ['2002', 35, '自然语言处理'],
                ['2003', 70, '自然语言处理'],
                ['2009', 26, '自然语言处理'],
                ['2010', 35, '自然语言处理'],
                ['2011', 40, '自然语言处理'],
                ['2012', 32, '自然语言处理'],
                ['2013', 22, '自然语言处理']
            ]
        }]
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }

});
