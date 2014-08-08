"""
CS50 Library
https://manual.cs50.net/Library

@author Colton Ogden <cogden@cs50.net>
@author Dan Armendariz <danallan@cs.harvard.edu>
@link https://manual.cs50.net/Library
@package CS50
@version 0.2

Copyright (c) 2014, David J. Malan <malan@harvard.edu>
All rights reserved.

BSD 3-Clause License
http://www.opensource.org/licenses/BSD-3-Clause

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
    Neither the name of CS50 nor the names of its contributors may be used
    to endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from tempfile import gettempdir
import openid
from openid.extensions import ax, sreg
from openid.store.filestore import FileOpenIDStore
from openid.consumer import consumer

# CS50
class CS50:
    """
    Returns URL to which user can be directed for
    authentication via CS50 ID.

    @param  trust_root  URL that CS50 ID should prompt user to trust
    @param  return_to   URL to which CS50 ID should return user
    @param  session     Session variable passed in (i.e., through Django)
    @param  fields      Simple Registration fields to request from CS50 ID
    @param  attributes  Attribute Exchange attributes to request from CS50 ID

    @return URL for CS50 ID
    """
    @staticmethod
    def getLoginUrl(trust_root, return_to, session,
                    fields=['email','fullname'], attributes=None):
        # prepare request
        store = FileOpenIDStore(gettempdir())
        c = consumer.Consumer(session, store)
        auth_request = c.begin('https://id.cs50.net')

        # simple registration fields
        if fields:
            sreg_request = sreg.SRegRequest(optional=fields, required=None)
            auth_request.addExtension(sreg_request)

        # attribute exchange fields
        if attributes:
            ax_request = ax.FetchRequest()
            for attribute in attributes:
                ax_request.add(ax.AttrInfo(attribute, count=1, required=False))
            auth_request.addExtension(ax_request)

        # generate url for direction
        url = auth_request.redirectURL(trust_root, return_to)

        # return built url
        return url

    """
    If user was authenticated (at URL returned by getLoginUrl),
    returns associative array that WILL contain user's Harvard email
    address (mail) and that MAY contain user's name (displayName).

    @param  return_to   URL to which CS50 ID returned user
    @param  session     Session variable passed in (i.e., through Django)
    @param  get         A dictionary of GET parameters
    @param  post        A dictionary of POST parameters
    @param  attributes  Attribute Exchange attributes to request from CS50 ID

    @return user as associative array, or false if failed
    """
    @staticmethod
    def getUser(return_to, session, get=None, post=None, attributes=None):
        store = FileOpenIDStore(gettempdir())
        c = consumer.Consumer(session, store)

        # build a params objects containing query parameters
        params = get

        # in the case of POST
        if post:
            params.update(post)

        # Get a response object indicating the result of the OpenID
        # protocol.
        response = c.complete(params, return_to)

        user = None
        if response.status == consumer.SUCCESS:
            user = {'identity':response.identity_url}

            # simple registration fields
            sreg_response = sreg.SRegResponse.fromSuccessResponse(response)
            if sreg_response:
                user.update(dict(sreg_response.items()))

            # get attribute exchange attributes
            ax_response = ax.FetchResponse.fromSuccessResponse(response)
            if ax_response and attributes:
                for attribute in attributes:
                    user[attribute] = ax_response.get(attribute)

        return user

