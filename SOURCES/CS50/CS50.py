"""
CS50 Library
https://manual.cs50.net/Library

@author David J. Malan <malan@harvard.edu>
@link https://manual.cs50.net/Library
@package CS50
@version 3

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

# CS50
class CS50:
    """
    Returns URL to which user can be directed for
    authentication via CS50 ID.
    
    @param  trust_root  URL that CS50 ID should prompt user to trust
    @param  return_to   URL to which CS50 ID should return user
    @param  fields      Simple Registration fields to request from CS50 ID
    @param  attributes  Attribute Exchange attributes to request from CS50 ID
    
    @return URL for CS50 ID
    """
    @staticmethod
    def getLoginUrl(trust_root, return_to, fields = ('email', 'fullname'), *attributes):
        # ignore Janrain's use of deprecated functions
        