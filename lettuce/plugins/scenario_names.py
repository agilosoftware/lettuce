# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERsteps.pyCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from lettuce import core
from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.plugins.reporter import Reporter

class NameReporter(Reporter):
    def print_scenario_ran(self, scenario):
        self.wrt('%s ... ' % scenario.name)
        if scenario.passed:
            self.wrt("OK")
        elif scenario.failed:
            reason = self.scenarios_and_its_fails[scenario]
            if isinstance(reason.exception, AssertionError):
                self.wrt("FAILED")
            else:
                self.wrt("ERROR")
        self.wrt("\n")

    def print_stacktrace(self, step):
        if not step.display:
            return

        if step.failed:
            print_spaced = lambda x: self.wrt("%s%s\n" % (" " * step.indentation, x))

            for line in step.why.traceback.splitlines():
                print_spaced(line)

reporter = NameReporter()

after.each_scenario(reporter.print_scenario_ran)
after.each_step(reporter.store_failed_step)
after.each_step(reporter.print_stacktrace)
after.all(reporter.print_end)


def print_no_features_found(where):
    where = core.fs.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    reporter.wrt('Oops!\n')
    reporter.wrt('could not find features at %s\n' % where)
