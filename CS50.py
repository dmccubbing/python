"""
CS50 Library
https://manual.cs50.net/Library

@author Colton Ogden <cogden@cs50.net>
@link https://manual.cs50.net/Library
@package CS50
@version 0.1

Copyright (c) 2013, David J. Malan <malan@harvard.edu>
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

import openid
import openid.extensions.ax
import openid.extensions.sreg
from openid.store import filestore
from openid.consumer import consumer
import util

# CS50
class CS50:
    """
    Returns URL to which user can be directed for
    authentication via CS50 ID.
    
    @param  directory   Directory used to store state
    @param  trust_root  URL that CS50 ID should prompt user to trust
    @param  return_to   URL to which CS50 ID should return user
    @param  session     Session variable passed in (i.e., through Django)
    @param  fields      Simple Registration fields to request from CS50 ID
    @param  attributes  Attribute Exchange attributes to request from CS50 ID
    
    @return URL for CS50 ID
    """
    @staticmethod
    def getLoginUrl(directory, trust_root, return_to, session, fields = ['email', 'fullname'], attributes = []):
        # prepare request
        store = util.getOpenIDStore(directory, 'c_')
        c = consumer.Consumer(session, store)
        auth_request = c.begin('https://id.cs50.net')
        
        # simple registration fields
        if (fields and len(fields) > 0)
            sreg_request = sreg.SRegRequest(optional=fields, required=['key'])
            auth_request.addExtension(sreg_request)
            
        # attribute exchange fields
        if len(attributes) > 0:
            ax_request = ax.FetchRequest()
            for attribute in attributes:
                ax_request.add(ax.AttrInfo(attribute, count=1, required=False))
            auth_request.addExtension(ax_request)
        
        # generate url for direction
        return auth_request.redirect_url(trust_root, return_to)
        
    """
    If user was authenticated (at URL returned by getLoginUrl),
    returns associative array that WILL contain user's Harvard email
    address (mail) and that MAY contain user's name (displayName).
    
    @param  directory   Path to directory used to store state
    @param  return_to   URL to which CS50 ID returned user
    @param  request     A Django Request object we can grab parameters from  
         
    @return user as associative array, or false if failed
    """
    @staticmethod
    def getUser(directory, return_to, request):
        user = {}
        
        # clean parameters from the request URL to ensure Janrain's lib works
        request_args = util.normalDict(request.GET)
        if request.method == 'POST':
            request_args.update(util.normalDict(request.POST))

        if request_args:
            c = getConsumer(request)
            
        # Get a response object indicating the result of the OpenID
        # protocol.
        return_to = util.getViewURL(request, getUser)
        response = c.complete(request_args, return_to)
        
        if response.status == consumer.SUCCESS: 
            user['identity'] = response.identity_url
            
            # simple registration fields
            sreg_response = sreg.SRegResponse.fromSuccessResponse(response)
                if (sreg_response):
                    user = dict(user.items() + sreg_response.items())
            
            # get attribute exchange attributes
            ax_response = ax.FetchResponse.fromSuccessResponse(response)
                if (ax_response):
                    user = dict(user.items() + sreg_response.items())
            
            return user
        else:
            return False