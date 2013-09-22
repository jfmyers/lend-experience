var app = app || {};
$(function($){
	//EditContributionController
	app.EditContributionController = {
		init: function()
		{
			this.formHandler();			
			this.misc = app.Misc;
		},
		formHandler: function()
		{
			var thisController = this,
			 	frm = $('#existing_contribution_form');

			frm.submit(function (e) {
				e.preventDefault();
				// Get description with formatting and place in the formatted text area
				$("#formatted_description").text( $("#editor").html() );
				// Get rid of formatting from description and place in description text area
				$("#description").text( thisController.misc.cleanEditorText() );
				// Display the loader gif.
				$(".saving-form").removeClass("blank");
				// Disable the submit button.
				$("#submit").attr("disabled",true);
				// Submit the form via ajax.
				
				$.ajax({
			    	type: frm.attr('method'),
					url: frm.attr('action'),
					data: frm.serialize(),
			        success: function (data) {
						$(".saving-form").addClass("blank");
						$("#submit").attr("disabled",false);
						thisController.misc.headerAlert("Your experience has been saved!","success",8000);
					},
					error: function(data) {
						$("#submit").attr("disabled",false);
						$(".saving-form").addClass("blank");
						
						//Display error messages.
						if(data.status == 400) {
							if(data.responseText.title != null) {
								thisController.misc.inputBorderAlert("#title");
								thisController.misc.headerAlert("A title for your experience is required!","error",8000);
							} else if(data.responseText.description != null) {
								thisController.misc.inputBorderAlert("#editor");
								thisController.misc.headerAlert("A description for your experience is required!","error",8000);
							} else {
								thisController.misc.headerAlert("Something went wrong! Please refresh the page and try again.","error",15000);
							}
						} else {
							thisController.misc.headerAlert("Access forbidden. Further attempts to modify this experience will result in the termination of your Lend Experience account.","error",50000);
						}
			        }
				});
			});	
		}
	}
});