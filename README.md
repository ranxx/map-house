# map-house

## crawl.py

用来爬取58出租信息

## unique.py

是用来去重的

## 部署

先爬取某个城市的出租信息
```bash
python3 crawl.py 北京
```
然后启动服务
```bash
python3 -m http.server 3000
```
在浏览器访问 0.0.0.0:3000 就能看到地图，可以在导入爬取城市的出租信息