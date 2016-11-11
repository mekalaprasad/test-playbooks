import pytest
import logging

from tests.api import Base_Api_Test

from towerkit.exceptions import BadRequest, UnexpectedTowerState

log = logging.getLogger(__name__)

# Creating
# [ ] Node using (a) job template (b) project update (c) inventory update
# [ ] API browser's json template for node includes {success,failure,always} nodes. Can you post values for these?
# [ ] Able to use same node in multiple workflows
# [x] (-) Cannot use system job template
# [x] (-) Cannot use workflow job template
# [ ] (-) Cannot create node without specifying unified_job_template
# [ ] (-) Cannot use bad id for unified job template / workflow template
# [ ] (-) Configure node to trigger itself (e.g. on success)

# Deleting
# [ ] Deleting unified job template used by node
# [ ] Deleting workflow job template used by node


@pytest.mark.api
@pytest.mark.skip_selenium
@pytest.mark.destructive
class Test_Workflow_Nodes(Base_Api_Test):

    pytestmark = pytest.mark.usefixtures('authtoken', 'install_enterprise_license_unlimited')

    # Node cannot point to Workflow Job Template or System Job

    def test_workflow_job_template_node_cannot_contain_workflow_job_template(self, factories):
        wfjt = factories.workflow_job_template()
        with pytest.raises(BadRequest):
            wfjt.related.workflow_nodes.post(dict(unified_job_template=wfjt.id))

    def test_workflow_job_template_node_cannot_contain_system_job_template(self, factories, api_system_job_templates_pg):
        wfjt = factories.workflow_job_template()
        system_jts = api_system_job_templates_pg.get()
        assert system_jts.results, 'Failed to locate any system job templates'
        system_jt = system_jts.results.pop()
        with pytest.raises(BadRequest):
            wfjt.related.workflow_nodes.post(dict(unified_job_template=system_jt.id))
