# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import frappe
from frappe.utils import get_url, call_hook_method, cint
from frappe import _
import urllib, json
import requests
from frappe.integration_broker.doctype.integration_service.integration_service import IntegrationService

class MoneywaveSettings(IntegrationService):


	service_name = "Moneywave"
	supported_currencies = ["NGN"]

	def live_or_test(self):

		if self.use_test:
			return "https://moneywave.herokuapp.com"
		else:
			return "https://live.moneywaveapi.co"

	def validate(self):
		if not self.flags.ignore_mandatory:
			self.validate_moneywave_credentails()

	def on_update(self):
		pass


	def enable(self):
		call_hook_method('payment_gateway_enabled', gateway='Razorpay')

		if not self.flags.ignore_mandatory:
			self.validate_moneywave_credentails()

	def get_token(self):
		
		if self.api_key and self.api_secret:

			self.m_token = json.loads(requests.post(self.live_or_test() + "/v1/merchant/verify",
				data={"apiKey": self.api_key, "secret":self.api_secret}).text)
			return self.m_token['token']
		else:
			frappe.throw(_("Please enter api credentials"))
			#return self.m_token

	def validate_moneywave_credentails(self):

		self.get_token()
		if self.m_token['status'] != 'success':
			frappe.throw(_("Seems API Key or API Secret is wrong"))

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(_("Please select another payment method. {0} does not support transactions in currency '{1}'").format(self.service_name, currency))

	def get_payment_url(self, **kwargs):
		m_kwargs = kwargs
		m_kwargs.update({'token':self.get_token()})
		return get_url("./moneywave_checkout?{0}".format(urllib.urlencode(m_kwargs)))

	def create_request(self, data):
		self.data = frappe._dict(data)

		try:
			self.integration_request = super(MoneywaveSettings, self).create_request(self.data, "Host", \
				"Moneywave")
			return self.authorize_payment()

		except Exception:
			frappe.log_error(frappe.get_traceback())
			return{
				"redirect_to": frappe.redirect_to_message(_('Server Error'), _("Seems issue with moneywave server's config. Don't worry, in case of failure amount will get refunded to your account.")),
				"status": 401
			}

	def authorize_payment(self):
		# writemsg(self.integration_request)
		# writemsg(self.integration_request.data.paystack_payment_ref)
		"""
		An authorization is performed when user’s payment details are successfully authenticated by the bank.
		The money is deducted from the customer’s account, but will not be transferred to the merchant’s account
		until it is explicitly captured by merchant.
		"""

		data = json.loads(self.integration_request.data)
		redirect_to = data.get('notes', {}).get('redirect_to') or None
		redirect_message = data.get('notes', {}).get('redirect_message') or None

		try:
			resp = json.loads(requests.post(self.live_or_test() + "/v1/transfer", data = self.m_token).text)
			if resp['status'] == "success":
				self.integration_request.db_set('status', 'Authorized', update_modified=False)
				self.flags.status_changed_to = "Authorized"
			else:
				frappe.log_error(str(resp), 'Moneywave Payment not authorized')
		except:
			frappe.log_error(frappe.get_traceback())
			# failed
			pass

		status = frappe.flags.integration_request.status_code
		if self.flags.status_changed_to == "Authorized":
			if self.data.reference_doctype and self.data.reference_docname:
				custom_redirect_to = None
				if self.data.reference_doctype == "Sales Invoice" and self.data.reference_docname:
					utils.update_sales_invoice(self.data.reference_docname)
				try:
					custom_redirect_to = frappe.get_doc(self.data.reference_doctype,
						self.data.reference_docname).run_method("on_payment_authorized", self.flags.status_changed_to)
				except Exception:
					frappe.log_error(frappe.get_traceback())

				if custom_redirect_to:
					redirect_to = custom_redirect_to

			redirect_url = 'payment-success'
		else:
			redirect_url = 'payment-failed'

		if redirect_to:
			redirect_url += '?' + urllib.urlencode({'redirect_to': redirect_to})
		if redirect_message:
			redirect_url += '&' + urllib.urlencode({'redirect_message': redirect_message})

		return {
			"redirect_to": redirect_url,
			"status": status
		}
	
	def get_service_details(self):
		return """
			<div>
				<p> Steps to configure Service
				<ol>
					<li> Get Paystack api credentials by login to:
						<a href="https://paystack.com/" target="_blank">
							https://paystack.com/
						</a>
					</li>
					<br>
					<li> Setup credentials on Paystack Settings doctype.
						Click on
						<button class="btn btn-default btn-xs disabled"> Paystack Settings </button>
						top right corner
					</li>
					<br>
					<li>
						After saving settings,
							<label>
								<span class="input-area">
									<input type="checkbox" class="input-with-feedback" checked disabled>
								</span>
								<span class="label-area small">Enable</span>
							</label>
						Paystack Integration Service and Save a document.
					</li>
					<br>
					<li>
						To view Paystack's payment logs,
						<button class="btn btn-default btn-xs disabled"> Show Log </button>
					</li>
				</ol>
			</div>
		"""

def post_request(url, auth=None,data={}):

	headers = {}
	if not auth:
		return

	headers['Content-Type'] = 'application/json'
	if not data=={}:
		data = json.dumps(data)

	try:
		s = get_request_session()
		frappe.flags.integration_request = s.post(url, data=data, headers=headers)
		frappe.flags.integration_request.raise_for_status()
		return frappe.flags.integration_request.json()
	except Exception, exc:
		frappe.log_error(frappe.get_traceback())
		raise exc

@frappe.whitelist()
def get_bank_code():
	rr = json.loads(requests.post("https://moneywave.herokuapp.com/banks").text)
	rrr = ''
	for i in rr['data']:
		rrr = rrr + '<p>' + str(rr['data'][i]) + '    :' + str(i) + '</p>'
	return rrr
