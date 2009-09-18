from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from datetime import datetime, date, timedelta

from project.settings import ACCT_TYPE_QUOTA, DEFAULT_QUOTA, ACCT_TYPE_BUFFER, DEFAULT_BUFFER
from project.settings import STATS_DAYS_OFFSET as DAYS_OFFSET
from labels import labels
from models import UserProfile, UserReport, GuestReport, UsageStats
from forms import BasicEvalForm, DepthEvalForm, MultiEvalForm
from forms import UserForm, ProfileForm, ManageReportForm
from evaluate import evaluate, multi_evaluate, evaluate_dhtml
from processors import get_report_content, get_pgrpteval_content
from uid import generate

#----------------------------------------------------------------
def index(request):
    """
    Serve the appropriate Run FAE form based on the user's login status.
    """
    if request.user.is_authenticated():
        return index_user(request)
    else:
        return index_guest(request)

#----------------------------------------------------------------
def index_user(request):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = DepthEvalForm(request.POST)
        if form.is_valid():
            # Check that formid matches session variable
            if not check_formid(request):
                raise Http404(labels['invalid_formid'])
            params = {
                'url': form.cleaned_data['url'],
                'title': form.cleaned_data['title'] or labels['untitled'],
                'depth': form.cleaned_data['depth'],
                'span': form.cleaned_data['span'],
                'dhtml': form.cleaned_data['dhtml'],
                'username': request.user.username
                }
            now = datetime.now()
            status, uid = evaluate(params, request.user.is_authenticated(), now)
            if status:
                report = UserReport(
                    id = uid,
                    user = request.user,
                    timestamp = now,
                    pgcount = status,
                    url = params['url'],
                    urlcount = 1,
                    depth = params['depth'],
                    title = params['title'],
                    dhtml = params['dhtml']
                    )
                report.save()
                response = HttpResponseRedirect('/report/%s/' % uid)

            # Set cookie values on whichever response object we have
            response.set_cookie('d_url', value=form.cleaned_data['url'], max_age=settings.MAX_AGE)
            response.set_cookie('d_title', value=form.cleaned_data['title'], max_age=settings.MAX_AGE)
            response.set_cookie('d_depth', value=form.cleaned_data['depth'], max_age=settings.MAX_AGE)
            response.set_cookie('d_span', value=form.cleaned_data['span'], max_age=settings.MAX_AGE)
            if form.cleaned_data['dhtml']:
                response.set_cookie('d_dhtml', value=form.cleaned_data['dhtml'], max_age=settings.MAX_AGE)
            else:
                response.delete_cookie('d_dhtml')

            if status:
                return response
            else:
                return message(request, response, 'Unable to create report!')

    else:
        init_values = {}
        if 'd_url' in request.COOKIES:
            init_values['url'] = request.COOKIES['d_url']
        if 'd_title' in request.COOKIES:
            init_values['title'] = request.COOKIES['d_title']
        if 'd_depth' in request.COOKIES:
            init_values['depth'] = request.COOKIES['d_depth']
        if 'd_span' in request.COOKIES:
            init_values['span'] = request.COOKIES['d_span']
        if 'd_dhtml' in request.COOKIES:
            init_values['dhtml'] = request.COOKIES['d_dhtml']
        form = DepthEvalForm(initial=init_values)

    context = {
        'page_type': 'index',
        'title': labels['index'],
        'formid': store_formid(request),
        'form': form,
        }

    # Return response
    t = get_template('index_user.html')
    html = t.render(RequestContext(request, context))
    response.write(html)
    return response

#----------------------------------------------------------------
def index_guest(request):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = BasicEvalForm(request.POST)
        if form.is_valid():
            # Check that formid matches session variable
            if not check_formid(request):
                raise Http404(labels['invalid_formid'])
            params = {
                'url': form.cleaned_data['url'],
                'title': labels['untitled'],
                'username': 'guest'
                }
            now = datetime.now()
            status, uid = evaluate(params, False, now)
            if status:
                report = GuestReport(
                    id = uid,
                    timestamp = now,
                    pgcount = status,
                    url = params['url']
                    )
                report.save()
                response = HttpResponseRedirect('/report/%s/' % uid)

            response.set_cookie('b_url', value=form.cleaned_data['url'], max_age=settings.MAX_AGE)

            if status:
                return response
            else:
                return message(request, response, 'Unable to create report!')
    else:
        init_values = {}
        if 'b_url' in request.COOKIES:
            init_values['url'] = request.COOKIES['b_url']
        form = BasicEvalForm(initial=init_values)

    context = {
        'page_type': 'index',
        'title': labels['index'],
        'formid': store_formid(request),
        'form': form,
        }

    # Return response
    t = get_template('index_guest.html')
    html = t.render(RequestContext(request, context))
    response.write(html)
    return response

#----------------------------------------------------------------
@login_required
def index_multi(request):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = MultiEvalForm(request.POST)
        if form.is_valid():
            # Check that formid matches session variable
            if not check_formid(request):
                raise Http404(labels['invalid_formid'])
            params = {
                'urls': form.cleaned_data['urls'],
                'title': form.cleaned_data['title'] or labels['untitled'],
                'dhtml': form.cleaned_data['dhtml'],
                'username': request.user.username
                }
            now = datetime.now()
            status, uid = multi_evaluate(params, request.user.is_authenticated(), now)

            if status:
                urls = form.cleaned_data['urls'].split()
                report = UserReport(
                    id = uid,
                    user = request.user,
                    timestamp = now,
                    pgcount = status,
                    url = urls[0],
                    urlcount = len(urls),
                    depth = 0,
                    title = params['title'],
                    dhtml = params['dhtml']
                    )
                report.save()
                response = HttpResponseRedirect('/report/%s/' % uid)

            response.set_cookie('m_urls', value=form.cleaned_data['urls'], max_age=settings.MAX_AGE)
            response.set_cookie('m_title', value=form.cleaned_data['title'], max_age=settings.MAX_AGE)
            if form.cleaned_data['dhtml']:
                response.set_cookie('m_dhtml', value=form.cleaned_data['dhtml'], max_age=settings.MAX_AGE)
            else:
                response.delete_cookie('m_dhtml')

            if status:
                return response
            else:
                return message(request, response, 'Unable to create report!')
    else:
        init_values = {}
        if 'm_urls' in request.COOKIES:
            init_values['urls'] = request.COOKIES['m_urls']
        if 'm_title' in request.COOKIES:
            init_values['title'] = request.COOKIES['m_title']
        if 'm_dhtml' in request.COOKIES:
            init_values['dhtml'] = request.COOKIES['m_dhtml']
        form = MultiEvalForm(initial=init_values)

    context = {
        'page_type': 'index',
        'title': labels['multi'],
        'formid': store_formid(request),
        'form': form,
        }

    # Return response
    t = get_template('index_multi.html')
    html = t.render(RequestContext(request, context))
    response.write(html)
    return response

#----------------------------------------------------------------
def process_dhtml(request):
    """
    Evaluate one or more DHTML DOM snapshots sent as POST data.
    """
    if not request.method == 'POST':
        raise Http404('Unable to process DHTML data!')

    if 'doc1' in request.POST and len(request.POST['doc1']):
        params = {
            'request': request,
            'url': 'Unspecified',
            'depth': '0',
            'title': 'DHTML Report',
            'username': request.user.username
            }
        now = datetime.now()
        status, uid = evaluate_dhtml(params, request.user.is_authenticated(), now)
        if status:
            if request.user.is_authenticated():
                report = UserReport(
                    id = uid,
                    user = request.user,
                    timestamp = now,
                    pgcount = status,
                    url = params['url'],
                    urlcount = 1,
                    depth = params['depth'],
                    title = params['title']
                    )
            else:
                report = GuestReport(
                    id = uid,
                    timestamp = now,
                    pgcount = status,
                    url = params['url']
                    )
            report.save()
            return HttpResponseRedirect('/report/%s/' % uid)
        else:
            return message(request, HttpResponse(), 'Unable to create report!')

    else:
        return message(request, HttpResponse(), 'No DHTML data detected!')
            
#----------------------------------------------------------------
def process_link(request):
    """
    Evaluate referrer page with direct link to FAE.
    """
    if 'HTTP_REFERER' in request.META and len(request.META['HTTP_REFERER']):
        params = {
            'url': request.META['HTTP_REFERER'],
            'depth': '0',
            'title': 'Direct Link Report',
            'username': 'guest'
            }
        now = datetime.now()
        status, uid = evaluate(params, False, now)
        if status:
            report = GuestReport(
                id = uid,
                timestamp = now,
                pgcount = status,
                url = params['url']
                )
            report.save()
            return HttpResponseRedirect('/report/%s/' % uid)
        else:
            return message(request, response, 'Unable to create report!')

    else:
        return message(request, HttpResponse(), 'No HTTP_REFERER detected!')

#----------------------------------------------------------------
def check_formid(request):
    return request.POST['formid'] == request.session.get('formid')

#----------------------------------------------------------------
def store_formid(request):
    formid = generate()
    request.session['formid'] = formid
    return formid

#----------------------------------------------------------------
def message(request, response, text):
    """
    Return the response, which may have cookie data associated
    with it, using the message template.
    """
    t = get_template('message.html')
    context = {'page_type': 'message', 'title': text}
    html = t.render(RequestContext(request, context))
    response.write(html)
    return response

#----------------------------------------------------------------
def registration_closed(request):
    """
    Return the response using the specified template.
    """
    t = get_template('registration/registration_closed.html')
    context = { 'installation': settings.INSTALLATION, 'public_url': settings.PUBLIC_URL }
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
@login_required
def archived_reports(request):
    """
    Display a list of the user's currently archived reports.
    """
    report_list = UserReport.objects.filter(user=request.user)
    context = {
        'page_type': 'archive',
        'title': labels['archive'],
        'username': request.user.username,
        'report_list': report_list
        }

    # For highlighting currently selected report in list
    report_info = request.session.get('report', {})
    if report_info: context['current_id'] = report_info['rptid']

    # Return response
    t = get_template('archive.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
@login_required
def manage_reports(request):
    """
    Allow user to select which reports should be archived.
    """
    report_list = UserReport.objects.filter(user=request.user)
    status = ''
    num_archive = 0
    for report in report_list:
        if report.archive:
            num_archive += 1

    try:
        profile = request.user.get_profile()
        quota = ACCT_TYPE_QUOTA[profile.acct_type]
        buffer = ACCT_TYPE_BUFFER[profile.acct_type]
    except ObjectDoesNotExist:
        quota = DEFAULT_QUOTA
        buffer = DEFAULT_BUFFER

    if request.method == 'POST':
        archive_info = []; i = 0
        for report in report_list:
            archive_info.append((report, ManageReportForm(request.POST, prefix=str(i), instance=report)))
            i += 1
        # validate based on number of selected reports
        count = len(request.POST)
        if count <= quota:
            for (report, form) in archive_info:
                form.save()
            status = 'Selection of permanently archived reports has been updated!'
            num_archive = count
        else:
            return message(request, HttpResponse(), 'Number of selected reports exceeds quota!')
            
    else:
        archive_info = []; i = 0
        for report in report_list:
            archive_info.append((report, ManageReportForm(prefix=str(i), instance=report)))
            i += 1

    context = {
        'page_type': 'manage',
        'title': labels['manage'],
        'username': request.user.username,
        'archive_info': archive_info,
        'report_list': report_list,
        'quota': quota,
        'buffer': buffer,
        'days_offset' : DAYS_OFFSET,
        'num_archive' : num_archive,
        'status': status,
        }

    # For highlighting currently selected report in list
    report_info = request.session.get('report', {})
    if report_info: context['current_id'] = report_info['rptid']

    # Return response
    t = get_template('manage.html')
    html = t.render(RequestContext(request, context))
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

    # If report_info doesn't exist, return error message
    if not report_info:
        return message(request, HttpResponse(), 'Report ID does not exist!')

    if type:
        report_info['type'] = type
    else:
        if not 'type' in report_info:
            report_info['type'] = default_type

    if section:
        report_info['section'] = section
    else:
        if not 'section' in report_info:
            report_info['section'] = default_section

    if pageid:
        report_info['pageid'] = pageid
    else:
        if not 'pageid' in report_info:
            report_info['pageid'] = default_pageid

    # Store report parameters in session variable
    request.session['report'] = report_info

    # Construct the document title
    title = labels['report'][report_info['type']]
    if report_info['type'] == 'page' and report_info['pgcount'] != '1':
        title += ': ' + report_info['pageid']

    # Save report_header at this point for get_report_content
    report_header = title
    if report_info['type'] == 'sitewide' or report_info['type'] == 'page':
        title += ': ' + labels['section'][report_info['section']]

    # Select the report template
    if report_info['type'] == 'sitewide':
        template_name = 'site_report.html'
    else:
        template_name = 'report.html'

    # Set up context
    context = {
        'page_type': 'report',
        'title': title,
        'content': get_report_content(report_info, report_header)
        }
    if report_info['type'] == 'sitewide' or report_info['type'] == 'page':
        context['display_sections'] = True

    # If results data was not found, return error message
    if not context['content']:
        return message(request, HttpResponse(), 'Report data does not exist!')

    # Return response
    t = get_template(template_name)
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
def pgrpteval(request):
    if request.is_ajax():
        report_info = request.session.get('report', {})
        testid = request.GET.get('testid', '')
        eval = request.GET.get('eval', '')
        content = get_pgrpteval_content(report_info, testid, eval)
    else:
        content = 'None'
    return HttpResponse(content)    

#----------------------------------------------------------------
def about(request, content_id='overview'):
    title = labels['about'] + ': ' + labels['subtitle'][content_id]
    content = 'about/' + content_id + '.html'

    context = {
        'page_type': 'about',
        'title': title,
        'subtitle': labels['subtitle'],
        'content': content,
        }

    if content_id == 'usage':
        today = date.today()
        one_week_ago = today - timedelta(days=8) # account for lag in collecting stats
        span = request.GET.get('span', '')

        if span == 'thismonth':
            stats = UsageStats.objects.filter(date__month=today.month, date__year=today.year)
        elif span == 'lastmonth':
            if today.month == 1:
                month, year = 12, today.year - 1
            else:
                month, year = today.month - 1, today.year
            stats = UsageStats.objects.filter(date__month=month, date__year=year)
        elif span == 'thisyear':
            stats = UsageStats.objects.filter(date__year=today.year)
        elif span == 'all':
            stats = UsageStats.objects.all()
        else: # Default to last seven days
            span = 'default'
            stats = UsageStats.objects.filter(date__gte=one_week_ago, date__lte=today)
        context['stats'] = stats
        context['caption'] = labels['stats'][span]

        # Aggregate totals for reports and pgcount fields
        user_reports = 0; user_pgcount = 0; guest_reports = 0; guest_pgcount = 0
        for record in stats:
            user_reports += record.user_reports
            user_pgcount += record.user_pgcount
            guest_reports += record.guest_reports
            guest_pgcount += record.guest_pgcount
        context['user_reports'] = user_reports
        context['user_pgcount'] = user_pgcount
        context['guest_reports'] = guest_reports
        context['guest_pgcount'] = guest_pgcount

    # Return response
    t = get_template('about/about.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
def get_report_info(request, rptid):
    """
    Given a report ID:
        IF rptid matches existing report_info
            return existing report_info
        ELSE
            lookup report by rptid in database
            IF found
                return a new dictionary with rptid
                and pgcount keys/values
            ELSE
                return an empty dictionary to flag
                that report does not exist
    """
    # Get latest report parameters if they exist
    report_info = request.session.get('report', {})

    if request.user.is_authenticated():
        primary   = UserReport
        secondary = GuestReport
    else:
        primary   = GuestReport
        secondary = UserReport

    if 'rptid' in report_info and report_info['rptid'] == rptid:
        return report_info
    else:
        try:
            report = primary.objects.get(id=rptid)
        except ObjectDoesNotExist:
            try:
                report = secondary.objects.get(id=rptid)
            except ObjectDoesNotExist:
                return {}

        return { 'rptid': rptid,
                 'pgcount': str(report.pgcount),
                 'filename': report.get_filename()
                 }

#----------------------------------------------------------------
def logout(request):
    from django.contrib.auth.views import logout
    return logout(request, next_page='/')

#----------------------------------------------------------------
def get_profile_data(profile_obj):
    """
    Given a user profile object, returns a dictionary representing
    its fields, suitable for passing as the initial data of a form.
    This fn. courtesy of James Bennett's broken profiles package.
    """
    opts = profile_obj._meta
    data_dict = {}
    for f in opts.fields + opts.many_to_many:
        data_dict[f.name] = f.value_from_object(profile_obj)
    return data_dict

#----------------------------------------------------------------
@login_required
def my_account(request):
    user_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
        }

    try:
        profile_obj = request.user.get_profile()
    except ObjectDoesNotExist:
        profile_obj = UserProfile(user=request.user, acct_type=1)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm(initial=user_data)
        profile_form = ProfileForm(initial=get_profile_data(profile_obj))

    context = {
        'title': labels['profile'],
        'username': request.user.username,
        'user_form': user_form,
        'profile_form': profile_form,
        }

    # Return response
    t = get_template('my_account.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)
