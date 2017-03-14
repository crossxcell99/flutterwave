
//$("button").off("click");

//$("#saveBtn").off('click').click( function (event) {
//	console.log("Hello World!");
//	return false;
//	});

$("#saveBtn").on("click", function (event) {
	console.log("Hello World!");
	console.log("Start>>>>>>>>>>>>>>>>>>>>")
	var objj = {}
	var obj = $("#checkout_details").serializeArray();
	//console.log(obj);
	for(var i=0;i<obj.length;i++){
		objj[obj[i].name]=obj[i].value
	}
	console.log(objj)

	frappe.call({
		method:"moneywave.templates.pages.moneywave_checkout.make_payment",
		args: objj,
		callback: function(data){
			console.log("drgregrrg^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
			console.log(data.message);
			console.log(data.message.status);
			console.log(data.message.data.authurl);

			if(data.message.status === 'success'){
				console.log('##################################')
				//var iframe = $("#iframe");
				//iframe.contentWindow.document.write(data.message.data.responsehtml);​
				//var newWindow = window.open('Dynamic Popup', 'height=' + iframe.height() + ', width=' + iframe.width() + 'scrollbars=auto, resizable=no, location=no, status=no');
				$('#div_id').empty();
				$tetx = $('<p>');
				$tetx.text("Redirecting to authorization page");
				$('#div_id').append($tetx);
				window.setTimeout(function()
					{
						window.location.href = data.message.data.authurl;
					},
						3000);
				}
			}
	})
});

$(document).ready(function(){
	frappe.call({
		method:"moneywave.templates.pages.moneywave_checkout.get_url_params",
		args: {'url':window.location.href},
		callback: function(data){
			console.log(data.message)
			var obj = $("#checkout_details").serializeArray();
			console.log(obj);
			}
			});
		});