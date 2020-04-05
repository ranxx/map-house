var map = new AMap.Map("container", {
    resizeEnable: true,
    zoomEnable: true,
    // 11448159,25.012759
    center: [102.715915, 25.012759],
    zoom: 13
});

// 添加标尺，参考带功能控件的地图。
var scale = new AMap.Scale();
map.addControl(scale);

//公交到达圈对象
var arrivalRange = new AMap.ArrivalRange();
//步行
// var walking = new AMap.Walking();
//经度，纬度，时间（用不到），通勤方式（默认是地铁＋公交）
var x, y, t, vehicle = "SUBWAY,BUS";
//工作地点，工作标记
var workAddress, workMarker;
//房源标记队列
var rentMarkerArray = [];
//多边形队列，存储公交到达的计算结果
var polygonArray = [];
//路径规划
var amapTransfer;
//
var addressMap = new Map();
// setInterval(() => {
//     showWorklocation()
// }, 1000);
setTimeout(()=>{
    showWorklocation()
}, 5000)

// setTimeout(()=>{
//     console.log("addressMap.length", addressMap.length)
// }, 200000)

//信息窗体对象,在房源标记被点击时弹出，参考给多个点添加信息窗体。
var infoWindow = new AMap.InfoWindow({
    offset: new AMap.Pixel(0, -30)
});

// // //地址补完的使用，参考输入提示后查询。
// var auto = new AMap.Autocomplete({
//     //通过id指定输入元素
//     input: "work-location"
// });

// //添加事件监听，在选择补完的地址后调用workLocationSelected
// AMap.event.addListener(auto, "select", workLocationSelected);

function takeBus(radio) {
    vehicle = radio.value;
    loadWorkLocation()
}

function takeSubway(radio) {
    vehicle = radio.value;
    loadWorkLocation()
}

function walking(radio) {
    vehicle = radio.value;
    loadWorkLocation()
}

function importRentInfo(fileInfo) {
    // console.log(fileInfo.files[0].name)
    // return
    var file = fileInfo.files[0].name;
    console.log(file)
    loadRentLocationByFile(file);
}

//更新工作地点，加载公交到达圈
function workLocationSelected(e) {
    workAddress = e.poi.name;
    // console.log(e)
    loadWorkLocation();
}

function citySelect(e) {
    address = e.poi
    // console.log(address.adcode)
    console.log(address.district)
    console.log(address.location)
    // 取出 省 市 县
    // 取出 市 区
    // 只要市
    // alls = String(address.district).match("(.*?)\省(.*?)\市(.*?)\县")
    // if (!alls ){
    //     alls = String(address.district).match("(.*?)\市(.*?)\区")
    // }
    //if (alls.length < 3) {

        //alls = String(address.district).match("(.*?)\市(.*?)\区")
    //}
    // console.log(alls)
    // city = alls[2]
    // subcity = ""
    // if (alls.length > 3) {
    //     subcity = alls[3]
    // }
    //map.setZoomAndCenter(12, [address.location.lng, address.location.lat]);
    // // 定位
    var geocoder = new AMap.Geocoder({
        city: address.district,
        radius: 1000
    });
    geocoder.getLocation(address.district, function(status, result) {
        if (status === "complete" && result.info === 'OK') {
            var geocode = result.geocodes[0];
            x = geocode.location.getLng();
            y = geocode.location.getLat();
            console.log(geocode)
            //地图移动到工作地点的位置
            map.setZoomAndCenter(12, [x, y]);
        }else{
            console.log("falt",status, result)
        }
    })
}



function loadWorkMarker(x, y, locationName) {
    workMarker = new AMap.Marker({
        map: map,
        title: locationName,
        icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
        position: [x, y]
    });
}

// function walkingRange(x,y,t,color,v) {
//     walking.search([x,y], t, function(status, result) {
        
//     })
// }

// 在地图上绘制到达圈，参考：公交到达圈。
function loadWorkRange(x, y, t, color, v) {
    arrivalRange.search([x, y], t, function(status, result) {
        if (result.bounds) {
            for (var i = 0; i < result.bounds.length; i++) {
                var polygon = new AMap.Polygon({
                    map: map,
                    fillColor: color,
                    fillOpacity: "0.4",
                    strokeColor: color,
                    strokeOpacity: "0.8",
                    strokeWeight: 1
                });
                polygon.setPath(result.bounds[i]);
                polygonArray.push(polygon);
            }
        }
    }, {
        policy: v
    });
}

function addMarkerByAddress(obj) {
    address = obj.address
    var geocoder = new AMap.Geocoder({
        city: obj.city,
        radius: 1000
    });
    geocoder.getLocation(address, (status, result)=> {
        if (status === "complete" && result.info === 'OK') {
            var geocode = result.geocodes[0];
            rentMarker = new AMap.Marker({
                map: map,
                title: obj.title,
                icon: 'http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
                position: [geocode.location.getLng(), geocode.location.getLat()]
            });
            rentMarker.content = '<div class="panel-body" style="min-height: 100px; max-height: 300px; overflow:scroll">'+"<div>房源：<a target = '_blank' href='" + obj.url + "'>" + obj.title + "</a>"+
            "<p>房价："+obj.price+"</p>"+
            "<p>来源："+obj.source+"</p>"+"</div></div>"
            rentMarker.address = obj.address
            rentMarker.title = obj.title
            // addressMap.set(obj.address, rentMarker)
            tmp = addressMap.get(obj.address)
            if (tmp != null) {
                tmp.content = tmp.content.replace('<div class="panel-body" style="min-height: 100px; max-height: 300px; overflow:scroll">','')
                index = rentMarker.content.lastIndexOf('</div>')
                rentMarker.content = rentMarker.content.substr(0, index)
                rentMarker.content += tmp.content
                // console.log(rentMarker.content)
                rentMarker.title += "\n"+ tmp.title
                map.remove(tmp)
            }
                rentMarkerArray.push(rentMarker);
                addressMap.set(obj.address, rentMarker)
            
            // 在房源标记被点击时打开
            rentMarker.on('click', (e)=> {
                workAddress = document.getElementById('work-location').value
                //鼠标移到标记上会显示标记content属性的内容
                infoWindow.setContent(e.target.content);
                //在标记的位置打开窗体
                infoWindow.open(map, e.target.getPosition());
                if( !workAddress && workAddress == "") {
                    console.log('没有选择工作地，所以没有路径规划')
                    return
                }
                if (amapTransfer) amapTransfer.clear();
                amapTransfer = new AMap.Transfer({
                    map: map,
                    policy: AMap.TransferPolicy.LEAST_TIME,
                    city: obj.city,
                    panel: 'transfer-panel'
                });
                amapTransfer.search([{
                    keyword: e.target.address
                }, {
                    keyword: workAddress
                }], function(status, result) {})
            });
        }
    })
}

function delWorkLocation() {
    if (polygonArray) map.remove(polygonArray);
    if (workMarker) map.remove(workMarker);
    polygonArray = [];
}

function delRentLocation() {
    if (rentMarkerArray) map.remove(rentMarkerArray);
    rentMarkerArray = [];
}

function showWorklocation() {
    if (workMarker) map.remove(workMarker);
    var flag = false
    console.log(workAddress)
    if ( workAddress != null && workAddress != "" && workAddress != document.getElementById('work-location').value) {
        if (polygonArray) {map.remove(polygonArray);flag=true}
    }
    workAddress = document.getElementById('work-location').value
    var geocoder = new AMap.Geocoder({
        city: "昆明市",
        radius: 1000
    });
    geocoder.getLocation(workAddress, function(status, result) {
        if (status === "complete" && result.info === 'OK') {
            var geocode = result.geocodes[0];
            x = geocode.location.getLng();
            y = geocode.location.getLat();
            //加载工作地点标记
            loadWorkMarker(x, y);
            if (flag) {
                //加载60分钟内工作地点到达圈
                loadWorkRange(x, y, 60, "#3f67a5", vehicle);
            }
        }
    })
}

function loadWorkLocation() {
    //首先清空地图上已有的到达圈
    delWorkLocation();
    var geocoder = new AMap.Geocoder({
        city: "昆明市",
        radius: 1000
    });

    geocoder.getLocation(workAddress, function(status, result) {
        if (status === "complete" && result.info === 'OK') {
            var geocode = result.geocodes[0];
            x = geocode.location.getLng();
            y = geocode.location.getLat();
            //加载工作地点标记
            loadWorkMarker(x, y);
            //加载60分钟内工作地点到达圈
            loadWorkRange(x, y, 60, "#3f67a5", vehicle);
            //地图移动到工作地点的位置
            map.setZoomAndCenter(12, [x, y]);
        }
    })
}

function loadRentLocationByFile(fileName) {
    //先删除现有的房源标记
    delRentLocation();
    //所有的地点都记录在集合中
    var rent_locations = new Set();
    //jquery操作
    $.get(fileName, function(data) {
        data = data.split("\n");
        data.forEach(function(item, index) {
            items = item.split(",")
            // [房源名称，地址，月租，房源url地址]。
            if (!items || items.length < 1 || items[0].length < 0) {
                return
            }
            obj={
                city:"昆明市",
                source: "58同城",
                title:items[0],
                address:items[1],
                price:items[2],
                url:items[3]
            }
            rent_locations.add(obj);
        });
        rent_locations.forEach(function(element, index) {
            //加上房源标记
            addMarkerByAddress(element);
        });
    });
}

function wwww(params) {
    console.log("aj ndoa")
}