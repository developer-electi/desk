from __future__ import unicode_literals

import unittest

import frappe
from frappe.desk.form.assign_to import add as add_assignment
from frappe.utils import add_months, getdate

from frappedesk.frappedesk.doctype.ticket.test_ticket import make_ticket
from frappedesk.frappedesk.doctype.sla.test_service_level_agreement import (
	create_service_level_agreements_for_tickets,
)
from frappedesk.frappedesk.report.ticket_analytics.ticket_analytics import execute

months = [
	"Jan",
	"Feb",
	"Mar",
	"Apr",
	"May",
	"Jun",
	"Jul",
	"Aug",
	"Sep",
	"Oct",
	"Nov",
	"Dec",
]


class TestTicketAnalytics(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# frappe.db.sql("delete from `tabTicket` where company='_Test Company'")
		frappe.db.set_value("Frappe Desk Settings", None, "track_service_level_agreement", 1)

		current_month_date = getdate()
		last_month_date = add_months(current_month_date, -1)
		self.current_month = str(months[current_month_date.month - 1]).lower()
		self.last_month = str(months[last_month_date.month - 1]).lower()
		if current_month_date.year != last_month_date.year:
			self.current_month += "_" + str(current_month_date.year)
			self.last_month += "_" + str(last_month_date.year)

	def test_ticket_analytics(self):
		create_service_level_agreements_for_tickets()
		create_ticket_types()
		create_records()

		self.compare_result_for_customer()
		self.compare_result_for_ticket_type()
		self.compare_result_for_ticket_priority()
		self.compare_result_for_assignment()

	def compare_result_for_customer(self):
		filters = {
			# "company": "_Test Company",
			"based_on": "Customer",
			"from_date": add_months(getdate(), -1),
			"to_date": getdate(),
			"range": "Monthly",
		}

		report = execute(filters)

		expected_data = [
			{
				"customer": "__Test Customer 2",
				self.last_month: 1.0,
				self.current_month: 0.0,
				"total": 1.0,
			},
			{
				"customer": "__Test Customer 1",
				self.last_month: 0.0,
				self.current_month: 1.0,
				"total": 1.0,
			},
			{
				"customer": "__Test Customer",
				self.last_month: 1.0,
				self.current_month: 1.0,
				"total": 2.0,
			},
		]

		self.assertEqual(expected_data, report[1])  # rows
		self.assertEqual(len(report[0]), 4)  # cols

	def compare_result_for_ticket_type(self):
		filters = {
			# "company": "_Test Company",
			"based_on": "Ticket Type",
			"from_date": add_months(getdate(), -1),
			"to_date": getdate(),
			"range": "Monthly",
		}

		report = execute(filters)

		expected_data = [
			{
				"ticket_type": "Discomfort",
				self.last_month: 1.0,
				self.current_month: 0.0,
				"total": 1.0,
			},
			{
				"ticket_type": "Service Request",
				self.last_month: 0.0,
				self.current_month: 1.0,
				"total": 1.0,
			},
			{"ticket_type": "Bug", self.last_month: 1.0, self.current_month: 1.0, "total": 2.0},
		]

		self.assertEqual(expected_data, report[1])  # rows
		self.assertEqual(len(report[0]), 4)  # cols

	def compare_result_for_ticket_priority(self):
		filters = {
			# "company": "_Test Company",
			"based_on": "Ticket Priority",
			"from_date": add_months(getdate(), -1),
			"to_date": getdate(),
			"range": "Monthly",
		}

		report = execute(filters)

		expected_data = [
			{"priority": "Medium", self.last_month: 1.0, self.current_month: 1.0, "total": 2.0},
			{"priority": "Low", self.last_month: 1.0, self.current_month: 0.0, "total": 1.0},
			{"priority": "High", self.last_month: 0.0, self.current_month: 1.0, "total": 1.0},
		]

		self.assertEqual(expected_data, report[1])  # rows
		self.assertEqual(len(report[0]), 4)  # cols

	def compare_result_for_assignment(self):
		filters = {
			# "company": "_Test Company",
			"based_on": "Assigned To",
			"from_date": add_months(getdate(), -1),
			"to_date": getdate(),
			"range": "Monthly",
		}

		report = execute(filters)

		expected_data = [
			{
				"user": "test@example.com",
				self.last_month: 1.0,
				self.current_month: 1.0,
				"total": 2.0,
			},
			{
				"user": "test1@example.com",
				self.last_month: 2.0,
				self.current_month: 1.0,
				"total": 3.0,
			},
		]

		self.assertEqual(expected_data, report[1])  # rows
		self.assertEqual(len(report[0]), 4)  # cols


def create_ticket_types():
	for entry in ["Bug", "Service Request", "Discomfort"]:
		if not frappe.db.exists("Ticket Type", entry):
			frappe.get_doc({"doctype": "Ticket Type", "__newname": entry}).insert()


def create_records():
	current_month_date = getdate()
	last_month_date = add_months(current_month_date, -1)

	ticket = make_ticket(current_month_date, 2, "High", "Bug")
	add_assignment(
		{"assign_to": ["test@example.com"], "doctype": "Ticket", "name": ticket.name}
	)

	ticket = make_ticket(last_month_date, 2, "Low", "Bug")
	add_assignment(
		{"assign_to": ["test1@example.com"], "doctype": "Ticket", "name": ticket.name}
	)

	ticket = make_ticket(current_month_date, 2, "Medium", "Service Request")
	add_assignment(
		{"assign_to": ["test1@example.com"], "doctype": "Ticket", "name": ticket.name}
	)

	ticket = make_ticket(last_month_date, 2, "Medium", "Discomfort")
	add_assignment(
		{
			"assign_to": ["test@example.com", "test1@example.com"],
			"doctype": "Ticket",
			"name": ticket.name,
		}
	)
