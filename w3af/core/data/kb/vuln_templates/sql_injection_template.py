"""
sql_injection_template.py

Copyright 2013 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
from w3af.core.data.kb.vuln_templates.base_template import BaseTemplate
from w3af.core.data.fuzzer.mutants.querystring_mutant import QSMutant
from w3af.core.data.fuzzer.mutants.postdata_mutant import PostDataMutant
from w3af.core.data.request.fuzzable_request import FuzzableRequest


class SQLiTemplate(BaseTemplate):
    """
    Vulnerability template for SQL injection vulnerability.
    """
    def __init__(self):
        super(SQLiTemplate, self).__init__()
        
        self.name = self.get_vulnerability_name()
        
    def create_vuln(self):
        v = self.create_base_vuln()

        url = self.url

        if self.method.upper() == 'GET':
            url.querystring = self.data
            freq = FuzzableRequest(url, method=self.method)
            MutantKlass = QSMutant
        else:
            freq = FuzzableRequest(url, method=self.method, post_data=self.data)
            MutantKlass = PostDataMutant

        mutant = MutantKlass(freq)
        mutant.set_token((self.vulnerable_parameter, 0))
        mutant.set_dc(self.data)

        v.set_mutant(mutant)

        # Set the name of the vulnerability
        v.set_name(self.name)

        return v
        
    def get_kb_location(self):
        """
        :return: A tuple with the location where the vulnerability will be saved,
                 example return value would be: ('eval', 'eval')
        """
        return 'sqli', 'sqli'

    def get_vulnerability_name(self):
        """
        :return: A string containing the name of the vulnerability to be added
                 to the KB, example: 'SQL Injection'. This is just a descriptive
                 string which can contain any information, not used for any
                 strict matching of vulns before exploiting.
        """
        return '(Blind) SQL injection'

    def get_vulnerability_desc(self):
        return 'Blind and error based SQL injection vulnerability.'
