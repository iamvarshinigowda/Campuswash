from datetime import timezone
from django.contrib import admin
from .models import LaundryOrders, laundry_Membership, laundry_Payments, ExtraService,Feedback

from .utils import send_status_update_email
# Admin for Laundry Orders
class LaundryOrderAdmin(admin.ModelAdmin):
    list_display = ('laundry_id', 'user', 'membership', 'clothes_count', 'check_in_date', 'check_in_time', 'status', 'check_out_date')
    list_filter = ('status', 'check_in_date', 'membership__membership_type')
    search_fields = ('user__username', 'status', 'membership__membership_id')
    
    # Custom actions to update order status
    actions = ['mark_as_completed', 'mark_as_in_progress']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Done')

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='In Progress')

    mark_as_completed.short_description = "Mark selected orders as Completed"
    mark_as_in_progress.short_description = "Mark selected orders as In Progress"
    def save_model(self, request, obj, form, change):
        if change:  # Check if the record is being updated
            previous_status = LaundryOrders.objects.get(laundry_id=obj.laundry_id).status
            if previous_status != 'Done' and obj.status == 'Done':  # Check for status change
                send_status_update_email(obj.user.email, obj.laundry_id)
        super().save_model(request, obj, form, change)




# Admin for Laundry Memberships
class LaundryMembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_id', 'user', 'membership_type', 'start_date', 'valid_until', 'payment')
    list_filter = ('membership_type', 'start_date')
    search_fields = ('user__username', 'membership_id')
    
    # Action to delete expired memberships
    actions = ['delete_expired_memberships']

    def delete_expired_memberships(self, request, queryset):
        for membership in queryset:
            if membership.valid_until < timezone.now().date():
                membership.delete()

    delete_expired_memberships.short_description = "Delete Expired Memberships"


# Admin for Laundry Payments
class LaundryPaymentsAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'payment_date', 'payment_type', 'payment_for')
    list_filter = ('payment_type', 'payment_for', 'payment_date')
    search_fields = ('user__username', 'payment_type', 'payment_for')


# Admin for Extra Service
class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'extraService', 'clothesCount', 'totalAmount', 'paymentType', 'date_requested')
    list_filter = ('extraService', 'paymentType', 'date_requested')
    search_fields = ('user__username', 'extraService', 'paymentType')
    
    # Calculate amount and update the totalAmount field automatically if needed
    def save_model(self, request, obj, form, change):
        obj.totalAmount = obj.calculate_amount()  # Auto-calculate amount based on clothes count and service type
        super().save_model(request, obj, form, change)
class LaundryFeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'user', 'feedback_type', 'rating', 'short_message')  # Customize columns
    list_filter = ('feedback_type', 'rating')  # Add filtering options
    search_fields = ('user__username', 'message', 'feedback_type')  # Add search functionality

    # Method to display a shortened version of the message
    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'

# Register the Feedback model and admin
admin.site.register(Feedback, LaundryFeedbackAdmin)






admin.site.register(LaundryOrders, LaundryOrderAdmin)
admin.site.register(laundry_Membership, LaundryMembershipAdmin)
admin.site.register(laundry_Payments, LaundryPaymentsAdmin)
admin.site.register(ExtraService, ExtraServiceAdmin)
