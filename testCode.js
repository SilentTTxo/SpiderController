// 插入jq代码
var script = document.createElement("script");
script.type = "text/javascript";
script.src = "https://code.jquery.com/jquery-3.2.1.slim.js";
document.body.appendChild(script);

// 新建classic爬虫
Name = $("#newSpiderName_classic").val("GGG6")
Other = $("#newSpiderOther_classic").val("dsa")
Item = $("#newSpiderItem_classic").val("html")
Href = $("#newSpiderHref_classic").val("#leftcolumn > a::attr(href)")
StartUrl = $("#newSpiderStartUrl_classic").val("http://www.runoob.com/django/django-model.html")
$("#addParamItem_classic").click()
$($(".param_classic")[0]).val("H1")
$($(".param_classic")[1]).val("h1::text")

// 新建menu1爬虫
Name = $("#newSpiderName_menu1").val("menu1")
Other = $("#newSpiderOther_menu1").val("dsa")
Item = $("#newSpiderItem_menu1").val("html")
Href = $("#newSpiderHref_menu1").val(".sons > p > a::attr(href)")
StartUrl = $("#newSpiderStartUrl_menu1").val("http://so.gushiwen.org/type.aspx")
NextUrl = $("#newSpiderNextHref_menu1").val(".pages > a::attr(href)")
$("#addParamItem_menu1").click()
$($(".param_menu1")[0]).val("H1")
$($(".param_menu1")[1]).val("h1::text")

// 新建menuN爬虫
Name = $("#newSpiderName_menuN").val("menuN")
Other = $("#newSpiderOther_menuN").val("dsa")
Item = $("#newSpiderItem_menuN").val("html")
Href = $("#newSpiderHref_menuN").val(".sons > p > a::attr(href)")
StartUrl = $("#newSpiderStartUrl_menuN").val("http://so.gushiwen.org/type.aspx")
NextUrl = $("#newSpiderNextHref_menuN").val(".pages > a::attr(href)")
$("#addHrefItem_menuN").click()
$("#addHrefItem_menuN").click()
$("#addHrefItem_menuN").click()
$($(".href_menuN")[0]).val(".son5")    
$($(".href_menuN")[1]).val("son5-2")
$($(".href_menuN")[2]).val("son5-3")
$($(".addParamItem_menuN")[0]).click()
$($(".addParamItem_menuN")[1]).click()
$($(".addParamItem_menuN")[2]).click()
$($(".param_menuN")[0]).val("yiwen");$($(".param_menuN")[1]).val(".shangxicont::text")
$($(".param_menuN")[2]).val("chuangzuobeijing");$($(".param_menuN")[3]).val(".shangxicont::text")
$($(".param_menuN")[4]).val("jianshang");$($(".param_menuN")[5]).val(".shangxicont::text")

i.css(".son5")[2].css("a::attr(href)")[0].extract()