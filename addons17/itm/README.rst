============================
IT Infrastructure Management
============================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:0a7bb63fc33573b9c41dbb6cea29083cb6c798db09aa2ac3d89fb0cb675fb47a
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-trevi--software%2Ftrevi--misc-lightgray.png?logo=github
    :target: https://github.com/trevi-software/trevi-misc/tree/18.0/itm
    :alt: trevi-software/trevi-misc

|badge1| |badge2| |badge3|

This module is used to record information about a site's IT
infrastructure. You can record information about equipment, software,
backups, networks and access credentials.

**Table of contents**

.. contents::
   :local:

Known issues / Roadmap
======================

- Manually set (or install) the python library 'cryptography' to version
  36.0.2. Because of Odoo Python requirements this module will **NOT**
  work with versions of cryptography greater than 36.0.2. It will also
  **NOT** work with the version in the Odoo requirements.txt file
  (currently 3.4.8).
- The password for encrypting and decrypting credentials is stored in
  Odoo as a system parameter. An attacker who has the
  'Administration/Settings' priviledge or has access to the Odoo
  database itself can easily decrypt a credential's password field.
- To Do: store the encryption password in Odoo's configuration file
  instead of a system parameter in the database

Changelog
=========

16.0.2.0.0 (2022-11-01)
-----------------------

- [IMP] Use the new Odoo javascript framework OWL

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/trevi-software/trevi-misc/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/trevi-software/trevi-misc/issues/new?body=module:%20itm%0Aversion:%2018.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* TREVI Software
* Leandro Ezequiel Baldi

Other credits
-------------

- Leandro Ezequiel Baldi <baldileandro@gmail.com>
- Altela Eleviansyah Pramardhika <altela.pramardhika@gmail.com>

Maintainers
-----------

This module is part of the `trevi-software/trevi-misc <https://github.com/trevi-software/trevi-misc/tree/18.0/itm>`_ project on GitHub.

You are welcome to contribute.
