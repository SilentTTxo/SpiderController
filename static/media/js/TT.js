String.prototype.format = function(args) {
	var result = this;
	if (arguments.length > 0) {    
		if (arguments.length == 1 && typeof (args) == "object") {
			for (var key in args) {
				if(args[key]!=undefined){
					var reg = new RegExp("({" + key + "})", "g");
					result = result.replace(reg, args[key]);
				}
			}
		}
		else {
			for (var i = 0; i < arguments.length; i++) {
				if (arguments[i] != undefined) {
                    //var reg = new RegExp("({[" + i + "]})", "g");//这个在索引大于9时会有问题，谢谢何以笙箫的指出
					var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}
showMsg = function(data){
			$.gritter.add({
				title: "提示",
				text: data,
				sticky: false,
				time: '2000'
			});
		}
var TT = {
	init : function(){
		//解除蒙版加载动画
		$("html").ajaxStop(function(){
			$(".loader").fadeOut();
		})
		//载入模板文件
		$(".page-sidebar-menu").load("/media/include/sidebar.html",function(){
			//初始化sidebar样式
			url = window.location.pathname
			url = url.split('/')[2]
			$("a[href='"+url+"']").parent().addClass("active");
			$("a[href='"+url+"']").parent().parent().parent().addClass("active");

			//载入页头
			$("#pageinfo").load("/media/include/pageinfo.html",function(){
				//填充页头
				$(".page-title")[0].innerHTML = $("a[href='"+url+"']")[0].innerHTML;
				$(".breadcrumb").append('<li><a href="#">'+$("a[href='"+url+"']").parent().parent().parent().children().children()[1].innerHTML+'</a><i class="icon-angle-right"></i></li>');
				$(".breadcrumb").append('<li><a href="#">'+$("a[href='"+url+"']")[0].innerHTML+'</a></li>');
			});

		});
		$("head").load("/media/include/head.html");
		$(".pull-right").load("/media/include/pull-right.html",function(){
			//填充用户名
			$.ajax({
				type:"GET",
				url:"/api/getUserInfo",
				success : function(result){
					result = jQuery.parseJSON(result);
					$("#username")[0].innerHTML = result['username'];
				}
			});
			$("#logout").click(function(){
				location.href='https://login.flyme.cn/sso/logout?useruri=http://corpus.tx-tools.meizu.com/system_info.html'
			})
		});
		$(".footer").load("/media/include/footer.html");
		
	},
	table : function(title,thName,param,style,apiUrl){
		var data = '<div class="portlet box green"><div class="portlet-title"><div class="caption"><i class="icon-cogs"></i>'+title+'</div><div class="tools"><a href="javascript:;" class="collapse"></a><a href="#portlet-config" data-toggle="modal" class="config"></a><a href="javascript:;" class="reload"></a><a href="javascript:;" class="remove"></a></div></div><div class="portlet-body"><table class="table table-hover"><thead><tr>'

		//添加table头
		for(i=0;i<thName.length;i++){
			data +="<th>"+thName[i]+"</th>";
		}

		//填充table数据
		$.ajax({
			type:"GET",
			url:apiUrl+"/getAll",
			success : function(result){
				result = jQuery.parseJSON(result);
				adata = result['data'];
				if(result['code'] == "1"){
					showMsg("获取数据成功");
					str = ""
					model = "";
					for(i=0;i<param.length;i++){
						model += "<td>{"+param[i]+"}</td>"
					}
					for(i in adata){
						str += "<tr>";
						str += model.format(adata[i]);
						str += "</tr>"
					}
					data+=str;
					data +="</table></div></div>"
					$(".dataContent").append(data);
				}
				else{
					showMsg("网络出错");
				}
			}
		})
	}
}
