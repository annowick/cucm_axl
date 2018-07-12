# cucm_axl

<h3>Prerequisites</h3>
<ul>
<li>Download axl toolkit from CUCM and unzip it into "axltoolkit" subdirectory. To change it, modify WSDL_RELPATH constant</li>
<li>Default version is 10.5. To change it, modify VER constant</li>
</ul>

<h3>Keyword Arguments</h3>
<ul>
<li><b>server</b>: IP or FQDN. Default: prompt</li>
<li><b>username</b>: AXL user configured on CUCM. Default: prompt</li>
<li><b>password</b>: AXL password. Default: prompt</li>
<li><b>readonly</b>: if set, will only allow 'select' sql queries, as well as 'list' or 'get' axl queries. Default: True</li>
</ul>
    
<h3>Examples</h3>
<b>a = AxlConn(**CUCMRO)</b><br>
CUCM address: <i>CUCM IP Address or FQDN</i><br>
AXL Username: <i>axluser</i><br>
Password for axluser: <i>axlpassword</i><br>

<b>a.sql_query("SELECT name FROM device WHERE name LIKE 'SEP%'")</b><br>

[{'name': SEP000011112222}, {'name': SEP000011112223}]


<b>a.axl_query("listDeviceProfile(searchCriteria={'name': '%'}, returnedTags={'name': ''})")</b><br>

(<HTTPStatus.OK: 200>, (reply){<br>
    return =<br>
       (return){<br>
          deviceProfile[] =<br>
             (LDeviceProfile){<br>
                _uuid = "{2159B23D-D2C2-D7D8-8B4D-5970B6A5D0BB}"<br>
                name = "1001"<br>
             },<br>
             (LDeviceProfile){<br>
                _uuid = "{3A0B93C3-6556-B3F1-4E57-0E6115189550}"<br>
                name = "1002"<br>
             },<br>
       }<br>
  })<br>
