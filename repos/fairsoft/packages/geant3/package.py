# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Geant3(CMakePackage):
    """Simulation software using Monte Carlo methods to describe how particles pass through matter.."""

    homepage = "https://root.cern.ch/vmc"
    git      = "https://github.com/FairRootGroup/geant3.git"

    version('2-5-gcc8', tag='v2-5-gcc8')
    version('2-7_fairsoft', tag='v2-7_fairsoft')
    version('3-0_fairsoft', tag='v3-0_fairsoft')

    variant('build_type', default='Nightly',
            description='CMake build type',
            values=('Nightly'))

    depends_on('root')
    depends_on('vmc', when='@3-0_fairsoft:')

    patch('gcalor_stringsize.patch', level=0)
    patch('dict_fixes_30.patch', when='@v3-0_fairsoft')

    def cmake_args(self):
        spec = self.spec
        options = []
        options.append('-DCMAKE_INSTALL_LIBDIR:PATH=lib')
        options.append('-DROOT_DIR={0}'.format(
                self.spec['root'].prefix))

        return options

    def common_env_setup(self, env):
        env.set('G3SYS', join_path(self.prefix.share, 'geant3'))
        # So that root finds the shared library / rootmap
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)

    def setup_run_environment(self, env):
        self.common_env_setup(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.common_env_setup(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.common_env_setup(env)