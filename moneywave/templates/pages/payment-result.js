
$(document).ready(function(){

	frappe.call({
		method:"moneywave.templates.pages.moneywave_checkout.get_url_params",
		args: {'url':window.location.href},

		callback: function(data){
			console.log("//////////////////-GET URL PARAMS CALLED-//////////////")
			console.log(data.message)
			contained.urlparam = data.message

			if(contained.urlparam.transactionStatus === 'success'){
				$('#div_successful').removeClass('hidden');
			} else {
				$('#div_failed').removeClass('hidden');
			}
		}
	});
});

$("#continue_btn").on("click", function (event) {
	console.log('###########BUTTON CLICKED###################');
	//contained.urlparam = {'redirect_to':'userssz'}
	if(contained.urlparam.redirect_to){
		window.location.href = contained.urlparam.redirect_to
	} else{
		window.location.href = '/'
	}
	//window.location.href = 'http://google.com'
});

contained = Object();