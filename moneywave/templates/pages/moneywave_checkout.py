from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_url, flt
import urllib,requests,json,string,random
import json


no_cache = 1
no_sitemap = 1

# expected_keys = ('amount', 'payer_email')
expected_keys = ('amount', 'title', 'description', 'reference_doctype', 'reference_docname',
	'payer_name', 'payer_email', 'order_id')

@frappe.whitelist()
def get_url_params(url):
	from urlparse import urlparse,parse_qs
	o = urlparse(url)
	query = parse_qs(o.query)
	ret_query = dict()
	for i in query:
		ret_query.update({i:query[i][0]})
	return ret_query

@frappe.whitelist()
def make_payment(**obj):
	import requests
	moneywave_settings_py = frappe.get_doc("Moneywave Settings")
	#ax= dict(obj)
	obj.update({'apiKey':moneywave_settings_py.api_key,
				'firstname':moneywave_settings_py.first_name,
				'lastname':moneywave_settings_py.last_name,
				'recipient_bank':moneywave_settings_py.bank_code,
				'recipient_account_number':moneywave_settings_py.account_number,
				'fee':moneywave_settings_py.commission,
				'medium':'web',
				})
	headers = {'Authorization': str(moneywave_settings_py.get_token())}
	respp = json.loads(requests.post(str(moneywave_settings_py.live_or_test())+"/v1/transfer", data=obj, headers=headers).text)
	respp.update({'token':str(moneywave_settings_py.get_token())})
	return respp

def get_context(context):

	context.no_cache = 1
	context.public_key = frappe.db.get_value("Paystack Settings", None, "public_key")
	context.secret_key = frappe.db.get_value("Paystack Settings", None, "secret_key")
	context.amount = 0
	context.rand_ref = get_rand_ref()
	# TODO CHANGE THIS TO GET ADMIN EMAIL
	context.payer_email = "test@example.com"
	controller = frappe.get_doc("Paystack Settings")

	# all these keys exist in form_dict
	if not (set(expected_keys) - set(frappe.form_dict.keys())):
		for key in expected_keys:
			context[key] = frappe.form_dict[key]

		context['amount'] = flt(context['amount'])

	elif frappe.form_dict.payment_request:
		payment_req = frappe.get_doc('Payment Request', frappe.form_dict.payment_request)
		controller.validate_transaction_currency(payment_req.currency)

		if payment_req.status == "Paid":
			msg = """You have already paid for this order, Thank You.
					<p><a href="/"class="btn btn-primary">Back to Home</a></p>"""
			frappe.redirect_to_message(_('Already Paid'), _(msg))
			frappe.local.flags.redirect_location = frappe.local.response.location
			raise frappe.Redirect

		reference_doc = frappe.get_doc(payment_req.reference_doctype, payment_req.reference_name)

		context.amount = payment_req.grand_total
		context.title = reference_doc.company
		context.description = payment_req.subject
		context.doctype = payment_req.doctype
		context.name = payment_req.name
		context.payer_name = reference_doc.customer_name
		context.payer_email = payment_req.email_to or context.payer_email
		context.order_id = payment_req.name
		context.reference_doctype = payment_req.reference_doctype
		context.reference_docname = payment_req.reference_name

	else:
		frappe.redirect_to_message(_('Some information is missing'), _('Looks like someone sent you to an incomplete URL. Please ask them to look into it.'))
		frappe.local.flags.redirect_location = frappe.local.response.location
		raise frappe.Redirect


#@frappe.whitelist(allow_guest=True)
#def make_payment(paystack_payment_ref, options, reference_doctype, reference_docname):	
#	data = {}
#
#	if isinstance(options, basestring):
#		data = json.loads(options)
#
#	data.update({
#		"paystack_payment_ref": paystack_payment_ref,
#		"reference_docname": reference_docname,
#		"reference_doctype": reference_doctype
#	})
#
#	data =  frappe.get_doc("Paystack Settings").create_request(data)
#	frappe.db.commit()
#	return data


def get_rand_ref():
	rand = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(16)])
	return rand