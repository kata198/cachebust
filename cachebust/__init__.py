'''
    Copyright (c) 2015 Timothy Savannah under LGPLv2. You should have received a copy of this as LICENSE with this distribution.

    "cachebust" provides a means to ensure that browsers always fetch updated files when they change, by adding a param 'cachebust=$md5sum' to all the asset tags. When the file changes, the md5sum is updated, and the browser makes a new request.
'''

# vim: ts=4 sw=4 expandtab :

import os
import sys
import re
import urllib
try:
	import urlparse
	urlencode = urllib.urlencode
except ImportError:
	import urllib.parse as urlparse
	from urllib.parse import urlencode

from hashlib import md5


__all__ = ('cachebustUrl', 'updateTag', 'updateDocument', 'cachebustHtml', 'cachebustFile')

__version__ = '1.0.1'
__version_tuple__ = (1, 0, 1)


def cachebustUrl(urlValue, assetRoot=None, quiet=False):
    '''
        cachebustUrl - Uses a parameter, "cachebust" to ensure browser caching always picks up new value. Returns a cachebusted url from a given asset url

        @param urlValue <str> - Url value of asset (like value of "src" attribute)
        @param assetRoot <None/str> - Filesystem path which should be treated as representing "/" for urls. If None is provided, current directory will be used.
        @param quiet <bool> - True to silence warnings to stderr when cachebusting cannot be applied.

        @return - The same url on error, otherwise the url with "cachebust" param set to md5sum of file (so changes cause a refresh)

    '''
    if not assetRoot:
        assetRoot = os.getcwd()

    parseResults = urlparse.urlparse(urlValue)
    url = parseResults.path
    queryStr = urlencode([x for x in urlparse.parse_qsl(parseResults.query) if x[0] != 'cachebust'])
    

    path = ''
    try:
        if url.startswith('/'):
            path = assetRoot + url
        else:
            path = os.getcwd() + '/' + url
        if not os.path.isfile(path):
            if quiet is False:
                sys.stderr.write('Could not find file for %s, tried %s, not modifying cachebust.\n' %(urlValue, path))
            return urlValue
        with open(path, 'rb') as f:
            contents = f.read()
        cachebust = md5(contents).hexdigest()
    except Exception as e:
        if quiet is False:
            sys.stderr.write('Exception trying to generate md5sum of file %s: %s\n' %(path, str(e)))
        return urlValue

    if queryStr:
        queryStr += '&'
    queryStr += 'cachebust=' + cachebust

    finalUrl = []
    if parseResults.scheme:
        finalUrl.append(parseResults.scheme)
        finalUrl.append('://')
    if parseResults.netloc:
        finalUrl.append(parseResults.netloc)

    finalUrl.append(url)
    finalUrl.append('?')
    finalUrl.append(queryStr)

    return ''.join(finalUrl)
    

def updateTag(tagObj, fieldName=None, assetRoot=None, quiet=False):
    '''
        updateTag - Updates an AdvancedHTMLParser.AdvancedTag object to cachebust its source.


        @param tagObj <AdvancedHTMLParser.AdvancedTag> - A tag which will be cachebusted
        @param fieldName <str/None> - The attribute to cachebust. If "None" is provided, based on the tag name one will be picked ("src" for img,script and "rel" for link)
        @param assetRoot <None/str> - Filesystem path which should be treated as representing "/" for urls. If None is provided, current directory will be used.
        @param quiet <bool> - True to silence warnings to stderr when cachebusting cannot be applied.

        @return - True on success (tag was updated), False on failure (tag was not updated)

    '''
    if not assetRoot:
        assetRoot = os.getcwd()

    if fieldName is None:
        tagName = tagObj.tagName
        if tagName in {'img', 'script'}:
            fieldName = 'src'
        elif tagName in {'link', }:
            fieldName = 'rel'
        else:
            if quiet is False:
                sys.stderr.write("No provided fieldName and couldn't determine for tag: %s\n" %(tagName,))
            return False

    attrValue = tagObj.getAttribute(fieldName)
    if not attrValue:
        return False
    
    newValue = cachebustUrl(attrValue, assetRoot, quiet)

    if newValue != attrValue:
        tagObj.setAttribute(fieldName, newValue)
        return True

    return False

def updateDocument(parserObj, assetRoot=None, quiet=False):
    '''
        updateDocument - Updates an AdvancedHTMLParser.AdvancedHTMLParser object to cachebust all items

        @param parserObj <AdvancedHTMLParser.AdvancedHTMLParser> - The object which represents the document to cachebust
        @param assetRoot <None/str> - Filesystem path which should be treated as representing "/" for urls. If None is provided, current directory will be used.
        @param quiet <bool> - True to silence warnings to stderr when cachebusting cannot be applied.

        @return - None
    '''
    for tagType in ('img', 'script'):
        for element in parserObj.getElementsByTagName(tagType):
            updateTag(element, 'src', assetRoot, quiet)

    for tagType in ('link',):
        for element in parserObj.getElementsByTagName(tagType):
            updateTag(element, 'rel', assetRoot, quiet)


def cachebustHtml(html, encoding='utf-8', assetRoot=None, quiet=False):
    '''
        cachebustHtml - cachebusts provided html string and returns the cachebusted html.

        @param html <str> - String of html
        @param encoding <str> - Encoding to use (default, utf-8)
        @param assetRoot <None/str> - Filesystem path which should be treated as representing "/" for urls. If None is provided, current directory will be used.
        @param quiet <bool> - True to silence warnings to stderr when cachebusting cannot be applied.

        @return - cachebusted HTML
    '''
    import AdvancedHTMLParser

    parser = AdvancedHTMLParser.AdvancedHTMLParser(encoding=encoding)
    parser.parseStr(html)
    updateDocument(parser, assetRoot, quiet)

    return parser.getHTML()

def cachebustFile(filename, encoding='utf-8', assetRoot=None, quiet=False):
    '''
        cachebustFile - cachebusts provided file and returns the cachebusted html.

        @param html <str> - String of html
        @param encoding <str> - Encoding to use (default, utf-8)
        @param assetRoot <None/str> - Filesystem path which should be treated as representing "/" for urls. If None is provided, current directory will be used.
        @param quiet <bool> - True to silence warnings to stderr when cachebusting cannot be applied.

        @return - cachebusted HTML
    '''
    import AdvancedHTMLParser

    parser = AdvancedHTMLParser.AdvancedHTMLParser(encoding=encoding)
    parser.parseFile(filename)
    updateDocument(parser, assetRoot, quiet)

    return parser.getHTML()

