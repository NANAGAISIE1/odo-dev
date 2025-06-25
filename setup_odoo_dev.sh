#!/bin/bash
# setup_odoo_dev.sh - Setup script for Odoo development environment

echo "Setting up Odoo Development Environment..."

# Create project directory structure
mkdir -p odoo-dev/{addons17,addons18,config17,config18}
cd odoo-dev

# Create the docker-compose.yml file
cat > docker-compose.yml << 'EOF'
# (Copy the docker-compose.yml content from the first artifact)
EOF

# Create Odoo 17 configuration
cat > config17/odoo.conf << 'EOF'
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
admin_passwd = admin
logfile = /var/log/odoo/odoo.log
log_level = info
dev_mode = reload,qweb,werkzeug,xml
auto_reload = True
list_db = True
xmlrpc_port = 8069
longpolling_port = 8072
workers = 0
EOF

# Create Odoo 18 configuration
cat > config18/odoo.conf << 'EOF'
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
admin_passwd = admin
logfile = /var/log/odoo/odoo.log
log_level = info
dev_mode = reload,qweb,werkzeug,xml
auto_reload = True
list_db = True
xmlrpc_port = 8069
longpolling_port = 8072
workers = 0
EOF

# Create sample addon structure for both versions
create_sample_addon() {
    local version=$1
    local addon_dir="addons${version}/my_sample_addon"
    
    mkdir -p "$addon_dir"
    
    # __manifest__.py
    cat > "$addon_dir/__manifest__.py" << EOF
{
    'name': 'My Sample Addon',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Your Name',
    'category': 'Custom',
    'description': 'Sample addon for Odoo ${version}',
    'data': [
        'views/sample_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
EOF

    # __init__.py
    cat > "$addon_dir/__init__.py" << 'EOF'
from . import models
EOF

    # models/__init__.py
    mkdir -p "$addon_dir/models"
    cat > "$addon_dir/models/__init__.py" << 'EOF'
from . import sample_model
EOF

    # models/sample_model.py
    cat > "$addon_dir/models/sample_model.py" << 'EOF'
from odoo import models, fields, api

class SampleModel(models.Model):
    _name = 'sample.model'
    _description = 'Sample Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    
    @api.model
    def create(self, vals):
        return super(SampleModel, self).create(vals)
EOF

    # views/sample_view.xml
    mkdir -p "$addon_dir/views"
    cat > "$addon_dir/views/sample_view.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_sample_model_tree" model="ir.ui.view">
        <field name="name">sample.model.tree</field>
        <field name="model">sample.model</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="description"/>
            </tree>
        </field>
    </record>

    <record id="view_sample_model_form" model="ir.ui.view">
        <field name="name">sample.model.form</field>
        <field name="model">sample.model</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="description"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="action_sample_model" model="ir.actions.act_window">
        <field name="name">Sample Models</field>
        <field name="res_model">sample.model</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_sample_model" name="Sample Models" action="action_sample_model"/>
</odoo>
EOF
}

# Create sample addons for both versions
create_sample_addon 17
create_sample_addon 18

# Create management scripts
cat > start_odoo17.sh << 'EOF'
#!/bin/bash
echo "Starting Odoo 17 development environment..."
docker-compose --profile odoo17 up -d
echo "Odoo 17 is running on http://localhost:8069"
echo "Database: Use 'db' as hostname, 'odoo' as user and password"
EOF

cat > start_odoo18.sh << 'EOF'
#!/bin/bash
echo "Starting Odoo 18 development environment..."
docker-compose --profile odoo18 up -d
echo "Odoo 18 is running on http://localhost:8070"
echo "Database: Use 'db' as hostname, 'odoo' as user and password"
EOF

cat > stop_all.sh << 'EOF'
#!/bin/bash
echo "Stopping all Odoo services..."
docker-compose down
EOF

cat > start_tools.sh << 'EOF'
#!/bin/bash
echo "Starting development tools (pgAdmin)..."
docker-compose --profile tools up -d
echo "pgAdmin is running on http://localhost:5050"
echo "Login: admin@example.com / admin"
EOF

# Make scripts executable
chmod +x *.sh

echo ""
echo "✅ Odoo development environment setup complete!"
echo ""
echo "Directory structure:"
echo "odoo-dev/"
echo "├── docker-compose.yml"
echo "├── addons17/          # Your Odoo 17 custom addons"
echo "├── addons18/          # Your Odoo 18 custom addons"
echo "├── config17/          # Odoo 17 configuration"
echo "├── config18/          # Odoo 18 configuration"
echo "└── *.sh               # Management scripts"
echo ""
echo "Quick start commands:"
echo "• Start Odoo 17: ./start_odoo17.sh"
echo "• Start Odoo 18: ./start_odoo18.sh"
echo "• Start tools:   ./start_tools.sh"
echo "• Stop all:      ./stop_all.sh"
echo ""
echo "Access URLs:"
echo "• Odoo 17: http://localhost:8069"
echo "• Odoo 18: http://localhost:8070"
echo "• pgAdmin: http://localhost:5050"