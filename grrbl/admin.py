from grrbl.models import IP,Vote,Email
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.contrib.auth.models import User,Group
from models import UserProfile,GroupProfile

class IPAdmin(admin.ModelAdmin):
    search_fields = ['ipaddress','dateadded']
    date_hierarchy = 'dateadded'
    list_display = ('ipaddress', 'dateadded', 'b_or_w', 'votes' )

admin.site.register(IP, IPAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'vote' )
    filter = ('content_type',)

admin.site.register(Vote,VoteAdmin)


class EmailAdmin(admin.ModelAdmin):
    search_fields = ['emailaddress','dateadded']
    date_hierarchy = 'dateadded'
    list_display = ('emailaddress', 'dateadded', 'b_or_w', 'votes' )

admin.site.register(Email, EmailAdmin)


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline,]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active' )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class GroupProfileInline(admin.TabularInline):
    model = GroupProfile
    fk_name = 'group'
    max_num = 1


class CustomGroupAdmin(GroupAdmin):
    inlines = [GroupProfileInline,]
    list_display = ('name', 'id' , 'get_weight')

    def get_weight(self, object):
        return object.groupprofile.weight
    get_weight.short_description = 'Weight'

    def save_formset(self, request, form, formset, change):
        # We override save_formset, in order to ensure that we always create an
        # associated group profile, even when the user doesn't change the
        # default values of the TabularInline form.
        saved = formset.save()
        if not change and not saved:
            # We are creating a new group and no associated profiles were created
            profile = GroupProfile.objects.create(group=form.instance)
            profile.save()
    
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
