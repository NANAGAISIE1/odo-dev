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
