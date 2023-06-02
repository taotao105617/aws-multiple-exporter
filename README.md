### 场景
aws多账号多可用区多云产品的exporter

### 配置说明
>conf/configs.py  配置文件    
conf/metrics/*.yaml 相对应的云资源的监控指标文件

### 启动方式
```
sh build.sh  
docker-compose up -d   
```

### 如何接入新的云资源

>1. 在models/ 下新建一个对应的云资源的路径
>2. 参考aws_redis的模式获取实例信息，并生成"标准化"的数据结构
>3. 在service下的aws_svc.py 文件 下引用新的云资源，并在class_dict注册相应信息
>4. conf/configs.py的 ProductNamespaceF 添加云资源的信息
>5. conf/metrics/ 下增加相应的指标配置，命名需要规范（比如：redis --> redis.yaml，rds --> rds.yaml）
>6. conf/config.yaml 下增加云资源的启动端口
>7. 最后在docker-compose中添加相应云资源的配置,参考原有配置
>
> 上述对应的云资源的命名都需要一致，如云资源为redis，则上述命名具需要为redis，才可被自动发现
