# tower-qa

Welcome to the tower-qa repository.  Here you'll find playbooks, scripts, documentation and tests used for validating Ansible Tower.

## Repository structure

* `playbooks/` - ansible playbooks used for deploying tower
* `scripts/` - helper scripts
* `tests/` - tower-qa automated tests
* `docs/` - tower-qa documentation

## Build Triggers

The build, test and deployment process for Ansible Tower is managed by [Jenkins](http://50.116.42.103).  The following test events are used to trigger [Tower jenkins jobs](http://50.116.42.103/view/Tower/).

### git-push

Any time code changes are pushed into the [ansible-tower.git repository](https://github.com/ansible/ansible-tower), jenkins will trigger the [Test_Tower_Unittest](http://50.116.42.103/view/Tower/job/Test_Tower_Unittest/) job.

### cron

On a daily interval, jenkins will trigger the development build process with the job [Nightly_Build - Tower](http://50.116.42.103/view/Tower/job/Nightly%20Build%20-%20Tower/).

### manual

All jenkins jobs can be triggered manually.  Jenkins will prompt for any required build parameters.

## Build Workflow

There are two primary workflows through the Tower build process:
 1. Release (`OFFICIAL=yes`) - builds `.rpm`, `.deb` and `.tgz` files for official product releases
 1. Nightly (`OFFICIAL=no`) - builds `.rpm`, `.deb` and `.tgz` files for internal purposes, and initiates tests

### Release

The official build workflow is triggered by the job [Release_Tower](http://50.116.42.103/view/Tower/job/Release_Tower/).  All jobs in this workflow use the parameter `OFFICIAL=yes`.  Build artifacts (e.g. `.rpm`, `.deb` and `.tgz` files) are intended for production-use.

* [Release_Tower](http://50.116.42.103/view/Tower/job/Release_Tower/)
  * [Build_Tower_TAR](http://50.116.42.103/view/Tower/job/Build_Tower_TAR/)
  * [Build_Tower_RPM](http://50.116.42.103/view/Tower/job/Build_Tower_RPM/)
  * [Build_Tower_DEB](http://50.116.42.103/view/Tower/job/Build_Tower_DEB/)

### Nightly

The nightly build workflow is triggered on a ... wait for it ... nightly basis by jenkins.  All jobs use the parameter `OFFICIAL=no`.  Build artifacts (e.g. `.rpm`, `.deb` and `.tgz` files) are intended for internal testing purposes only.

* [Nightly_Build - Tower](http://50.116.42.103/view/Tower/job/Nightly%20Build%20-%20Tower/)
  * [Build_Tower_TAR](http://50.116.42.103/view/Tower/job/Build_Tower_TAR/)
  * [Build_Tower_RPM](http://50.116.42.103/view/Tower/job/Build_Tower_RPM/)
    * [Test_Tower_Install](http://50.116.42.103/view/Tower/job/Test_Tower_Install) (for rpm-based distros only)
      * [Test_Tower_Integration](http://50.116.42.103/view/Tower/job/Test_Tower_Integration) (for rpm-based distros only)
  * [Build_Tower_DEB](http://50.116.42.103/view/Tower/job/Build_Tower_DEB/)
    * [Test_Tower_Install](http://50.116.42.103/view/Tower/job/Test_Tower_Install) (for ubuntu only)
      * [Test_Tower_Integration](http://50.116.42.103/view/Tower/job/Test_Tower_Integration) (for ubuntu distros only)

