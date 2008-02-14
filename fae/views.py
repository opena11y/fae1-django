from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import datetime
from labels import labels
from forms import BasicEvalForm, DepthEvalForm, MultiEvalForm

def index(request, multi=False):
    """
    Serve the appropriate Run FAE page based on the user's login status.
    """
    # Get latest report parameters if they exist
    report_info = request.session.get('report', {})

    # Get appropriate title
    if multi:
        title = labels['multi']
    elif evaluate:
        title = 'Processing...'
    else:
        title = labels['index']

    # Set up initial context values
    context = {
        'page_type': 'index',
        'is_logged_in': request.user.is_authenticated(),
        'site': labels['site'],
        'title': title,
        }
    if report_info: context['report'] = report_info

    if request.user.is_authenticated():
        if multi:
            return index_multi(request, context)
        else:
            return index_user(request, context)
    else:
        return index_guest(request, context)

#----------------------------------------------------------------
def index_user(request, ctx):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = DepthEvalForm(request.POST)
        if form.is_valid():
            response.set_cookie('url', form.clean_data['url'])
            response.set_cookie('title', form.clean_data['title'])
            response.set_cookie('depth', form.clean_data['depth'])
            response.set_cookie('span', form.clean_data['span'])
    else:
        init_values = {}
        if 'url' in request.COOKIES:
            init_values['url'] = request.COOKIES['url']
        if 'title' in request.COOKIES:
            init_values['title'] = request.COOKIES['title']
        if 'depth' in request.COOKIES:
            init_values['depth'] = request.COOKIES['depth']
        if 'span' in request.COOKIES:
            init_values['span'] = request.COOKIES['span']
        form = DepthEvalForm(initial=init_values)

    # Add the appropriate form to the context
    ctx['form'] = form

    # Return response
    t = get_template('index_user.html')
    html = t.render(Context(ctx))
    response.write(html)
    return response

#----------------------------------------------------------------
def index_multi(request, ctx):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = MultiEvalForm(request.POST)
        if form.is_valid():
            response.set_cookie('urls', form.clean_data['urls'])
            response.set_cookie('titles', form.clean_data['titles'])
    else:
        init_values = {}
        if 'urls' in request.COOKIES:
            init_values['urls'] = request.COOKIES['urls']
        if 'titles' in request.COOKIES:
            init_values['titles'] = request.COOKIES['titles']
        form = MultiEvalForm(initial=init_values)

    # Add the appropriate form to the context
    ctx['form'] = form

    # Return response
    t = get_template('index_multi.html')
    html = t.render(Context(ctx))
    response.write(html)
    return response

#----------------------------------------------------------------
def index_guest(request, ctx):

    if request.method == 'POST':
        form = BasicEvalForm(request.POST)
        if form.is_valid(): pass
    else:
        form = BasicEvalForm()

    # Add the appropriate form to the context
    ctx['form'] = form

    # Return response
    t = get_template('index_guest.html')
    html = t.render(Context(ctx))
    return HttpResponse(html)

#----------------------------------------------------------------
@login_required
def archived_reports(request):
    """
    Display a list of the user's currently archived reports.
    """
    # Get latest report parameters if they exist
    report_info = request.session.get('report', {})

    # Set up context
    c = {
        'page_type': 'archive',
        'is_logged_in': request.user.is_authenticated(),
        'site': labels['site'],
        'title': labels['archive'],
        }
    if report_info: c['report'] = report_info

    # Return response
    t = get_template('archive.html')
    html = t.render(Context(c))
    return HttpResponse(html)

#----------------------------------------------------------------
def page_report(request, rptid, type, pageid=None, section=None):
    """
    Call the report function, but allow a different ordering of arguments.
    """
    return report(request, rptid, type, section, pageid)

#----------------------------------------------------------------
def report(request, rptid, type=None, section=None, pageid=None):
    """
    Serve the requested report, with defaults for type, section and pageid
    when none are specified.
    """
    # Set default values
    default_type = 'summary'
    default_section = 'nav'
    default_pageid = '1'

    # Get latest report parameters if they exist
    report_info = get_report_info(request, rptid)

    if type:
        report_info['type'] = type
    else:
        if not report_info.has_key('type'):
            report_info['type'] = default_type

    if section:
        report_info['section'] = section
    else:
        if not report_info.has_key('section'):
            report_info['section'] = default_section

    if pageid:
        report_info['pageid'] = pageid
    else:
        if not report_info.has_key('pageid'):
            report_info['pageid'] = default_pageid

    # Store report parameters in session variable
    request.session['report'] = report_info

    # Construct the document title
    title = labels['report'][report_info['type']]
    if report_info['type'] == 'page' and report_info['pgcount'] != '1':
        title += ' ' + report_info['pageid']

    if report_info['type'] == 'sitewide' or report_info['type'] == 'page':
        title += ': ' + labels['section'][report_info['section']]

    # Set up context
    c = {
        'page_type': 'report',
        'is_logged_in': request.user.is_authenticated(),
        'site': labels['site'],
        'title': title,
        'report': report_info
        }
    if report_info['type'] == 'sitewide' or report_info['type'] == 'page':
        c['display_sections'] = True

    # Return response
    t = get_template('report.html')
    html = t.render(Context(c))
    return HttpResponse(html)

#----------------------------------------------------------------
def about(request, content_id='overview'):
    # Get latest report parameters if they exist
    report_info = request.session.get('report', {})

    content = 'about/' + content_id + '.html'
    title = labels['about'] + ': ' + labels['subtitle'][content_id]

    # Set up  context values
    ctx = {
        'page_type': 'about',
        'is_logged_in': request.user.is_authenticated(),
        'site': labels['site'],
        'title': title,
        'subtitle': labels['subtitle'],
        'content': content,
        }
    if report_info: ctx['report'] = report_info

    # Return response
    t = get_template('about/about.html')
    html = t.render(Context(ctx))
    return HttpResponse(html)

#----------------------------------------------------------------
def get_report_info(request, rptid):
    """
    Given a report ID:
        IF rptid matches existing report_info
            return existing report_info
        ELSE
            return a new dictionary with new rptid

    Later, when a new report is requested, this function
    will need to get the report metadata from the database.
    """
    # Get latest report parameters if they exist
    report_info = request.session.get('report', {})

    if report_info.has_key('rptid') and report_info['rptid'] == rptid:
        return report_info
    else:
        return { 'rptid': rptid, 'pgcount': '12' }

#----------------------------------------------------------------
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
