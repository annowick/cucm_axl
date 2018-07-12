# cucm_axl

<h3>Prerequisites</h3>
- download axl toolkit from CUCM and unzip it into "axltoolkit" subdirectory. To change it, modify WSDL_RELPATH constant<br>
- default version is 10.5, to change it modify VER constant<br>

<h3>Keyword Arguments</h3>
- server - IP or FQDN. Default: prompt<br>
- username - AXL user configured on CUCM. Default: prompt<br>
- password - AXL password. Default: prompt<br>
- readonly - if set, will only allow 'select' sql queries, as well as 'list' or 'get' axl queries. Default: True<br>

<h3>Examples</h3>
<b>a = AxlConn(**CUCMRO)</b><br>
CUCM address: <CUCM IP Address or FQDN><br>
AXL Username: <axluser><br>
Password for axluser: <axlpassword><br>

<b>a.sql_query("select name from device where name like 'SEP%'")</b><br>

[{'name': SEP000011112222}, {'name': SEP000011112223}]


<b>a.axl_query("listDeviceProfile(searchCriteria={'name': '%'}, returnedTags={'name': ''})")</b><br>

(<HTTPStatus.OK: 200>, (reply){<br>
    return =<br>
       (return){<br>
          deviceProfile[] =
             (LDeviceProfile){
                _uuid = "{2159B23D-D2C2-D7D8-8B4D-5970B6A5D0BB}"
                name = "1001001"
             },
             (LDeviceProfile){
                _uuid = "{3A0B93C3-6556-B3F1-4E57-0E6115189550}"
                name = "1001002"
             },
       }
  })
