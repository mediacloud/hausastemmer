Hausa language stemmer
======================

.. image:: https://travis-ci.org/pypt/mediacloud-hausastemmer.svg?branch=master
  :target: https://travis-ci.org/pypt/mediacloud-hausastemmer

.. image:: https://coveralls.io/repos/github/pypt/mediacloud-hausastemmer/badge.svg?branch=develop
  :target: https://coveralls.io/github/pypt/mediacloud-hausastemmer?branch=develop

Hausa language stemmer reference implementation by Bimba et al., 2015.

Uses Hausa affix-rules and reference lookup to stem words in Hausa language: `Bimba, A., Idris, N., Khamis, N. and
Noor, N.F.M. (2015) ‘Stemming Hausa text: Using affix-stripping rules and reference look-up’, Language Resources and
Evaluation, 50(3), pp. 687–703. doi: 10.1007/s10579-015-9311-x. <https://bit.ly/hausa-stemming-bimba>`_

Based on modifications to the implementation of the Porter's Stemming Algorithm by Vivake Gupta (2001).

Copyright (C) 2013, `Bimba Andrew Thomas <mailto:andrewbimba@gmail.com>`_, Department of Artificial Intelligence,
FSKTM Universiti Malaya, Kuala Lumpur, Malaysia.

Adapted as a Python module by `Linas Valiukas <mailto:lvaliukas@cyber.law.harvard.edu>`_.

Usage
-----

.. code-block:: python

   import hausastemmer

   print(hausastemmer.stem('Nijeriya kasa ce a nahiyar Afirka ta yamma.'.split()));


License
-------

Copyright (C) 2013, Bimba Andrew Thomas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details <http://www.gnu.org/licenses/>.
