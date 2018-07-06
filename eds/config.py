

environments={
    "aliyun":{
          "task":{
              "recode":{
                  "taskOpen": True,
                  "hour":1,
                  "minute":00,
                  "second":00
              },
          },
          "file":{
              "pic_url":"C://fengge/data/eds/",
              "ueditor_url":"C://fengge/data/eds",
          },
          "dbs": {
                "host": 'localhost',
                "user": 'root',
                "password": 'SLX..eds123',
                "database": 'eds_web',
            },
          "es":{
              "host":"127.0.0.1"
          },
    },
    "local":{
          "task":{
              "record":{
                  "taskOpen": False,
                  "hour":1,
                  "minute":00,
                  "second":00
              },
          },
            "file": {
                "pic_url": "E://eds/",
                "ueditor_url": "E://eds",
            },
            "dbs":{
                "host" : '47.104.236.183',
                "user": 'root',
                "password":'SLX..eds123',
                 "database" : 'eds_web',
            },
            "es": {
                "host": "47.104.236.183"
            },
    }
}


environment_name="local"

environment=environments[environment_name]

