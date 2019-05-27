#!/usr/bin/env bash

set -euxo pipefail

# Script variables
#
SCENARIO=${SCENARIO:-standalone}
TOWER_VERSION=${TOWER_VERSION:-devel}
ANSIBLE_VERSION=${ANSIBLE_VERSION:-stable-2.7}
PLATFORM=${PLATFORM:-rhel-7.6-x86_64}
BUNDLE=${BUNDLE:-no}


# Env variables - need to be exported
#
export AWS_ACCESS_KEY=${AWS_ACCESS_KEY:-''}
export AWS_SECRET_KEY=${AWS_SECRET_KEY:-''}
export CLOUD_PROVIDER=${CLOUD_PROVIDER:-ec2}
export ANSIBLE_INSTALL_METHOD=${ANSIBLE_INSTALL_METHOD:-nightly}
export ANSIBLE_NIGHTLY_REPO=${ANSIBLE_NIGHTLY_REPO:-"http://nightlies.testing.ansible.com/ansible_nightlies_QcGXFZKv5VfQHi/"}
export ANSIBLE_TIMEOUT=${ANSIBLE_TIMEOUT:-30}
export DELETE_ON_START=${CLEAN_DEPLOYMENT_BEFORE_JOB_RUN:-yes}
export REAP_INSTANCES=${CLEAN_DEPLOYMENT_AFTER_JOB_RUN:-no}
export REAP_INSTANCES_ON_FAILURE=${CLEAN_DEPLOYMENT_ON_JOB_FAILURE:-yes}
export MINIMUM_VAR_SPACE=${MINIMUM_VAR_SPACE:-0}
export INSTANCE_NAME_PREFIX=${DEPLOYMENT_NAME:-'deployment-name'}
export VERBOSE=${VERBOSE:-no}
export ANSIBLE_NIGHTLY_BRANCH=${ANSIBLE_VERSION}
export AW_REPO_URL=${AW_REPO_URL:-"http://nightlies.testing.ansible.com/ansible-tower_nightlies_m8u16fz56qr6q7/devel"}
export AWX_SETUP_PATH=${AWX_SETUP_PATH:-"/setup/ansible-tower-setup-latest.tar.gz"}
export AWX_IPV6_DEPLOYMENT=${AWX_IPV6_DEPLOYMENT:-no}
export ANSIBLE_FORCE_COLOR=${ANSIBLE_FORCE_COLOR:-True}

ANSIBLE_NIGHTLY_REPO=${ANSIBLE_NIGHTLY_REPO}/${ANSIBLE_VERSION}

# -- Start
#
# shellcheck source=lib/common
source "$(dirname "${0}")"/lib/common

if [[ "${AWS_ACCESS_KEY}" == "" ]] || [[ "${AWS_SECRET_KEY}" == "" ]]; then
    >&2 echo "install.sh: Environment variables \$AWS_ACCESS_KEY and \$AWS_SECRET_KEY must be specified"
    exit 1
fi

setup_python3_env
pip install PyYAML argparse
setup_env_based_on_deployment_scenario "${SCENARIO}"
AWX_IPV6_DEPLOYMENT=$(retrieve_boolean_value "${AWX_IPV6_DEPLOYMENT}")
DELETE_ON_START=$(retrieve_boolean_value "${DELETE_ON_START}")
REAP_INSTANCES=$(retrieve_boolean_value "${REAP_INSTANCES}")
AW_REPO_URL=$(retrieve_aw_repo_url_based_on_version "${TOWER_VERSION}")
AWX_SETUP_PATH=$(retrieve_awx_setup_path_based_on_version_and_scenario "${TOWER_VERSION}" "${SCENARIO}" "${AW_REPO_URL}" "${BUNDLE}" "${PLATFORM}")
INSTANCE_NAME_PREFIX=$(generate_instance_name_prefix "${INSTANCE_NAME_PREFIX}" "${PLATFORM}" "${ANSIBLE_VERSION}" "${TOWER_VERSION}")

# FIXME(spredzy): Remove the below code when stable-2.8 is in epel 8
if [[ "${PLATFORM}" == "rhel-8.0-x86_64" ]]; then
    ANSIBLE_INSTALL_METHOD='pip'
fi

export AWX_VERBOSITY=$(retrieve_verbosity_string)
export AWX_PLAYBOOK="${PLAYBOOK}"
export AWX_INVENTORY="${INVENTORY}"

python scripts/cloud_vars_from_env.py \
    --cloud-provider "${CLOUD_PROVIDER}" --platform "${PLATFORM}" --image-vars "${IMAGE_VARS}" \
    > "${VARS_FILE}"
