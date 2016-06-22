================
alibabaa
================


What is alibabaa module for?
------------------------------------

This module is a non-official API tool to request search results from https://s.1688.com


Usage Example
-------------

.. code:: python
    
    >>> from alibabaa.alibabaa import Alibabaa

    # jquery style of to call methods
    >>> print Alibabaa().addKeyword("自行车").addKeywords(["发电机","手机屏"]).setPage(1).setMode("view").alimama()
    item 山地车碟刹山地自行车/自行车批发酒类促销PF980大头
    price 215.0
    company 天津市盛强自行车有限公司
    location unknown
    ......
    
    # traditional way to call methods
    >>> ali = Alibabaa()
    >>> ali.addKeyword("电动车")
    >>> ali.setPage(2)
    >>> ali.addKeywords(["发电机","手机屏"])
    >>> ali.setMode("save")
    >>> ali.alimama()
    >>> ali.setMode("view")
    >>> ali.alimama()
    item 山地车碟刹山地自行车/自行车批发酒类促销PF980大头
    price 215.0
    company 天津市盛强自行车有限公司
    location unknown
    ......
    >>> ali.setMode("api")
    True
    >>> data = ali.alimama()
    >>> print data[0][0].items()
    [('item', '\xe5\x8e\x82\xe5\xae\xb6\xe6\x89\xb9\xe5\x8f\x91 8\xe5\xaf\xb8\xe8\x93\x9d\xe7\x89\x99\xe9\x9f\xb3\xe5\x93\x8d\xe6\x99\xba\xe8\x83\xbd\xe7\x94\xb5\xe5\x8a\xa8\xe5\x8f\x8c\xe8\xbd\xae\xe5\xb9\xb3\xe8\xa1\xa1\xe8\xbd\xa6 \xe4\xb8\xa4\xe8\xbd\xae\xe6\xb3\x8a\xe7\xa7\xbb\xe8\xbd\xa6 \xe7\x94\xb5\xe5\x8a\xa8\xe6\x89\xad\xe6\x89\xad\xe8\xbd\xa6'), ('price', 299.0), ('company', '\xe6\xb7\xb1\xe5\x9c\xb3\xe5\xb8\x82\xe6\x98\x93\xe5\x9f\x8e\xe7\xa7\x91\xe6\x8a\x80\xe5\x8f\x91\xe5\xb1\x95\xe6\x9c\x89\xe9\x99\x90\xe5\x85\xac\xe5\x8f\xb8'), ('location', '\xe6\xb7\xb1\xe5\x9c\xb3\xe5\xb8\x82\xe5\xae\x9d\xe5\xae\x89\xe5\x8c\xba')]

Installation
------------

Use pip:

.. code:: shell

    $ pip install -U alibabaa


Documentation
-------------

Documentation is available at https://github.com/brunobell/alibabaa/blob/master/README.rst


Contribution
============

Use github to submit bug,fix or wish request: https://github.com/brunobell/alibabaa/issues
