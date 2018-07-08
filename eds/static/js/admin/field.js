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
  el : '#field',

  delimiters: ['${', '}'],
  unsafeDelimiters :['{!!', '!!}'],

  data : function() {
      return {
       dialogVisible: false,
        teacherData:[],
        field:"",
        fields:[],
        fieldData: [],
        selectedField: [],
        filterMethod(query, item) {
          return item.key.indexOf(query) > -1 ||item.label.indexOf(query) > -1;
        },
       page:1,
	   pPageNum:10,
	   num:0,

      };
    },
    computed:{
       fieldName:function(){
           field=this.fields[this.field]
           if (field==""|| typeof(field) == "undefined"){
                return ""
           }
           return field.name
       }
    },
     watch: {
          field:function (newQuestion, oldQuestion) {
                this.teacherLoad();
          },
     },
     methods: {
         handleAdd(row){
            row.selected=1;
            this.changeTeacherField(row.id,row.selected);
         },
        handleDelete(row){
        row.selected=0;
        this.changeTeacherField(row.id,row.selected);
     },
     changeTeacherField(id,selected){
        url='/admin/changeTeacherField';
        var data={selected:selected,id:id}
        self=this;
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
                re=data.success
                if (!re){
                    layer.alert(data.msg)
                }
                layer.closeAll('loading');
            },
            error:function (res) {
                layer.closeAll('loading');
            }
        });
     },

     tableRowClassName({row, rowIndex}) {
        if (row.selected === 1) {
          return 'warning-row';
        }
        return '';
      },
         handleSizeChange(val) {
            this.pPageNum=val;
            this.teacherLoad();
          },
          handleCurrentChange(val) {
            this.page=val;
            this.teacherLoad();
          },
      teacherLoad:function(){
                field=this.fields[this.field]
                if (!field){
                    return ;
                }
                var data= {field:field.discipline_code,page:this.page,pPageNum:this.pPageNum};
                data= {
                    data: JSON.stringify(data),
                };
                field_code=field.discipline_code;
                url='/admin/getTeacherByField';
                self=this;
                layer.load(2);
                $.ajax({
                    url:url,
                    type:'POST',
                    data:data,
                    dataType: 'json',
                    success:function(data){
                        re=data.obj;
                        self.teacherData=re["result"];
                        self.num=re["num"]
                        layer.closeAll('loading');
                    },
                    error:function (res) {
                        layer.closeAll('loading');
                    }
                });
      },
      setField:function(){
         data=[]
         if (this.checkField()){
                this.fields=[];
                for(var i=0;i<this.fieldData.length;i++){
                     if(this.selectedField.indexOf(this.fieldData[i].key)>=0){
                           this.fields.push(this.fieldData[i].obj);
                           data.push(this.fieldData[i].key);
                     }
                }
                this.teacherLoad();
                url='/admin/setField';
                self=this;
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
                        re=data.success
                        if (!re){
                            layer.alert(data.msg)
                        }
                        layer.closeAll('loading');
                    },
                    error:function (res) {
                        layer.closeAll('loading');
                    }
                });
                this.dialogVisible=false;
         }
      },
      checkField:function(){
        num=this.selectedField.length;
        if (num>5){
          this.$message({
          message: '领域数应当在3-5之间',
          type: 'warning'
        });
        return false;
        }else if(num<3){
          this.$message({
          message: '领域数应当在3-5之间',
          type: 'warning'
        });
        return false;
        }
        return true;
      },
      handleChange(value, direction, movedKeys) {
            this.checkField();
      }
    },

     created:function() {
                url='/admin/getField';
                self=this;
                layer.load(2);
                $.ajax({
                    url:url,
                    type:'POST',
                    dataType: 'json',
                    success:function(data){
                        re=data.obj;
                        for(var i=0;i<re.length;i++){
                            if (re[i].selected==1){
                               self.fields.push(re[i])
                               self.selectedField.push(re[i]["discipline_code"])
                            }
                            self.fieldData.push({
                                label: re[i]["name"],
                                key:re[i]["discipline_code"],
                                obj: re[i]
                              });

                        }
                        self.teacherLoad();
                        layer.closeAll('loading');
                    },
                    error:function (res) {
                        layer.closeAll('loading');
                    }
                });
     },
  });
});