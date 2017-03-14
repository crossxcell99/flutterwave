# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "moneywave"
app_title = "Moneywave"
app_publisher = "Frappe"
app_description = "Payment solution"
app_icon = "red"
app_color = "red"
app_email = "900llecx@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/moneywave/css/moneywave.css"
# app_include_js = "/assets/moneywave/js/moneywave.js"

integration_services = ["Moneywave"]

# include js, css files in header of web template
# web_include_css = "/assets/moneywave/css/moneywave.css"
# web_include_js = "/assets/moneywave/js/moneywave.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "moneywave.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "moneywave.install.before_install"
# after_install = "moneywave.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "moneywave.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"moneywave.tasks.all"
# 	],
# 	"daily": [
# 		"moneywave.tasks.daily"
# 	],
# 	"hourly": [
# 		"moneywave.tasks.hourly"
# 	],
# 	"weekly": [
# 		"moneywave.tasks.weekly"
# 	]
# 	"monthly": [
# 		"moneywave.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "moneywave.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "moneywave.event.get_events"
# }

