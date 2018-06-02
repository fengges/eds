
import math
from eds.config import pic_url
from eds.dao.expert.expertdao import expertDao

class ExpertService:

    def get_info(self,params):
        result=expertDao.get_info(params)
        return result

    def get_radar(self,params):
        result=expertDao.get_radar(params)
        result=expertDao.get_radar(params)
        list=[]
        for r in result:
            if result[r]<1:
                result[r]=1
        list.append(math.log(result['paper_num'],2))
        list.append(math.log(result['citation'],2))
        list.append(math.log(result['h_index'],2))
        list.append(math.log(result['g_index'],2))
        list.append(math.log(result['sociability'],2))
        return list

    def get_theme(self,params):
        result={}
        theme,data=expertDao.get_theme(params)
        result["legend_data"]=[]
        for t in theme:
            result["legend_data"].append(t["theme"])
        year_list=[]
        for d in data:
            year_list.append(int(d["year"]))
        try :
            max_year=max(year_list)
            min_year=min(year_list)
        except:
            max_year=2018
            min_year=2018
        result["xAxis_data"]=[]
        for i in range(min_year,max_year+1):
            result["xAxis_data"].append(str(i))
        result["series"]=[]
        dic = sorted(data, key=lambda x: x['theme'], reverse=True)
        for t in result["legend_data"]:
            teacher_theme={}
            teacher_theme["name"]=t
            teacher_theme["type"] = 'line'
            teacher_theme["stack"] = '总量'
            teacher_theme["smooth"]=True
            teacher_theme["itemStyle"]={}
            teacher_theme["itemStyle"]["normal"]={}
            teacher_theme["itemStyle"]["normal"]["areaStyle"]={"type": 'default'},
            teacher_theme["data"]=[0 for i in range(min_year,max_year+1)]
            for d in dic:
                if d['theme']==t:
                    y=int(d['year'])
                    teacher_theme["data"][y-min_year]=d['paper_num']
            result["series"].append(teacher_theme)
        theme_count={}
        for r in result["series"]:
            theme_count[r['name']]=sum(teacher_theme["data"])
        c1 = sorted(theme_count, key=lambda x: x[1], reverse=True)
        if len(c1) - 5 >= 0:
            n = 5
        else:
            n = len(c1)
        c1=c1[0:n]
        legend_data = []
        series=[]
        for i in range(len(result["legend_data"])):
            if result["legend_data"][i] in c1:
                legend_data.append(result["legend_data"][i])
                series.append(result["series"][i])
        result["legend_data"]=legend_data
        result["series"]=series
        if len(result["legend_data"])==0:
            result["legend_data"]=['label']
            result["series"]=[0]
        return result

    def get_ego(self,params):
        list=expertDao.get_ego(params)
        result={}
        nodes=[]
        links=[]
        root={
            'name': str(params[0]),
            'value': '#',
            'category': 0,
            'id': params[0],
            'depth': 0,
            'symbolSize':30
        }
        max_w=0
        nodes.append(root)
        for l in list:
            node={}
            id=l["coauthor"]
            node['name']=l['name']
            node['id'] = id
            node['depth']=1
            if l['w']>=max_w:
                max_w=l['w']
            if id==-1:
                node['category']=2
                node['label']=l['name'].split('*')[0]
            else :
                node['category']=1
                node['label'] = l['name']
            node['value']=node['label']
            nodes.append(node)

            link={}
            link['source']=root["name"]
            link['target'] = node["name"]
            links.append(link)
        divde=max_w/30
        for i in range(1,len(nodes)):
            nodes[i]['symbolSize']=list[i-1]['w']/divde
            links[i-1]['weight'] = 30-nodes[i]['symbolSize']+5
        result['nodes']=nodes
        result['links'] = links
        return result
    def get_pic(self,id):
        try:
            image = open(pic_url+'ExpertImgs/'+str(id)+'.jpg','rb')
        except:
            image = open(pic_url + 'ExpertImgs/demo.jpg', 'rb')
        return image
expertService=ExpertService()