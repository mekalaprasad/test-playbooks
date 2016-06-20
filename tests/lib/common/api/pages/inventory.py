import json
from common.api.pages import Base, Base_List, Unified_Job_Page, Unified_Job_Template_Page, Credential_Page, json_setter, json_getter


class Inventory_Page(Base):
    # FIXME - it would be nice for base_url to always return self.json.url.
    base_url = '/api/v1/inventories/{id}/'
    name = property(json_getter('name'), json_setter('name'))
    type = property(json_getter('type'), json_setter('type'))
    description = property(json_getter('description'), json_setter('description'))
    variables = property(json_getter('variables'), json_setter('variables'))
    organization = property(json_getter('organization'), json_setter('organization'))

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related'], \
            "No such related attribute '%s'" % attr
        if attr == 'hosts':
            cls = Hosts_Page
        elif attr in ['created_by', 'modified_by']:
            from users import User_Page
            cls = User_Page
        elif attr == 'groups':
            cls = Groups_Page
        elif attr == 'inventory_sources':
            cls = Inventory_Sources_Page
        elif attr == 'root_groups':
            cls = Groups_Page
        elif attr == 'script':
            cls = Base
        elif attr == 'ad_hoc_commands':
            from ad_hoc_commands import Ad_Hoc_Commands_Page
            cls = Ad_Hoc_Commands_Page
        elif attr == 'organization':
            from organizations import Organization_Page
            cls = Organization_Page
        elif attr == 'access_list':
            from access_list import Access_List_Page
            cls = Access_List_Page
        elif attr == 'object_roles':
            from roles import Roles_Page
            cls = Roles_Page
        elif attr in ['job_templates', 'scan_job_templates']:
            from job_templates import Job_Templates_Page
            cls = Job_Templates_Page
        elif attr in ['variable_data', 'tree']:
            cls = Base
        elif attr == 'activity_stream':
            from activity_stream import Activity_Stream_Page
            cls = Activity_Stream_Page
        else:
            raise NotImplementedError("No related class found for '%s'" % attr)

        return cls(self.testsetup, base_url=self.json['related'][attr]).get(**kwargs)

    def print_ini(self):
        '''
        Print an ini version of the inventory
        '''
        output = list()
        inv_dict = self.get_related('script', hostvars=1).json

        for group in inv_dict.keys():
            if group == '_meta':
                continue

            # output host groups
            output.append('[%s]' % group)
            for host in inv_dict[group].get('hosts', []):
                # FIXME ... include hostvars
                output.append(host)
            output.append('')  # newline

            # output child groups
            if inv_dict[group].get('children', []):
                output.append('[%s:children]' % group)
                for child in inv_dict[group].get('children', []):
                    output.append(child)
                output.append('')  # newline

            # output group vars
            if inv_dict[group].get('vars', {}).items():
                output.append('[%s:vars]' % group)
                for k, v in inv_dict[group].get('vars', {}).items():
                    output.append('%s=%s' % (k, v))
                output.append('')  # newline

        print '\n'.join(output)


class Inventories_Page(Inventory_Page, Base_List):
    base_url = '/api/v1/inventories/'


class Group_Page(Base):
    # FIXME - it would be nice for base_url to always return self.json.url.
    base_url = '/api/v1/groups/{id}/'
    name = property(json_getter('name'), json_setter('name'))
    description = property(json_getter('description'), json_setter('description'))
    inventory = property(json_getter('inventory'), json_setter('inventory'))
    variables = property(json_getter('variables'), json_setter('variables'))
    total_hosts = property(json_getter('total_hosts'), json_setter('total_hosts'))

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related']
        if attr == 'hosts':
            related = Hosts_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'all_hosts':
            related = Hosts_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'inventory':
            related = Inventory_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'inventory_source':
            related = Inventory_Source_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'children':
            related = Groups_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'variable_data':
            related = Base(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'ad_hoc_commands':
            from ad_hoc_commands import Ad_Hoc_Commands_Page
            related = Ad_Hoc_Commands_Page(self.testsetup, base_url=self.json['related'][attr])
        else:
            raise NotImplementedError
        return related.get(**kwargs)

    @property
    def is_root_group(self):
        '''
        Returns whether the current group is a top-level root group in the inventory
        '''
        return self.get_related('inventory').get_related('root_groups', id=self.id).count == 1

    def get_parents(self):
        '''
        Inspects the API and returns all groups that include the current group
        as a child.
        '''
        parents = list()
        for candidate in self.get_related('inventory').get_related('groups').results:
            if candidate.get_related('children', id=self.id).count > 0:
                parents.append(candidate.id)
        return parents


class Groups_Page(Group_Page, Base_List):
    base_url = '/api/v1/groups/'


class Host_Page(Base):
    # FIXME - it would be nice for base_url to always return self.json.url.
    base_url = '/api/v1/hosts/{id}/'
    name = property(json_getter('name'), json_setter('name'))
    description = property(json_getter('description'), json_setter('description'))
    inventory = property(json_getter('inventory'), json_setter('inventory'))
    variables = property(json_getter('variables'), json_setter('variables'))

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related']
        if attr == 'variable_data':
            related = Base(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'inventory':
            related = Inventory_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'groups':
            related = Groups_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'ad_hoc_commands':
            from ad_hoc_commands import Ad_Hoc_Commands_Page
            related = Ad_Hoc_Commands_Page(self.testsetup, base_url=self.json['related'][attr])
        elif attr == 'fact_versions':
            related = Fact_Versions_Page(self.testsetup, base_url=self.json['related'][attr])
        else:
            raise NotImplementedError
        return related.get(**kwargs)


class Fact_Version_Page(Base):
    base_url = '/api/v1/hosts/{id}/fact_versions/'
    module = property(json_getter('module'), json_setter('module'))
    timestamp = property(json_getter('timestamp'), json_setter('timestamp'))

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related']
        if attr == 'fact_view':
            related = Fact_View_Page(self.testsetup, base_url=self.json['related'][attr])
        else:
            raise NotImplementedError
        return related.get(**kwargs)


class Fact_Versions_Page(Fact_Version_Page, Base_List):
    base_url = '/api/v1/hosts/{id}/fact_versions/'

    @property
    def count(self):
        return len(self.results)


class Fact_View_Page(Base):
    base_url = '/api/v1/hosts/{id}/fact_view/'
    timestamp = property(json_getter('timestamp'), json_setter('timestamp'))
    host = property(json_getter('host'), json_setter('host'))
    module = property(json_getter('module'), json_setter('module'))
    facts = property(json_getter('facts'), json_setter('facts'))


class Hosts_Page(Host_Page, Base_List):
    base_url = '/api/v1/hosts/'


class Inventory_Source_Page(Unified_Job_Template_Page):
    # FIXME - it would be nice for base_url to always return self.json.url.
    base_url = '/api/v1/inventory_sources/{id}/'

    source = property(json_getter('source'), json_setter('source'))
    source_vars = property(json_getter('source_vars'), json_setter('source_vars'))
    source_script = property(json_getter('source_script'), json_setter('source_script'))
    update_cache_timeout = property(json_getter('update_cache_timeout'), json_setter('update_cache_timeout'))
    update_on_launch = property(json_getter('update_on_launch'), json_setter('update_on_launch'))
    inventory = property(json_getter('inventory'), json_setter('inventory'))
    group_by = property(json_getter('group_by'), json_setter('group_by'))
    source_regions = property(json_getter('source_regions'), json_setter('source_regions'))
    instance_filters = property(json_getter('instance_filters'), json_setter('instance_filters'))

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related'], \
            "No such related attribute '%s'" % attr
        cls = None
        if attr in ('last_update', 'current_update'):
            cls = Inventory_Update_Page
        elif attr == 'credential':
            cls = Credential_Page
        elif attr == 'groups':
            cls = Inventory_Source_Groups_Page
        elif attr == 'inventory_updates':
            cls = Inventory_Updates_Page
        elif attr == 'inventory':
            cls = Inventory_Page
        elif attr == 'update':
            cls = Inventory_Source_Update_Page
        elif attr == 'schedules':
            from schedules import Schedules_Page
            cls = Schedules_Page
        elif attr == 'notification_templates_any':
            from notification_templates import Notification_Templates_Page
            cls = Notification_Templates_Page
        elif attr == 'notification_templates_error':
            from notification_templates import Notification_Templates_Page
            cls = Notification_Templates_Page
        elif attr == 'notification_templates_success':
            from notification_templates import Notification_Templates_Page
            cls = Notification_Templates_Page

        if cls is None:
            raise NotImplementedError("No related class found for '%s'" % attr)

        return cls(self.testsetup, base_url=self.json['related'][attr]).get(**kwargs)

    def update(self):
        '''
        Update the inventory_source using related->update endpoint
        '''
        # get related->launch
        update_pg = self.get_related('update')

        # assert can_update == True
        assert update_pg.can_update, \
            "The specified inventory_source (id:%s) is not able to update (can_update:%s)" % \
            (self.id, update_pg.can_update)

        # start the inventory_update
        result = update_pg.post()

        # assert JSON response
        assert 'inventory_update' in result.json, \
            "Unexpected JSON response when starting an inventory_update.\n%s" % \
            json.dumps(result.json, indent=2)

        # locate and return the inventory_update
        jobs_pg = self.get_related('inventory_updates', id=result.json['inventory_update'])
        assert jobs_pg.count == 1, \
            "An inventory_update started (id:%s) but job not found in response at %s/inventory_updates/" % \
            (result.json['inventory_update'], self.url)
        return jobs_pg.results[0]

    @property
    def is_successful(self):
        '''An inventory_source is considered successful when:
            0) source != ""
            1) super().is_successful
        '''
        return self.source != "" and super(Inventory_Source_Page, self).is_successful


class Inventory_Sources_Page(Inventory_Source_Page, Base_List):
    base_url = '/api/v1/inventory_sources/'


class Inventory_Source_Groups_Page(Group_Page, Base_List):
    base_url = '/api/v1/inventory_sources/{id}/groups'


class Inventory_Source_Update_Page(Base):
    base_url = '/api/v1/inventory_sources/{id}/launch'
    can_update = property(json_getter('can_update'), json_setter('can_update'))


class Inventory_Update_Page(Unified_Job_Page):
    base_url = '/api/v1/inventory_updates/{id}/'

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related'], \
            "No such related attribute '%s'" % attr
        if attr == 'cancel':
            cls = Inventory_Update_Cancel_Page
        elif attr == 'inventory_source':
            cls = Inventory_Source_Page
        else:
            raise NotImplementedError("No related class found for '%s'" % attr)

        return cls(self.testsetup, base_url=self.json['related'][attr]).get(**kwargs)


class Inventory_Updates_Page(Inventory_Update_Page, Base_List):
    base_url = '/api/v1/inventory_sources/{inventory_source}/inventory_updates/'


class Inventory_Update_Cancel_Page(Base):
    base_url = '/api/v1/inventory_updates/{id}/cancel'
    can_cancel = property(json_getter('can_cancel'), json_setter('can_cancel'))


class Inventory_Script_Page(Base):
    base_url = '/api/v1/inventory_scripts/{id}/'
    name = property(json_getter('name'), json_setter('name'))
    description = property(json_getter('description'), json_setter('description'))
    script = property(json_getter('script'), json_setter('script'))

    def get_related(self, attr, **kwargs):
        assert attr in self.json['related'], \
            "No such related attribute '%s'" % attr
        if attr in ['created_by', 'modified_by']:
            from users import User_Page
            cls = User_Page
        elif attr == 'object_roles':
            from roles import Roles_Page
            cls = Roles_Page
        elif attr == 'organization':
            from organizations import Organizations_Page
            cls = Organizations_Page
        else:
            raise NotImplementedError("No related class found for '%s'" % attr)

        return cls(self.testsetup, base_url=self.json['related'][attr]).get(**kwargs)


class Inventory_Scripts_Page(Inventory_Script_Page, Base_List):
    base_url = '/api/v1/inventory_scripts/'
