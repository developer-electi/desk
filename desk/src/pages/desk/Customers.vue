<template>
	<div class="flex flex-col h-full px-4">
		<ListManager
			ref="fdCustomerList"
			:options="{
				cache: ['FD Customer', 'Desk'],
				doctype: 'FD Customer',
				urlQueryFilters: true,
				saveFiltersLocally: true,
				fields: [
					'customer_name',
					'domain',
					'contact_count',
					'ticket_count',
				],
				limit: 20,
			}"
		>
			<template #body>
				<ListViewer
					:options="{
						name: 'Customer',
						listTitle: 'All Customers',
						base: '12',
						filterBox: true,
						presetFilters: true,
						fields: {
							customer_name: {
								label: 'Name',
								width: '4',
							},
							contact_count: {
								label: 'Contacts',
								width: '2',
							},
							ticket_count: {
								label: 'Tickets',
								width: '2',
							},
						},
					}"
					class="text-base h-[100vh] pt-4"
					@add-item="
						() => {
							showNewCustomerDialog = true
						}
					"
				>
					<template #field-customer_name="{ row }">
						<router-link
							:to="{ path: `/frappedesk/customers/${row.name}` }"
						>
							{{ `${row.customer_name}` }}
						</router-link>
					</template>
				</ListViewer>
			</template>
		</ListManager>
		<NewCustomerDialog
			v-model="showNewCustomerDialog"
			@close="
				() => {
					showNewCustomerDialog = false
				}
			"
		/>
	</div>
</template>
<script>
import ListManager from "@/components/global/ListManager.vue"
import ListViewer from "@/components/global/ListViewer.vue"
import NewCustomerDialog from "@/components/desk/global/NewCustomerDialog.vue"
export default {
	name: "Customers",
	components: {
		ListManager,
		ListViewer,
		NewCustomerDialog,
	},
	data() {
		return {
			showNewCustomerDialog: false,
		}
	},
}
</script>
