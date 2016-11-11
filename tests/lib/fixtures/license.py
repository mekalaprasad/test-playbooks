import os.path
import sys
import logging
import pytest
import towerkit.tower.license


log = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def tower_license_path(request, tower_config_dir):
    return os.path.join(tower_config_dir, 'license')


@pytest.fixture(scope='class')
def backup_license(request, ansible_runner, tower_license_path):
    '''Backup any existing license files. The files will be restored upon teardown.
    '''
    log.debug("calling fixture backup_license")
    ansible_runner.shell('mv {0} {0}.bak'.format(tower_license_path, removes=tower_license_path))

    def teardown():
        log.debug("calling teardown backup_license")
        ansible_runner.shell('mv {0}.bak {0}'.format(tower_license_path, removes=tower_license_path + '.bak'))
    request.addfinalizer(teardown)


@pytest.fixture(scope='class')
def install_license_1000(request, ansible_runner, tower_license_path):
    '''Install a license where instance_count=1000
    '''

    log.debug("calling fixture install_license_1000")
    fname = towerkit.tower.license.generate_license_file(instance_count=1000, days=365)
    ansible_runner.copy(src=fname, dest=tower_license_path, owner='awx', group='awx', mode='0600')

    def teardown():
        log.debug("calling teardown install_license_1000")
        ansible_runner.file(path=tower_license_path, state='absent')
    request.addfinalizer(teardown)


@pytest.fixture(scope='class')
def install_license_10000(request, ansible_runner, tower_license_path):
    '''Install a license where instance_count=10000
    '''

    log.debug("calling fixture install_license_10000")
    fname = towerkit.tower.license.generate_license_file(instance_count=10000, days=365)
    ansible_runner.copy(src=fname, dest=tower_license_path, owner='awx', group='awx', mode='0600')

    def teardown():
        log.debug("calling teardown install_license_10000")
        ansible_runner.file(path=tower_license_path, state='absent')
    request.addfinalizer(teardown)


@pytest.fixture(scope='class')
def install_license_unlimited(request, ansible_runner, tower_license_path):
    '''Install a license where instance_count=unlimited
    '''

    log.debug("calling fixture install_license_unlimited")
    fname = towerkit.tower.license.generate_license_file(instance_count=sys.maxint, days=365)
    ansible_runner.copy(src=fname, dest=tower_license_path, owner='awx', group='awx', mode='0600')

    def teardown():
        log.debug("calling teardown install_license_unlimited")
        ansible_runner.file(path=tower_license_path, state='absent')
    request.addfinalizer(teardown)
