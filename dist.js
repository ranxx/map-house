var city=[
   ["北京市","天津市","上海市","重庆市"],
   ["广州市","深圳市","珠海市","东莞市"],
   ["南京市","苏州市","南通市","常州市"],
   ["福州市","厦门市","莆田市","泉州市"]
   ];
var district=[
    [
        ["东城区","西城区","宣武区"],["和平区","红桥区","塘沽区"],["杨浦区","徐汇区"],["万州区","涪陵区"]
    ],
    [
        ["天河区","海珠区","白云区","番禺区"],["南山区","宝安区","福田区"],["香洲区","斗门区","金湾区"],["东城区","莞城区","万江区"]
    ],
    [
        ['玄武区','白下区','秦淮区','建邺区'],['沧浪区','平江区','金阊区','虎丘区'],['崇川区','港闸区','海安县','如东县'],['天宁区','钟楼区','新北区']
    ],
    [
        ['鼓楼区','台江区','仓山区','马尾区'],['思明区','海沧区','湖里区','集美区'],['城厢区','涵江区','荔城区','秀屿区'],['鲤城区','丰泽区','洛江区','泉港区']
    ]
];
function getCity(){
    //获得省份下拉框的对象
    console.log(document.getElementById('province').fo .selectedIndex)
    var sltProvince=document.forms[0].province;
    //获得城市下拉框的对象
    var sltCity=document.forms[0].city;     
    //获得市区下拉框的对象
    var sltDistrict=document.forms[0].district;
    //得到对应省份的城市数组
    var provinceCity=city[sltProvince.selectedIndex - 1];  
    //清空城市下拉框，仅留提示选项
    sltCity.length=1;
      sltDistrict.length=1;
    //将城市数组中的值填充到城市下拉框中
    for(var i=0;i<provinceCity.length;i++){
       sltCity[i+1]=new Option(provinceCity[i],provinceCity[i]);
    }
}
function getDistrict() {
    var sltProvince=document.forms[0].province;
     //获得城市下拉框的对象
    var sltCity=document.forms[0].city;     
    //获得市区下拉框的对象
    var sltDistrict=document.forms[0].district;
    //得到对应城市的市区数组
    var cityDistrict=district[sltProvince.selectedIndex - 1][sltCity.selectedIndex - 1];
    //清空城市下拉框，仅留提示选项
    sltDistrict.length=1;
    //将市区数组中的值填充到市区下拉框中
    for(var i=0;i<cityDistrict.length;i++){
       sltDistrict[i+1]=new Option(cityDistrict[i],cityDistrict[i]);
    }
}