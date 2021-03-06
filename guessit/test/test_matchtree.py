#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function, unicode_literals

from guessit.test.guessittest import *

from guessit.transfo.guess_release_group import GuessReleaseGroup
from guessit.transfo.guess_properties import GuessProperties
from guessit.matchtree import BaseMatchTree

keywords = yaml.load("""

? Xvid PROPER
: videoCodec: Xvid
  other: PROPER

? PROPER-Xvid
: videoCodec: Xvid
  other: PROPER

""")


def guess_info(string, options=None):
    mtree = MatchTree(string)
    GuessReleaseGroup().process(mtree, options)
    GuessProperties().process(mtree, options)
    return mtree.matched()


class TestMatchTree(TestGuessit):
    def test_base_tree(self):
        t = BaseMatchTree('One Two Three(Three) Four')
        t.partition((3, 7, 20))
        leaves = t.leaves()

        self.assertEqual(leaves[0].span, (0, 3))

        self.assertEqual('One', leaves[0].value)
        self.assertEqual(' Two', leaves[1].value)
        self.assertEqual(' Three(Three)', leaves[2].value)
        self.assertEqual(' Four', leaves[3].value)

        leaves[2].partition((1, 6, 7, 12))
        three_leaves = leaves[2].leaves()

        self.assertEqual('Three', three_leaves[1].value)
        self.assertEqual('Three', three_leaves[3].value)

        leaves = t.leaves()

        self.assertEqual(len(leaves), 8)

        self.assertEqual(leaves[5], three_leaves[3])

        self.assertEqual(t.previous_leaf(leaves[5]), leaves[4])
        self.assertEqual(t.next_leaf(leaves[5]), leaves[6])

        self.assertEqual(t.next_leaves(leaves[5]), [leaves[6], leaves[7]])
        self.assertEqual(t.previous_leaves(leaves[5]), [leaves[4], leaves[3], leaves[2], leaves[1], leaves[0]])

        self.assertEqual(t.next_leaf(leaves[7]), None)
        self.assertEqual(t.previous_leaf(leaves[0]), None)

        self.assertEqual(t.next_leaves(leaves[7]), [])
        self.assertEqual(t.previous_leaves(leaves[0]), [])

    def test_match(self):
        self.checkFields(keywords, guess_info)


suite = allTests(TestMatchTree)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
