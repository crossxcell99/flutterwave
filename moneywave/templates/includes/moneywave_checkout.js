
//$("button").off("click");

//$("#saveBtn").off('click').click( function (event) {
//	console.log("Hello World!");
//	return false;
//	});

$("#saveBtn").on("click", function (event) {
	console.log("Hello World!");
	var ax = frappe.form_dict
	console.log(ax)
	//return false;
});