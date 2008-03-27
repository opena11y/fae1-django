from django.contrib.sites.models import Site

site_name = Site.objects.get_current().name

reports = {
    'summary': 'Summary Report',
    'sitewide': 'Sitewide Report',
    'page': 'Page Report',
    'menu': 'List of Pages',
    }

sections = {
    'nav': 'Navigation &amp; Orientation',
    'text': 'Text Equivalents',
    'auto': 'Scripting',
    'style': 'Styling',
    'std': 'HTML Standards',
    }

subtitles = {
    'overview': 'Overview',
    'rules': 'Rules Summary',
    'users': 'Intended Users',
    'future': 'Future Plans',
    'versions': 'Version History',
    'disclaimer': 'Disclaimer',
    }

labels = {
    'about': 'About FAE',
    'archive': 'Archived Reports',
    'index': 'Run FAE',
    'multi': 'Evaluate Multiple URLs',
    'next': 'Next',
    'prev': 'Previous',
    'profile': 'My Account',
    'report': reports,    
    'section': sections,
    'subtitle': subtitles,
    }
