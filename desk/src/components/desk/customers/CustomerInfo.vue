<template>
	<div class="flex flex-col" v-if="customerDoc">
		<div class="customer-info flex-1">
			<div class="flex flex-row">
				<div class="info basis-1/2 m-[20px]">
					<div v-if="editingTitle">
						<div class="max-w-max mb-[10px]">
							<Input
								label="Customer Name"
								type="text"
								:value="customerDoc.customer_name"
								@change="
									(val) => {
										values.customerName = val
									}
								"
							/>
						</div>
						<div class="max-w-max">
							<Input
								label="Domain"
								type="text"
								:value="customerDoc.domain"
								@change="
									(val) => {
										values.domain = val
									}
								"
							/>
						</div>
					</div>
					<div v-else>
						<div class="flex">
							<div
								class="bg-[#90C5F4] w-14 h-14 justify-center flex items-center rounded-md font-medium text-white text-2xl"
							>
								<span>{{ acronym[0] }} {{ acronym[1] }}</span>
							</div>
							<div class="pl-4">
								<div class="font-medium text-2xl w-full">
									{{ values.customerName }}
								</div>

								<div class="font-light text-base">
									{{ values.domain }}
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="actions basis-1/2 m-[20px]">
					<div v-if="editingTitle" class="flex flex-row justify-end">
						<Button
							class="mr-1"
							appearance="primary"
							@click="
								() => {
									updateCustomer()
									editingTitle = false
								}
							"
							>Save</Button
						>
						<Button
							class="mr-1"
							appearance="secondary"
							@click="
								() => {
									editingTitle = false
									$resources.customer.reload()
								}
							"
							>Discard</Button
						>
					</div>
					<div v-else class="flex flex-row justify-end">
						<Button
							class="mr-1"
							appearance="secondary"
							icon-left="edit"
							@click="editingTitle = true"
							>Edit</Button
						>
						<!-- TO DO -->
						<!-- <Button
							class="mr-1"
							appearance="secondary"
							icon-left="trash"
							@click="deleteCustomer()"
							>Delete</Button
						> -->

						<Button
							class="mr-1"
							appearance="secondary"
							icon-left="plus"
							@click="
								() => {
									showNewContactDialog = true
								}
							"
							>Add Contact</Button
						>
						<Button
							class="mr-1"
							appearance="secondary"
							icon-left="plus"
							@click="
								() => {
									showNewTicketDialog = true
								}
							"
							>Add Ticket</Button
						>
					</div>
				</div>
			</div>
		</div>

		<div class="customer-table flex-1">
			<AccordionCustomer
				:isOpen="false"
				class="customer-accordion flex flex-col"
			>
				<template v-slot:title>
					<span class="font-medium text-lg flex-1"
						>Contacts ({{
							customerDoc.contact_count == null
								? "0"
								: customerDoc.contact_count
						}})
					</span>
				</template>

				<template v-slot:data>
					<div
						v-for="contact in contactDoc"
						class="flex font-normal text-sm py-2 items-center space-x-3 mx-5 py-2 px-4 border-b border-[#F4F5F6]-200"
					>
						<div class="w-[30%]">
							<router-link
								:to="`/frappedesk/contacts/${contact.name}`"
							>
								{{ contact.first_name }}
								{{
									contact.last_name == null
										? ""
										: contact.last_name
								}}
							</router-link>
						</div>
						<div class="w-[20%]">
							{{ contact.email_ids[0].email_id }}
						</div>
						<div class="w-[20%]">
							{{
								contact.phone_nos.length == 0
									? ""
									: contact.phone_nos[0].phone
							}}
						</div>
					</div>
				</template>
			</AccordionCustomer>
		</div>
		<div class="ticket-table flex-1 mt-5">
			<AccordionCustomer
				:isOpen="true"
				class="flex flex-col ticket-accordion"
			>
				<template v-slot:title>
					<span class="flex-1 font-medium text-lg"
						>Tickets ({{
							customerDoc.ticket_count == null
								? "0"
								: customerDoc.ticket_count
						}})
					</span>
				</template>

				<template v-slot:data>
					<div
						v-for="ticket in ticketDoc"
						class="flex w-[100%] pl-[22px] font-normal text-sm py-3 mx-5"
					>
						<div class="font-normal w-[10%] text-sm text-[#74808B]">
							{{ ticket.name }}
						</div>

						<div class="w-[40%] font-normal text-sm text-[#192734]">
							<router-link
								:to="`/frappedesk/tickets/${ticket.name}`"
							>
								{{ ticket.subject }}
							</router-link>
						</div>

						<div class="w-[10%] font-normal text-xs text-[#74808B]">
							<span :class="getStatusStyle(ticket.status)">{{
								ticket.status
							}}</span>
						</div>

						<div class="w-[10%] font-medium text-xs text-[#74808B]">
							<span :class="getTypeStyle(ticket.ticket_type)">
								{{ ticket.ticket_type }}
							</span>
						</div>

						<div class="w-[10%] font-normal text-xs text-[#74808B]">
							{{ ticket.priority }}
						</div>

						<div
							class="w-[10%] font-normal text-sm text-[#74808B] line-clamp-1"
						>
							{{ ticket.contact }}
						</div>
						<!-- <div class="w-[10%]" v-for="contact in contactDoc">
							<Avatar
								:label="user"
								class="w-[10%]"
								:imageURL="
									contact.name == ticket.contact
										? contact.image
										: ''
								"
								size="md"
							/>
						</div> -->
					</div>
				</template>
			</AccordionCustomer>
		</div>

		<NewContactDialog
			v-model="showNewContactDialog"
			:fdCustomer="customer"
			@contactCreated="
				() => {
					showNewContactDialog = false
					$router.go()
				}
			"
		/>
		<NewTicketDialog
			v-model="showNewTicketDialog"
			:fdCustomer="customer"
			@close="showNewTicketDialog = false"
			@ticket-created="
				() => {
					showNewTicketDialog = false
					$router.go()
				}
			"
		/>
	</div>
</template>

<script>
import { Dropdown, Avatar } from "frappe-ui"
import { Input } from "frappe-ui"
import AccordionCustomer from "@/components/global/AccordionCustomer.vue"
import CustomIcons from "@/components/desk/global/CustomIcons.vue"
import NewContactDialog from "@/components/desk/global/NewContactDialog.vue"
import NewTicketDialog from "@/components/desk/tickets/NewTicketDialog.vue"
export default {
	name: "CustomerInfo",
	props: ["customer"],
	components: {
		Dropdown,
		CustomIcons,
		NewContactDialog,
		NewTicketDialog,
		Input,
		Avatar,
		AccordionCustomer,
	},
	data() {
		return {
			editingTitle: false,
			showNewContactDialog: false,
			showNewTicketDialog: false,
			values: {
				customerName: "",
				domain: "",
			},
		}
	},
	computed: {
		acronym() {
			var str = this.customerDoc.customer_name
			var matches = str.match(/\b(\w)/g)
			var acronym = matches.join("")
			return acronym
		},
		ticketDoc() {
			return this.$resources.ticket.data
		},
		contactDoc() {
			return this.$resources.contact.data
		},
		customerDoc() {
			if (this.$resources.customer.doc) {
				this.values.customerName =
					this.$resources.customer.doc.customer_name
				this.values.domain = this.$resources.customer.doc.domain
			}
			return this.$resources.customer.doc || null
		},
	},
	resources: {
		customer() {
			return {
				type: "document",
				doctype: "FD Customer",
				name: this.customer,
				setValue: {
					onSuccess() {
						this.$toast({
							title: "Customer updated successfully.",
							appearance: "success",
							customIcon: "circle-check",
						})
					},
				},
			}
		},
		renameCustomerDoc() {
			return {
				method: "frappe.client.rename_doc",
				onSuccess: (res) => {
					this.$router.push({
						path: `/frappedesk/customers/${res}`,
					})
				},
			}
		},
		contact() {
			return {
				method: "frappedesk.api.fdCustomer.get_contact",
				params: {
					doctype: "Contact",
					link_name: this.customer,
					fields: ["*"],
				},
				auto: true,
			}
		},
		ticket() {
			return {
				method: "frappe.client.get_list",
				params: {
					doctype: "Ticket",
					fields: ["*"],
					filters: {
						customer: this.customer,
					},
				},
				auto: true,
			}
		},
	},
	methods: {
		validateInputs() {
			return !(this.values.customerName == "" || this.values.domain == "")
		},
		deleteCustomer() {
			return this.$resources.customer.delete.submit(null, {
				onSuccess: () => {
					this.$toast({
						title: "Customer deleted",
						customIcon: "circle-check",
						appearance: "success",
					})
					this.resetForm()
				},
				auto: true,
				onError: (e) => {
					this.$toast({
						title: "Cannot delete customer",
						text: e,
						customIcon: "circle-fail",
						appearance: "danger",
					})
				},
			})
		},
		updateCustomer() {
			if (this.validateInputs()) {
				this.$resources.customer.setValue.submit({
					domain: this.values.domain,
				})
				if (this.values.customerName !== this.customer) {
					this.$resources.renameCustomerDoc.submit({
						doctype: "FD Customer",
						old_name: this.customer,
						new_name: this.values.customerName,
					})
				}
			} else {
				this.$toast({
					title: "Please fill all the fields",
					customIcon: "circle-fail",
					appearance: "danger",
				})
			}
		},
		updateUrlSlug() {
			let doc = this.customer
			if (
				!this.$route.params.slug ||
				this.$route.params.slug !== doc.slug
			) {
				this.$router.replace({
					name: "Customer",
					params: {
						...this.$route.params,
						slug: doc.slug,
					},
					query: this.$route.query,
				})
			}
		},
		getStatusStyle(status) {
			const badge = {
				Open: "badge-danger",
				Resolved: "badge-replied",
				Closed: "badge-success",
				Replied: "badge-replied ",
			}[status]
			return badge
		},
		getTypeStyle(ticket_type) {
			const badge = {
				Question: "badge-question",
				Bug: "badge-bug",
				Incident: "badge-incident",
			}[ticket_type]
			return badge
		},
	},
}
</script>
