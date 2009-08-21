# coding: utf-8
###
# Copyleft (ↄ) 2009, Štěpán Němec
# All lefts reserved.
###
import codecs
import re
from BeautifulSoup import BeautifulSoup

import supybot.utils as utils
from supybot.commands import *
import supybot.callbacks as callbacks


def strlist(brs):
    sL = []
    for i in brs:
        sL.append(i.string)
    return sL

_langRe = re.compile(r'\S+lang\S+')
class SeznamSlov(callbacks.Plugin):
    """Provides a `seznamslov' command interfacing [screen scraping :-(] to the
    Czech translating dictionary at <http://slovnik.seznam.cz>."""
    threaded = True
    _isLang = re.compile(r'^(?:en|de|fr|it|es)_cz$|^cz_(?:en|de|fr|it|es)$')
    def seznamslov(self, irc, msg, args, term, lang):
        """<term> [<lang>]

        Searches the online dictionary at slovnik.seznam.cz.

        Optional second argument in the format 'from_to' specifies the
        translation languages. Valid values are: en_cz (the default), de_cz,
        fr_cz, it_cz, es_cz and the reversed equivalents cz_en etc.
        """
        if not isinstance(lang, basestring):
            lang = lang.group(0)
        url = 'http://slovnik.seznam.cz/?q=%s&lang=%s' % (
        utils.web.urlquote(term.decode('utf-8', 'replace').encode('utf-8',
        'replace')), lang)
        soup = BeautifulSoup(utils.web.getUrl(url))
        words = soup.find('table', { 'id': 'words' })
        if words is None:
            irc.reply('Nothing found.')
            return
        worditems = words.findAll('tr')
        result = ''
        for item in worditems:
            orig = codecs.encode(item.find('td', { 'class': 'word' }).find('a',
                { 'href': _langRe }).string, 'utf-8', 'replace')
            trls = strlist(item.find('td', { 'class': 'translated' }).findAll(
            'a', { 'href': _langRe }))
            result += orig + ': ' + ', '.join(trls).encode('utf-8',
                    'replace') + ' --- '
        irc.reply(result[:-5])

    seznamslov = wrap(seznamslov, ['something', additional(('matches', _isLang,
    'Invalid language specification.'), 'en_cz')])


Class = SeznamSlov


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
