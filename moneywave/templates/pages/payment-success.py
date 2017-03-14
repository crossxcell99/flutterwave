# -*- coding: utf-8 -*-
# Copyright (c) 2015, Manqala Ltd. and contributors
# For license information, please see license.txt


from __future__ import unicode_literals

import frappe

def get_context(context):
	token = frappe.local.form_dict.token
