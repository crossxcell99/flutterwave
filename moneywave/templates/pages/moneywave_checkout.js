
//$("button").off("click");

//$("#saveBtn").off('click').click( function (event) {
//	console.log("Hello World!");
//	return false;
//	});

$("#saveBtn").on("click", function (event) {
	console.log("Hello World!");
	console.log("Start>>>>>>>>>>>>>>>>>>>>");
	console.log(contained.urlparam);
	console.log('This is contained url');
	var objj = {}
	var obj = $("#checkout_details").serializeArray();
	//console.log(obj);
	for(var i=0;i<obj.length;i++){
		objj[obj[i].name]=obj[i].value
	}
	objj['amount']=contained.urlparam.amount
//	objj['redirecturl']=contained.urlparam.redirect_to
	objj['redirecturl']= window.location.protocol + '//'+ window.location.host + '/payment-result'
	objj['email']=contained.urlparam.payer_email
	console.log(objj)
	var opts = {
				  lines: 13 // The number of lines to draw
				, length: 14 // The length of each line
				, width: 3 // The line thickness
				, radius: 13 // The radius of the inner circle
				, scale: 0.5 // Scales overall size of the spinner
				, corners: 0.4 // Corner roundness (0..1)
				, color: '#000' // #rgb or #rrggbb or array of colors
				, opacity: 0.25 // Opacity of the lines
				, rotate: 0 // The rotation offset
				, direction: 1 // 1: clockwise, -1: counterclockwise
				, speed: 1 // Rounds per second
				, trail: 60 // Afterglow percentage
				, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
				, zIndex: 2e9 // The z-index (defaults to 2000000000)
				, className: 'spinner' // The CSS class to assign to the spinner
				, top: '50%' // Top position relative to parent
				, left: '50%' // Left position relative to parent
				, shadow: false // Whether to render a shadow
				, hwaccel: false // Whether to use hardware acceleration
				, position: 'absolute' // Element positioning
				}
	var target = document.getElementById('div_id')
	var spinner = new Spinner(opts).spin(target);

	frappe.call({
		method:"moneywave.templates.pages.moneywave_checkout.make_payment",
		args: objj,
		callback: function(data){
			console.log("##################-MAKE-PAYMENT-SECTION-######################");
			console.log(data.message.data);
			console.log(data.message.data.transfer);

			if(data.message.status !== 'success'){
				frappe.msgprint(data.message.message);
				console.log(data.message.message);
			}

			if(data.message.status === 'success'){

				$('#div_id').empty();
				$tetx = $('<p>');
				$tetx.text("Redirecting to authorization page");
				$('#div_id').append($tetx);

				var opts = {
							  lines: 13 // The number of lines to draw
							, length: 14 // The length of each line
							, width: 3 // The line thickness
							, radius: 13 // The radius of the inner circle
							, scale: 0.5 // Scales overall size of the spinner
							, corners: 0.4 // Corner roundness (0..1)
							, color: '#000' // #rgb or #rrggbb or array of colors
							, opacity: 0.25 // Opacity of the lines
							, rotate: 0 // The rotation offset
							, direction: 1 // 1: clockwise, -1: counterclockwise
							, speed: 1 // Rounds per second
							, trail: 60 // Afterglow percentage
							, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
							, zIndex: 2e9 // The z-index (defaults to 2000000000)
							, className: 'spinner' // The CSS class to assign to the spinner
							, top: '50%' // Top position relative to parent
							, left: '50%' // Left position relative to parent
							, shadow: false // Whether to render a shadow
							, hwaccel: false // Whether to use hardware acceleration
							, position: 'absolute' // Element positioning
							}
				var target = document.getElementById('loadingAnimation')
				var spinner = new Spinner(opts).spin(target);

				contained.transfer = data.message.data.transfer;
				contained.data = data.message.data;

				contained.options = {
							"amount":contained.urlparam.amount,
							"email":contained.urlparam.payer_email,
							"payer_name":contained.urlparam.payer_name,
							"id":contained.transfer.id,
						//	"request_name":contained.transfer.id,
							"reference_doctype":contained.urlparam.reference_doctype,
							"reference_docname":contained.urlparam.reference_docname,
							"flutter_charge_reference":contained.transfer.flutterChargeReference,
							"redirect_to":contained.urlparam.redirect_to,
						}

				frappe.call({
					method:"moneywave.templates.pages.moneywave_checkout.continue_payment",
					args:{
							"payment_ref": contained.transfer.flutterChargeReference,
							"options": contained.options,
							"reference_doctype": contained.urlparam.reference_doctype,
							"reference_docname": contained.urlparam.reference_docname
						},
					callback: function(dd){

						console.log("#############-CONTINUE PAYMENT IS CALLED-###################");
						console.log(dd);
						window.location.href = contained.data.authurl
					}

					});
				} 
			}

				//var iframe = $("#iframe");
				//iframe.contentWindow.document.write(data.message.data.responsehtml);​
				//var newWindow = window.open('Dynamic Popup', 'height=' + iframe.height() + ', width=' + iframe.width() + 'scrollbars=auto, resizable=no, location=no, status=no');
	});
});

var contained = Object();

$(document).ready(function(){
	frappe.call({
		method:"moneywave.templates.pages.moneywave_checkout.get_url_params",
		args: {'url':window.location.href},
		callback: function(data){
			console.log("//////////////////READY FUNCTION-CALL CALLED//////////////")
			console.log(data.message)
			contained.urlparam = data.message
			var obj = $("#checkout_details").serializeArray();
			console.log(obj);
			}
			});
	//console.log(contained.urlparam);
		});




      
 
//      	options = {
//		"amount":contained.urlparam.amount,
//		"email":contained.urlparam.payer_email,
//		"payer_name":contained.urlparam.payer_name,
//		"request_name":contained.transfer.id,
//		"reference_doctype":contained.urlparam.reference_doctype,
//		"reference_docname":contained.urlparam.reference_docname,
//		"paystack_payment_ref":contained.transfer.flutterChargeReference
//	}
//      paystack.make_payment_log(contained.transfer.flutterChargeReference, options, contained.urlparam.reference_doctype, contained.urlparam.reference_docname);
//    
//
//frappe.provide('moneywave');
//
//paystack.make_payment_log = function(response_reference, options, doctype, docname){
	//$('.paystack-loading').addClass('hidden');
	//$('.paystack-confirming').removeClass('hidden');
	// console.log(response_reference+" "+options+" "+doctype+" "+docname)

//	frappe.call({
//		method:'paystack_integration.templates.pages.paystack_checkout.make_payment',
//		args:{
//			"paystack_payment_ref": response_reference,
//			"options": options,
//			"reference_doctype": doctype,
//			"reference_docname": docname
//		},
//		callback: function(r){
//			if (r.message && r.message.status == 200) {
//				window.location.href = r.message.redirect_to
//			}
//			else if (r.message && ([401,400,500].indexOf(r.message.status) > -1)) {
//				window.location.href = r.message.redirect_to
//			}
//		}
//	});
//}
