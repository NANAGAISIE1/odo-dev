=================================
Management System - Nonconformity
=================================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:8f944a448f605b372b3a2c6468e3bc6a4f1eb3a8c62697964e2e1fa359b6cd1d
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fmanagement--system-lightgray.png?logo=github
    :target: https://github.com/OCA/management-system/tree/16.0/mgmtsystem_nonconformity
    :alt: OCA/management-system
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/management-system-16-0/management-system-16-0-mgmtsystem_nonconformity
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/management-system&target_branch=16.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module enables you to manage the nonconformities of your management systems:

* Quality (ISO 9001)
* Environment (ISO 14001)
* Information Security (ISO 27001)
* Health and Safety (ISO 45001)
* IT Services (ISO 20000)

**Table of contents**

.. contents::
   :local:

Configuration
=============

Users must be added to the appropriate groups within Odoo as follows:

* Creators: Settings > Users > Groups > Management System / User

To configure email notifications for certain stages go to:

* Management System > Configuration > Nonconformities > Stages
* Click on any stage and click the edit button.
* Click on the dropdown icon in the field Email Template, select your template and click Save.

Usage
=====

To use this module:

* Go to Management System > Nonconformities
* Click on Create to enter the following information:

* Partner : Customer, supplier or internal personnel
* Related to: Any reference pointing to the NC (order id, project id, task id, etc.)
* Responsible: Person responsible for the NC
* Manager : Person managing the department or owner of the procedure
* Filled in by: Originator of NC report
* Origins:  The source of the NC, how was it discover
* Procedures:  Against which procedure is the NC
* Description: Evidence, reference to the standards

* Click on Save and then on Analysis.

Go to the newly created NC and fill in the following
information in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the results of the investigation
* Severity: Select the severity among unfounded, minor and major
* Immediate action: Create or select an immediate action if appropriate

Click on the Save button and then on the "Action Plan" button in the top right corner.

In the Actions tab, select or create new actions by entering the following
items:

* Subject: What must be done - Return to Supplier, Use As Is, Scrap, Rework,
  Re-grade, Repair
* Deadline: Date by which the action must be completed
* Responsible: Person in charge for implementing the action
* Type: Immediate, corrective or preventive actions or improvement opportunity
* Description: Details of the action

When the action is created, a notification is sent to the person responsible
for the action.

Enter comments into the input field below the "Plan Review" section, those comments are required to reach the next stage.

To begin the work on the planned Actions change the stage of the NC to open by clicking on the "In Progress" button in the top right corner.

When all actions of the plan are done, their effectiveness must be evaluated
before closing the NC.

Known issues / Roadmap
======================

* The custom emails should be replaced by Mail Tracking features and Subtypes (like in Project Tasks and Project Issues)
* Automatically add responsible_user_id._uid, manager_user_id._uid, author_user_id._uid to chatter

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/management-system/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/management-system/issues/new?body=module:%20mgmtsystem_nonconformity%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Savoir-faire Linux

Contributors
~~~~~~~~~~~~

* Daniel Reis <dreis.pt@hotmail.com>
* Glen Dromgoole <gdromgoole@tier1engineering.com>
* Loic Lacroix <loic.lacroix@savoirfairelinux.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Gervais Naoussi <gervaisnaoussi@gmail.com>
* Eugen Don <eugen.don@don-systems.de>
* Jose Maria Alzaga <jose.alzaga@aselcis.com>
* `Tecnativa <https://www.tecnativa.com>`_:

  * Ernesto Tejeda

Trobz

* Dung Tran <dungtd@trobz.com>

Other credits
~~~~~~~~~~~~~

The development of this module has been financially supported by:

* Camptocamp

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/management-system <https://github.com/OCA/management-system/tree/16.0/mgmtsystem_nonconformity>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
