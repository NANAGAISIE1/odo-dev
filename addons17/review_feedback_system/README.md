# Review and Feedback System for Odoo

A comprehensive review and feedback management system for Odoo v17 that enables businesses to collect, manage, and display customer reviews seamlessly.

## Features

### 🌟 Core Features
- **User-friendly review submission forms** - Easy-to-use web forms for customers
- **Automatic data capture and storage** - All reviews stored in Odoo database
- **Website review display** - Beautiful display of approved reviews
- **Advanced admin dashboard** - Comprehensive management interface
- **Real-time notification system** - Email notifications for new reviews
- **Analytics and reporting** - Detailed insights and trends
- **Responsive design** - Works on all devices
- **Security and compliance** - Built-in security measures

### 📊 Review Management
- **Review moderation workflow** - Approve, reject, or archive reviews
- **Bulk actions** - Process multiple reviews at once
- **Business responses** - Respond to customer reviews
- **Rating system** - 5-star rating with detailed feedback
- **Categories** - Organize reviews by categories
- **Attachments** - Support for images and files

### 🎯 Website Integration
- **Public review pages** - `/reviews` - Browse all reviews
- **Product-specific reviews** - Reviews linked to products
- **Review submission** - `/review/submit` - Customer submission form
- **Search and filtering** - Find reviews by category, rating, etc.
- **SEO-friendly URLs** - Optimized for search engines

### 👤 Customer Portal
- **My Reviews** - Customers can manage their reviews
- **Edit reviews** - Update reviews before approval
- **Review history** - Track review status and responses
- **Email notifications** - Updates on review status

### ⚙️ Admin Features
- **Settings configuration** - Customize review behavior
- **Moderation queue** - Manage pending reviews
- **Analytics dashboard** - Review trends and statistics
- **Notification system** - Email alerts for new reviews
- **Security groups** - Role-based access control

## Installation

1. **Download the module** to your Odoo addons directory:
   ```bash
   cp -r review_feedback_system /path/to/odoo/addons/
   ```

2. **Update the addons list** in Odoo:
   - Go to Apps
   - Click "Update Apps List"

3. **Install the module**:
   - Search for "Review and Feedback System"
   - Click "Install"

4. **Configure the module**:
   - Go to Reviews > Configuration > Settings
   - Configure your preferences

## Configuration

### Basic Setup

1. **Review Categories**:
   - Go to Reviews > Configuration > Categories
   - Create categories for your reviews (e.g., Products, Services, Support)

2. **Review Settings**:
   - Go to Reviews > Configuration > Settings
   - Configure moderation settings
   - Set up email notifications
   - Adjust display preferences

3. **Website Menu**:
   - The module automatically adds a "Reviews" menu to your website
   - Customize the menu position in Website > Configuration > Menus

### Advanced Configuration

#### Moderation Settings
- **Require Moderation**: All reviews need approval before publishing
- **Auto-approve Verified Purchases**: Automatically approve reviews from verified customers
- **Minimum Rating to Publish**: Set minimum rating for auto-publishing

#### Email Notifications
- **Notification Email**: Set email address for review notifications
- **Notify on New Reviews**: Enable/disable new review notifications
- **Customer Notifications**: Send updates to customers about their reviews

#### Display Settings
- **Reviews per Page**: Number of reviews to display per page
- **Show Reviewer Names**: Display customer names on reviews
- **Allow Voting**: Enable helpfulness voting on reviews

## Usage

### For Customers

#### Submitting a Review
1. Visit `/review/submit` on your website
2. Fill in the review form:
   - Review title
   - Rating (1-5 stars)
   - Detailed review content
   - Product/service (optional)
   - Pros and cons (optional)
3. Submit the review
4. Wait for moderation (if enabled)

#### Managing Reviews
1. Log in to your account
2. Go to "My Account" > "Reviews"
3. View, edit, or track your reviews

### For Administrators

#### Review Moderation
1. Go to Reviews > Pending Moderation
2. Review submitted reviews
3. Approve, reject, or request changes
4. Add business responses if needed

#### Analytics and Reporting
1. Go to Reviews > Analytics
2. View review trends and statistics
3. Export data for further analysis

#### Bulk Actions
1. Select multiple reviews in list view
2. Use Action menu for bulk operations:
   - Bulk approve/reject
   - Bulk publish/unpublish
   - Bulk archive/delete

## API and Integration

### Website Routes
- `GET /reviews` - List all published reviews
- `GET /review/<int:review_id>` - View specific review
- `GET /review/submit` - Review submission form
- `POST /review/submit` - Process review submission
- `GET /reviews/product/<int:product_id>` - Product-specific reviews

### JSON API Endpoints
- `POST /review/vote` - Vote on review helpfulness
- `GET /reviews/api/stats` - Get review statistics

### Models and Fields

#### review.feedback
Main review model with fields:
- `title` - Review title
- `content` - Review content
- `rating` - Rating (1-5)
- `state` - Review status (draft, submitted, approved, rejected, archived)
- `partner_id` - Customer (if registered)
- `product_id` - Related product
- `category_id` - Review category
- `website_published` - Published on website
- `verified_purchase` - Verified purchase flag

#### review.category
Review categories with fields:
- `name` - Category name
- `description` - Category description
- `website_published` - Published on website
- `website_sequence` - Display order

## Security

### User Groups
- **Review User** - Basic review access
- **Review Moderator** - Can moderate reviews
- **Review Manager** - Full review management access

### Security Features
- **Input validation** - All user inputs are validated
- **XSS protection** - Content is properly escaped
- **CSRF protection** - Forms include CSRF tokens
- **Access control** - Role-based permissions
- **Data privacy** - Customer data protection

## Customization

### Extending the Module

#### Adding Custom Fields
```python
class ReviewFeedback(models.Model):
    _inherit = 'review.feedback'
    
    custom_field = fields.Char('Custom Field')
```

#### Custom Email Templates
Modify templates in `data/review_email_templates.xml`

#### Custom Website Templates
Override templates in `views/website_review_templates.xml`

### Styling and Appearance

#### Frontend Styling
Customize CSS in `static/src/css/review_frontend.css`

#### Backend Styling
Customize CSS in `static/src/css/review_backend.css`

## Troubleshooting

### Common Issues

#### Reviews Not Appearing on Website
1. Check if reviews are approved
2. Verify `website_published` is True
3. Check category publication settings

#### Email Notifications Not Working
1. Verify email settings in Odoo
2. Check notification email configuration
3. Ensure email templates are active

#### Permission Errors
1. Check user groups and permissions
2. Verify security rules
3. Check record access rights

### Debug Mode
Enable debug mode to see detailed error messages:
```
?debug=1
```

## Performance Optimization

### Database Optimization
- Regular database cleanup
- Archive old reviews
- Optimize database indexes

### Caching
- Enable website caching
- Use CDN for static assets
- Optimize image sizes

## Support and Maintenance

### Regular Maintenance
- Monitor review moderation queue
- Clean up old attachments
- Update email templates
- Review analytics data

### Backup and Recovery
- Regular database backups
- Export review data
- Document configuration settings

## Contributing

We welcome contributions to improve the module:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This module is licensed under LGPL-3. See LICENSE file for details.

## Changelog

### Version 17.0.1.0.0
- Initial release
- Complete review management system
- Website integration
- Customer portal
- Analytics dashboard
- Email notifications
- Bulk actions
- Multi-language support

## Credits

Developed by Nana Gaisie for Odoo v17.

For support and questions, please contact: [Your Support Email]

---

**Happy Reviewing! 🌟**
