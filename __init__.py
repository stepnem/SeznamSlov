# coding: utf-8
###
# Copyleft (ↄ) 2009, Štěpán Němec
# All lefts reserved.
###

"""
This plugin provides an interface to the online dictionary at
<http://slovnik.seznam.cz>.
"""

import supybot
import supybot.world as world

__version__ = "1.0"

try:
    __author__ = supybot.authors.stepnem
except AttributeError:
    __author__ = supybot.Author('Štěpán Němec', 'stepnem',
                                'stepnem AT gmail DOT com')
    
__contributors__ = {}

__url__ = 'git://github.com/stepnem/SeznamSlov.git'

import config
import plugin
reload(plugin) # In case we're being reloaded.

Class = plugin.Class
configure = config.configure


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
