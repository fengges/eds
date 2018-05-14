

function heredoc(fn) {
  return fn.toString().replace(/^[^\/]+\/\*!?\s?/, '')
    .replace(/\*\/[^\/]+$/, '').trim().replace(/>\s*</g, '><');
}

var CommonTools = {
  
  methods: {
    getData:function(url,type,data,success,error){
    json_data=JSON.stringify(data);
    $.ajax({
        url:url,
        type:type, //GET
        data:json_data,
        dataType:'json',
        success:success,
        error:error,
    });
    alert(json_data);
    },
    /**
     * http post
     */
    post:function(url, data) {
      var self = this;
      var index = layer.load();
      return this.$http.post(url, data).then((resp) => {
        layer.close(index);
        console.log(resp);
        var data = resp.data;
        if (!data){
          throw "数据异常，请联系管理员";
        }
        if (!data.success) {
          throw data.msg;
        } else {
          return data.obj;
        }
      }, (err) => {
        layer.close(index);
        throw "网络异常，请检查网络";
      });
    },

    /** 取查询参数 */
    getQueryParam:function(name) {
      var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
      var r = window.location.search.substr(1).match(reg);
      if (r != null) {
        return unescape(r[2]);
      } else {
        return null;
      }
    },
    
    /**
     * 显示提示信息
     */
    showMsg:function(msg, cb) {
      layer.msg(msg? msg: '操作成功', {
        time: 2000,
        offset: 't',
        anim: 6
      }, function(){
        cb && cb();
      });
    },
    
    /**
     * 显示错误信息
     */
    showError:function(err) {
      layer.alert(err? err: '操作失败', {icon: 5});
    },
    
    /**
     * 提示信息
     */
    confirm : function(msg, ok, cacenl) {
      var index = layer.confirm(msg, function() {
        layer.close(index);
        if (ok) {
          ok();
        }
      }, function() {
        layer.close(index);
        if (cacenl) {
          cacenl();
        }
      });
    },
    
  }
  
};