var app = app || {};
$(function($){
	//Edit Story Controller
	app.EditStoryController = {
		init: function()
		{
			this.setUp();
		},
		setUp: function()
		{
			this.misc = app.Misc;
			
			var thisController = this;
			
			$("#fname").blur(function(e){
				thisController.updateField(e, "#fname_form");
			})
			$("#lname").blur(function(e){
				thisController.updateField(e, "#lname_form");
			})
			$("#city").blur(function(e){
				thisController.updateField(e, "#city_form");
			})
			$("#state").blur(function(e){
				thisController.updateField(e, "#state_form");
			})
			$("#email").blur(function(e){
				thisController.updateField(e, "#email_form");
			})
			$("#title").blur(function(e){
				thisController.updateField(e, "#title_form");
			})
			$("#company").blur(function(e){
				thisController.updateField(e, "#company_form");
			})
		},
		updateField: function(e, form)
		{
			var target = e.currentTarget,
				thisController = this,
				frm = $(form);
			 
			$.ajax({
			    type: frm.attr('method'),
				url: frm.attr('action'),
				data: frm.serialize(),
			    success: function (data) {
					if(data != 400){ 
						thisController.misc.headerAlert(data,"success",5000);
					}
				},
				error: function(data) {
					thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
			    }
			});
			return false;
			
		}
	}
});