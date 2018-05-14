
$(function() {
	/**
 	* 
 	* accordion
 	* 
 	*/
	var Accordion = function(el, multiple) {
		this.el = el || {};
		this.multiple = multiple || false;

		// Variables privadas
		var links = this.el.find('.link');
		// Evento
		links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
	}

	Accordion.prototype.dropdown = function(e) {
		var $el = e.data.el;
			$this = $(this),
			$next = $this.next();

		$next.slideToggle();
		$this.parent().toggleClass('open');

		if (!e.data.multiple) {
			$el.find('.submenu').not($next).slideUp().parent().removeClass('open');
		};
	}	

	var accordion = new Accordion($('#accordion'), false);

	/**
	 * 研究兴趣&学者能力图&自我中心网络Start
	 */

	var myDirection = echarts.init(document.getElementById('direction'));
	var myAbility = echarts.init(document.getElementById('ability'));
	var myEgonet = echarts.init(document.getElementById('egonet'));


    /**
	 * Ajax获取数据
	 */
    $.post('/getdrawdata', {"id":getId()}, function(data){
          data=data.obj;
          op_Ability = {

            tooltip : {
                trigger: 'axis',
                formatter:function(params){
                  var v=Math.pow(2,params[0][2])
                  v=Math.round(v)
                  return params[0][3]+"\n"+v;
                },
            },
             polar : [
                {
                    indicator : [
                        {text : 'paper', max  : 10},
                        {text : 'citation', max  : 12},
                        {text : 'h_index', max  : 6},
                        {text : 'G_index', max  : 7},
                        {text : 'social', max  : 9}
                    ],
                    radius : 55
                }
            ],
            calculable : true,
            series : [
                {
                    name: 'ra',
                    type: 'radar',
                    itemStyle: {
                        normal: {
                            areaStyle: {
                                type: 'default'
                            }
                        }
                    },
                    data : [
                        {
                            value :data['radar'],
                        }
                    ]
                }
            ]
        };

    myAbility.setOption(op_Ability);

    var constMaxRadius = 8;
    var constMinRadius = 2;

    var egoNodes = [];
    var egoLinks = [];
    var name=$("#name").text()
    ego=data["ego"];
    var egoNodes=ego["nodes"]
    egoNodes[0]["label"]=name
    var egoLinks=ego["links"]
    myEgonet.setOption({


        legend: {
            x: 'left',
            data:['作者','收录', '未收录']
        },
        series : [
            {
                type:'force',
                name : "ego-net",
                ribbonType: false,
                categories : [
                    {name: '作者'},
                    {name: '收录'},
                    {name: '未收录'}
                ],
                itemStyle: {
                    normal: {
                        label: {
                            show: true,
                             textStyle: {
                                color: '#333'
                            }
                        },
                        nodeStyle : {
                            brushType : 'both',
                            borderColor : 'rgba(255,215,0,0.6)',
                            borderWidth : 1
                        }
                    }
                },
                ribbonType:false,
                minRadius : constMinRadius,
                maxRadius : constMaxRadius,
                coolDown: 0.995,
                nodes:egoNodes,
                links:egoLinks,
                steps : 1
            }
        ]
    });

    theme=data['theme']
    option = {
                          toolbox: {
        show : true,
        feature : {
            saveAsImage : {show: true}
        }
    },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:theme["legend_data"]
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : theme["xAxis_data"]
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series :theme["series"]
    };
    myDirection.setOption(option);
    }, "json");



    /**
     *egonet点击事件
     */
    var ecConfig = echarts.config;
    function eAnotherPage(param){
        if (typeof(param.data.id) == "undefined"){
           return
        }
//  	alert(""+param.data.value+"===="+param.data.name);

        if (param.data.id==-1){
            layer.open({
              type: 2,
              title: searchStr,
              shadeClose: true,
              shade: false,
              maxmin: true, //开启最大化最小化按钮
              area: ["80%","80%"],
              content: 'http://xueshu.baidu.com/s?wd='+param.data.name.replace('*','')+'&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2'
            });
		}else if (param.data.value!='#'){
		    window.open(""+param.data.id);
		}
    }
    myEgonet.on(ecConfig.EVENT.CLICK, eAnotherPage);

    function getId(){
        var reg = /profile\/([0-9]*)/
        return reg.exec(document.URL)[1];

    }

});
