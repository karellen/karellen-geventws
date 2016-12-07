#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pybuilder.core import use_plugin, init, Project, Author

use_plugin("pypi:karellen_pyb_plugin", ">=0.0.1.dev")
use_plugin("copy_resources")
use_plugin("filter_resources")

name = "karellen-geventws"
version = "1.0.0"

url = "https://github.com/karellen/karellen-geventws"
description = "Please visit %s for more information!" % url
summary = "Karellen Testing Library"

authors = [Author("Jeffrey Gelens", "jeffrey@noppo.pro"), Author("Karellen, Inc", "supervisor@karellen.co")]
license = "Apache License, Version 2.0"

default_task = ["install_dependencies", "analyze", "sphinx_generate_documentation", "publish"]


@init
def set_properties(project: Project):
    # Dependencies
    project.depends_on("gevent")

    project.build_depends_on("wsaccel")
    project.build_depends_on("ujson")
    project.build_depends_on("websocket-client", "~=0.0")
    # project.build_depends_on("autobahntestsuite", "~=0.7")

    # Cram Configuration
    project.set_property("cram_fail_if_no_tests", False)

    # Disable flake8
    project.set_property("flake8_break_build", False)

    # Integration Tests Coverage is disabled since there are no integration tests
    project.set_property("unittest_coverage_threshold_warn", 0)
    project.set_property("unittest_coverage_branch_threshold_warn", 0)
    project.set_property("unittest_coverage_branch_partial_threshold_warn", 0)
    project.set_property("unittest_coverage_allow_non_imported_modules", True)
    project.set_property("integrationtest_coverage_threshold_warn", 0)
    project.set_property("integrationtest_coverage_branch_threshold_warn", 0)
    project.set_property("integrationtest_coverage_branch_partial_threshold_warn", 0)
    project.set_property("integrationtest_coverage_allow_non_imported_modules", True)

    project.set_property("pybuilder_header_plugin_break_build", False)

    project.set_property("copy_resources_target", "$dir_dist")
    project.get_property("copy_resources_glob").append("LICENSE")
    project.get_property("filter_resources_glob").append("**/geventwebsocket/__init__.py")

    # Distutils
    project.set_property("distutils_classifiers", project.get_property("distutils_classifiers") + [
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        ])

    project.set_property("pdoc_module_name", "geventwebsocket")
