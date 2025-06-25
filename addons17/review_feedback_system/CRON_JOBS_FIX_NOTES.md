# IMPORTANT: Cron Job Code Formatting Guidelines

## Issue Summary
The `review_cron_jobs.xml` file contains Python code within XML `<field name="code">` tags. This code must follow specific formatting rules to avoid IndentationError during module installation.

## Fixed Issues
1. **Improper line breaks in variable assignments** - Split assignments across multiple lines caused syntax errors
2. **Inconsistent indentation** - Python code within XML must use consistent 4-space indentation
3. **Missing proper spacing** - Code blocks need proper spacing for readability and parsing

## Correct Format Example
```xml
<field name="code">
# Comment explaining the code
variable_name = env['ir.config_parameter'].sudo().get_param('param_name', default_value)

if condition:
    # Indented code block
    result = some_operation()
    
    if nested_condition:
        nested_result = nested_operation()
        log('Message: %s' % result)
</field>
```

## Common Mistakes to Avoid
1. ❌ Split variable assignments across lines without proper continuation
2. ❌ Inconsistent indentation (mixing tabs and spaces)
3. ❌ Missing spaces around operators
4. ❌ Improper nesting of code blocks

## Validation Commands
```bash
# Check XML syntax
xmllint --noout data/review_cron_jobs.xml

# Check Python syntax (if extracted)
python3 -c "exec('''[CODE_HERE]''')"
```

## File Status: ✅ FIXED
All 4 cron jobs in `data/review_cron_jobs.xml` have been corrected and validated.

---
**Note**: Always test XML files after manual edits to prevent installation errors.
