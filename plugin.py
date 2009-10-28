# coding: utf-8
###
# Copyleft (ↄ) 2009, Štěpán Němec
# All rites reversed.
###
import codecs
import re
import urllib
from BeautifulSoup import BeautifulSoup

import supybot.conf as conf
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
        urllib.quote_plus(term.decode('utf-8', 'replace').encode('utf-8',
        'replace')), lang)
        soup = BeautifulSoup(utils.web.getUrl(url))
        words = soup.find('table', { 'id': 'words' })
        result = ''
        if words is not None:
            worditems = words.findAll('tr')
            for item in worditems:
                orig = codecs.encode(item.find('td', { 'class': 'word' }).find('a',
                    { 'href': _langRe }).string, 'utf-8', 'replace')
                trls = strlist(item.find('td', { 'class': 'translated' }).findAll(
                'a', { 'href': _langRe }))
                result += orig + ': ' + ', '.join(trls).encode('utf-8',
                        'replace') + ' --- '
        collocations = soup.find('div', { 'id': 'collocations' })
        if collocations is not None:
            colllist = collocations.find('dl')
            collorigs = colllist.findAll('dt')
            colltrls = colllist.findAll('dd')
            pairs = zip(collorigs, colltrls)
            for pair in pairs:
                orig = codecs.encode(pair[0].find('a',
                    { 'href': _langRe }).string, 'utf-8', 'replace')
                trl = codecs.encode(pair[1].find('a',
                    { 'href': _langRe }).string, 'utf-8', 'replace')
                result += orig + ': ' + trl + ' --- '

        if self.registryValue('showUrl', msg.args[0]):
            url = ' (<' + url + '>)'
        else:
            url = ''

        if result:
            result = result[:-5] + url
            irc.reply(result)
        else:
            irc.reply('Nothing found.' + url)


    seznamslov = wrap(seznamslov, ['something', additional(('matches', _isLang,
    'Invalid language specification.'), 'en_cz')])


Class = SeznamSlov


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
