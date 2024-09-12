from django import template
import re

register = template.Library()

@register.filter(name='linebreaksbr')
def linebreaksbr(value):
    """Convert newlines into <br> tags."""
    return value.replace('\n', '<br>')

@register.filter(name='spaces_and_bold')
def spaces_and_bold(value):
    """Convert multiple spaces to non-breaking spaces and *text* to bold."""
    # Replace multiple spaces with non-breaking spaces
    value = re.sub(r' {2,}', lambda m: '&nbsp;' * len(m.group(0)), value)
    
    # Convert *text* to <strong>text</strong>
    value = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', value)
    
    return value
