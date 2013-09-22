var app = app || {};
$(function($){
	//Misc. Functions
	app.Misc = {
		isValidEmailAddress: function(emailAddress)
		{
		 	var pattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
			return pattern.test(emailAddress);
		},
		warning:function(selector, width, text, placement)
		{
			var options = {title:"",content:"<div style='float:left;width:"+width+"px;height:auto;padding: 2px 0px 8px 0px;'><h6 style='float:left;width:auto;height:auto;margin:0px;padding:0px;color:#f26d4f;'>"+text+"</h6><i style='float:left;width:18px;height:18px;margin:2px 0px 0px 12px;padding:0px;opacity:.65;' class='icon-exclamation-sign'></i></div>",trigger:'manual',html:true,placement:placement};
			$(selector).popover(options);
			$(selector).popover('show');
			var t = setTimeout(function(){
				$(selector).popover('destroy');
			},3000);
		},
		headerAlert:function(text, type, timeout)
		{	
			$(".header-alert").remove();
			var bgStyle,
			 	alertClass,
				top;
				
			if( type == "error") {
				bgStyle = "headerAlertError";
			} else if(type == "success") {
				bgStyle = "headerAlertSuccess";
			} else if(type == "warning") {
				bgStyle = "headerAlertError";
			}
			var scrollTop = $(window).scrollTop();
			if(scrollTop >= 50) {
				top = scrollTop;
			} else {
				top;
			}

			$("body").prepend("<div class='header-alert blank "+bgStyle+"' style='top:"+top+"px;'><div><p>"+text+"</p></div></div>");
			$(".header-alert").hide().removeClass('blank').fadeIn();
			setTimeout(function(){
				$(".header-alert").fadeOut();
			},timeout)
			
			$(window).scroll(function(){
				$(".header-alert").fadeOut(250);
			})
		},
		cleanEditorText: function()
		{
			var allText = $("#editor").html().split("<");
			var text = allText[0].trim();
			_.each($("#editor").children(),function(child){
				text = text + " " + $(child).text().trim();
			})
			text = text.replace(/\s{2,}/g,' ');
			return text;
		},
		inputBorderAlert: function(selector)
		{
			currentBorder = $(selector).css("border");
			$(selector).css("border","1px solid #F0BCB0");
			setTimeout(function(){
				$(selector).css("border",currentBorder);
			},4000);
			$(selector).focus();
		}
	}
});