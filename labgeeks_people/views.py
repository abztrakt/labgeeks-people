from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
import json
from labgeeks_people.forms import *
from labgeeks_people.models import *
from badger.models import Badge, Award
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import PermissionDenied
from django.views.generic.base import View
from django.views.generic.edit import FormView
from forms_builder.forms.signals import *
from forms_builder.forms.forms import FormForForm
from django.utils.decorators import method_decorator


class ViewReviews(View):
    """Display all submitted reviews of a user"""

    @method_decorator(login_required)
    def get(self, request, user):
        forms = ReviewForm.objects.all()
        official_reviews = forms[0].entries.filter(reviewing=user, final=True, official=True)
        print official_reviews
        if request.user.has_perm('labgeeks_people.finalize_review') or request.user == user:
            final_reviewer = True
        else:
            final_reviewer = False
        params = {'current_user': request.user, 'form': forms[0], 'official_reviews': official_reviews, 'final_reviewer': final_reviewer, 'user': user}
        return render(request, 'view_reviews.html', params)

        """def post(self, request, user):
            published = ReviewForm.objects.published()
            form = get_object_or_404(published[0])
            request_context = RequestContext(request)
            form_vars = (form, request_context, request.POST or None, request.FILES or None)
            save_form = SaveForm(*form_vars)
            # check for save or sumbit, if save then save(commit=False), store model instance for later use
            # then add checks for if a review was started
            if not save_form.is_valid():
                form_invalid.send(sender=request, form=save_form)
            else:
                form_entry = save_form.save()
                form_valid.send(sender=request, form=save_form, entry=form_entry)
            return redirect("submit/")"""


class SubmitReview(View):
    def get(self, request, user):
        if request.user.has_perm('labgeeks_people.finalize_review'):
            final_reviewer = True
        else:
            final_reviewer = False
        return render(request, "sent.html", {'reviewee': user, 'final_reviwer': final_reviewer})


class CreateReview(View):
    """Fill out a previously made review form for a user"""

    def get(self, request, user):
        if request.user.has_perm('labgeeks_people.finalize_review'):
            final_reviewer = True
        else:
            final_reviewer = False
        forms = ReviewForm.objects.published()
        form = get_object_or_404(forms[0])
        incomplete_reviews = ReviewFormEntry.objects.filter(reviewing=user, final=False, reviewer=request.user)
        if request.user.username == user:
            review_self = True
        else:
            review_self = False
        if request.user.has_perm('labgeeks_people.add_uwltreview'):
            can_add_review = True
        else:
            can_add_review = False
        params = {'user': user, 'final_reviewer': final_reviewer, 'can_add_review': can_add_review, 'review_self': review_self}
        #check for unfinished reviews, if so build form with unfinished data inserted
        if incomplete_reviews:
            request_context = RequestContext(request)
            incomplete_review = incomplete_reviews[0]
            form_vars = (form, request_context, request.POST or None, request.FILES or None)
            kwargs = {'instance': incomplete_reviewi, 'user': user}
            save_form = SaveForm(*form_vars, **kwargs)
            params['save_form'] = save_form
            incomplete_review.delete()
        if final_reviewer:
            staff_reviews = []
            reviews = ReviewFormEntry.objects.filter(reviewing=user, final=True, official=False)
            for review in reviews:
                if not review.official:
                    staff_reviews.append(review)
            params['staff_reviews'] = staff_reviews
        if not form:
            params['form'] = "No forms created"
        else:
            params['form'] = form
        return render(request, 'reviews.html', params)

    def post(self, request, user):
        published = ReviewForm.objects.published()
        form = get_object_or_404(published[0])
        request_context = RequestContext(request)
        form_vars = (form, request_context, request.POST or None, request.FILES or None)
        save_form = SaveForm(*form_vars)
        if not save_form.is_valid():
            form_invalid.send(sender=request, form=save_form)
        else:
            form_entry = save_form.save(commit=False)
            if request.user.has_perm('labgeeks_people.finalize_review'):
                form_entry.official = True
            form_entry.save()
            form_valid.send(sender=request, form=save_form, entry=form_entry)
        return redirect("submit/")

@login_required
def list_all(request):
    """ List all users in the system. (Alphabetically, ignoring case)
    """
    this_user = request.user
    if this_user.has_perm('labgeeks_people.add_uwltreview'):
        can_add_review = True
    else:
        can_add_review = False

    #Separate out the list of users by their group association.
    groups = Group.objects.all()
    group_list = []
    for group in groups:
        users = group.user_set.filter(is_active=True).extra(select={'username_upper': 'upper(username)'}, order_by=['username_upper'])
        data = {
            'group_name': group.name,
            'users': users,
        }
        group_list.append(data)

    # Lastly, grab all users who don't belong to a group.
    no_group = {
        'group_name': 'Users with no groups associated with them.',
        'users': User.objects.filter(groups=None)
    }
    if no_group['users']:
        group_list.append(no_group)

    return render_to_response('list.html', locals(), context_instance=RequestContext(request))


@login_required
def view_profile(request, name):
    """ Show a user profile.
    """
    user = User.objects.get(username=name)
    badge_list = Badge.objects.filter(creator=user) 
    if UserProfile.objects.filter(user=user):
        #User has already created a user profile.
        profile = UserProfile.objects.get(user=user)
        award_list = Award.objects.filter(user=user)
        if request.user == user or request.user.has_perm('labgeeks_people.change_userprofile'):
            edit = True
        if request.user == user or request.user.has_perm('labgeeks_people.view_wagehistory'):
            can_view_wage_history = True
        if request.user == user or request.user.has_perm('labgeeks_people.add_uwltreview'):
            can_view_review = True

        return render_to_response('profile.html', locals(), context_instance=RequestContext(request))
    else:
        #User HAS NOT created a user profile, allow them to create one.
        return create_user_profile(request, name)


@login_required
def create_user_profile(request, name):
    """ This view is called when creating or editing a user profile to the system.
        Allows the user to edit and display certain things about their information.
    """
    if request.user.__str__() == name or request.user.has_perm('labgeeks_people.change_userprofile'):
        can_edit = True
    else:
        can_edit = False

    if request.user.__str__() == name or request.user.has_perm('labgeeks_people.add_userprofile'):
        can_add = True
    else:
        can_add = False

    c = {}
    c.update(csrf(request))

    #Grab the user that the name belongs to and check to see if they have an existing profile.
    user = User.objects.get(username=name)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if (not can_edit and profile) or (not can_add and not profile):
        # Don't allow editing or adding of other people's profiles unless permission assigned
        return render_to_response('not_your_profile.html', locals(), context_instance=RequestContext(request))

    if request.method == 'POST':
        form = CreateUserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            gtg = True
            validation_message = False
            if 'staff_photo' in request.FILES:
                try:
                    form.clean_image()
                except:
                    validation_message = 'Image is too large (bigger than 1024*1024).  Try a smaller one!'
                    gtg = False
            if gtg:
                if profile:
                    # Update the user profile
                    profile = form.save()
                else:
                    # Create a user profile, but DON'T add to database quite yet.
                    profile = form.save(commit=False)

                    # Add user to the profile and save
                    profile.user = user
                    profile.save()

                    # Now, save the many-to-many data for the form (Required when commit=False)
                    form.save_m2m()

                # Allow editing right after creating/editing a profile.
                edit = True
                # View the profile
                return render_to_response('profile.html', locals(), context_instance=RequestContext(request))
    else:
        form = CreateUserProfileForm(instance=profile)

    # Differentiate between a super user creating a profile or a person creating their own profile.
    this_user = request.user
    if profile:
        message = "You are editing a user profile for "
    else:
        message = "You are creating a user profile for "

    if this_user.__str__() == name:
        message += "yourself."
    else:
        message += name + "."
    # The following code is used for displaying the user's call_me_by or first name.
    try:
        profile = UserProfile.objects.get(user=this_user)
        if profile.call_me_by:
            this_user = profile.call_me_by
        else:
            this_user = this_user.first_name
    except:
        this_user = user.first_name

    return render_to_response('create_profile.html', locals(), context_instance=RequestContext(request))


@login_required
def view_wage_history(request, user):

    user = User.objects.get(username=user)
    this_user = request.user

    if this_user != user and not this_user.has_perm('labgeeks_people.view_wagehistory'):
        raise PermissionDenied

    try:
        histories = WageHistory.objects.filter(user=user).order_by('-effective_date')
    except WageHistory.DoesNotExist:
        histories = None

    has_history = True

    if len(histories) == 0:
        has_history = False

    wages = []
    dates = []
    reasons = []
    wage_changes = []
    description = []

    try:
        profile = UserProfile.objects.get(user=user)
        if profile.call_me_by:
            user_name = profile.call_me_by + ' ' + user.last_name
        else:
            user_name = user.first_name + ' ' + user.last_name
    except:
        user_name = user.first_name + ' ' + user.last_name

    for history in histories:
        wages.append(history.wage)
        dates.append(history.effective_date)
        reasons.append(history.wage_change_reason)
        description.append(history.wage_change_reason.description)

    for i in range(len(wages)):
        holder = {
            'date': dates[i],
            'wage': wages[i],
            'reason': reasons[i],
            'desc': description[i],
        }
        wage_changes.append(holder)

    args = {
        'request': request,
        'has_history': has_history,
        'wage_changes': wage_changes,
        'user': user_name,
    }
    return render_to_response('wage_history.html', args)


@login_required
def edit_reviews(request, user):
    # Grab the user and any reviews they may have.
    user = User.objects.get(username=user)
    this_user = request.user
    if this_user.has_perm('labgeeks_people.add_uwltreview'):
        can_add_review = True
    else:
        can_add_review = False

    if not can_add_review:
        raise PermissionDenied

    if this_user.has_perm('labgeeks_people.finalize_review'):
        final_reviewer = True
    else:
        final_reviewer = False

    try:
        badge_photo = UserProfile.objects.get(user=user).bagde_photo._get_url()
    except:
        badge_photo = None

    # Handle the form submission and differentiate between the sub-reviewers
    # and the final reviewer.
    try:
        recent_review = UWLTReview.objects.filter(reviewer=this_user, user=user, is_final=False, is_used_up=False).order_by('-date')[0]
    except:
        recent_review = None

    wage_history_holder = WageHistory.objects.filter(user=user).order_by('effective_date').reverse()

    if wage_history_holder:
        last_wage_history = wage_history_holder[0]
    else:
        last_wage_history = None

    if last_wage_history:
        last_wage = last_wage_history.wage
        last_wage_string = str(last_wage)
    else:
        last_wage_string = 'none'
        last_wage = None

    last_wage_history_help = "Enter an updated wage for " + user.__unicode__() + " (last wage: " + last_wage_string + ")"

    if request.method == 'POST':

        if final_reviewer:
            form = CreateFinalUWLTReviewForm(request.POST, instance=recent_review)
            form2 = UpdateWageHistoryForm(request.POST, user=user)
        else:
            form = CreateUWLTReviewForm(request.POST, instance=recent_review)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.date = datetime.now().date()
            review.reviewer = this_user
            review.is_used_up = False

            if final_reviewer:
                if form2.is_valid():
                    wage_history = form2.save(commit=False)
                    wage_history.user = user
                    wage_history.effective_date = datetime.now().date()
                    if last_wage_history:
                        if last_wage != wage_history.wage and wage_history.wage is not None:
                            wage_history.save()
                    elif wage_history.wage is not None:
                        wage_history.save()

            # If the review is FINAL, mark the other reviews as used up and
            # don't show use them for averaging the scores.
            if 'is_final' in form.cleaned_data.keys() and form.cleaned_data['is_final']:
                old_reviews = UWLTReview.objects.filter(user=user, is_final=False, is_used_up=False)
                for old_review in old_reviews:
                    old_review.is_used_up = True
                    old_review.save()
                review.is_used_up = False

            review.save()
            form.save_m2m()
            recent_review = review
            return HttpResponseRedirect('')
    else:
        if final_reviewer:
            form = CreateFinalUWLTReviewForm(instance=recent_review)
            form2 = UpdateWageHistoryForm(instance=last_wage_history, user=user)
        else:
            form = CreateUWLTReviewForm(instance=recent_review)

    # Gather the data from the reviews and separate out fields.
    review_stats = {}
    comment_stats = []

    try:
        reviews = UWLTReview.objects.filter(user=user, is_used_up=False).order_by('-date')
    except UWLTReview.DoesNotExist:
        reviews = None

    for review in reviews:
        scores = get_scores(review)
        comments = get_comments(review)
        for key, value in scores.items():
            if final_reviewer and review.reviewer != this_user:
                stats = {'value': value, 'reviewer': review.reviewer, 'comments': comments[key]}
                if key in review_stats.keys():
                    review_stats[key].append(stats)
                else:
                    review_stats[key] = [stats]
        if final_reviewer and not review.is_final:
            comment_stats.append({'reviewer': review.reviewer, 'value': review.comments})

    # Create a list of all of the review fields and append review stats along
    # with them. The stats won't be appended if the review isn't a final one.
    form_fields = []
    for field in form.visible_fields():
        stats = None
        stats_text = ''
        if final_reviewer:
            name = (' '.join(str(x) for x in field.name.split('_'))).title()
            if name in review_stats.keys():
                stats_text = "Leads other scores:"
                stats = review_stats[name]
                avg = sum(int(v['value']) for v in stats) / len(stats)
                stats.append({'value': avg, 'reviewer': 'AVERAGE', 'comments': ''})
            if name == 'comments':
                stats_text = "Leads other comments:"
                stats = comment_stats

        field_info = {
            'label_tag': field.label_tag,
            'help_text': field.help_text,
            'field': field,
            'name': field.name,
            'stats': stats,
            'stats_text': stats_text,
        }

        form_fields.append(field_info)

    form2_fields = []
    if final_reviewer:
        for field in form2.visible_fields():
            # wage help text/previous wage not showing up for some reason, so this is my stopgap answer
            if field.name == "wage":
                field.help_text = last_wage_history_help
            field_info = {
                'label_tag': field.label_tag,
                'help_text': field.help_text,
                'field': field,
            }
            form2_fields.append(field_info)

    # Notify the user of a previous review.
    recent_message = ''
    if recent_review:
        recent_message = 'Looks like you made a review for %s on %s. Saved entries have been filled out.' % (user, recent_review.date)

    # The following code is used for displaying the user's call_me_by or first
    # name.
    try:
        profile = UserProfile.objects.get(user=this_user)
        if profile.call_me_by:
            this_user = profile.call_me_by
        else:
            this_user = this_user.first_name
    except:
        this_user = user.first_name

    # Return anything needed for the review form.
    args = {
        'request': request,
        'form_fields': form_fields,
        'form2_fields': form2_fields,
        'this_user': this_user,
        'user': user,
        'badge_photo': badge_photo,
        'can_add_review': can_add_review,
        'recent_message': recent_message,
        'final_reviewer': final_reviewer,
    }
    return render_to_response('reviews.html', args, context_instance=RequestContext(request))


def view_reviews(request, user):
    this_user = request.user
    user = User.objects.get(username=user)

    if this_user.has_perm('labgeeks_people.finalize_review'):  # change to labgeeks_people.finalize_review for modularity
        final_reviewer = True
    else:
        final_reviewer = False

    if not final_reviewer and this_user != user:
        raise PermissionDenied

    try:
        badge_photo = UserProfile.objects.get(user=user).bagde_photo._get_url()
    except:
        badge_photo = None
    try:
        reviews = UWLTReview.objects.filter(user=user, is_used_up=False).order_by('-date')
    except UWLTReview.DoesNotExist:
        reviews = None

    # Used for table viewing.
    table_dict = {}
    if this_user == user:
        table_dict['user'] = 'Your review scores:'
    else:
        table_dict['user'] = "%s's review scores:" % user.username

    table_date_info = []
    table_scores = {}
    weights = []
    averages = []

    for review in reviews:
        scores = get_scores(review)
        comments = get_comments(review)
        if review.is_final:
            weights.append(weight_review(review))
            total = sum(dict.values(scores)) * 1.0
            averages.append("%.2f" % (total / len(scores)))
        for key, value in scores.items():
            if review.is_final:
                if key in table_scores.keys():
                    table_scores[key].append(value)
                else:
                    table_scores[key] = [value]

        if review.is_final:
            table_date_info.append({'date': review.date, 'id': review.id})

    table_dict['scores'] = table_scores
    table_dict['date'] = table_date_info

    args = {
        'request': request,
        'table_dict': table_dict,
        'weights': weights,
        'averages': averages,
        'this_user': this_user,
        'user': user,
        'badge_photo': badge_photo,
        'final_reviewer': final_reviewer,
    }

    return render_to_response('view_reviews.html', args)


def view_review_data(request, user):
    user = User.objects.get(username=user)
    this_user = request.user
    data = request.REQUEST.copy()
    review_id = data.getlist('id')[0]
    try:
        review = UWLTReview.objects.get(id=review_id)
    except:
        raise PermissionDenied
    if this_user.has_perm('labgeeks_people.finalize_review') and this_user != user:
        can_finalize_review = True
    else:
        can_finalize_review = False

    if not can_finalize_review and not this_user == user or not review.is_final:
        result = json.dumps({
            'return_status': False,
            'message': 'You do not have permission to view this review.'
        })
        return HttpResponse(result)
    else:
        scores = get_scores(review)
        comments = get_comments(review)
        weighted = weight_review(review)
        total = sum(dict.values(scores)) * 1.0
        average = "%.2f" % (total / len(scores))

        result = json.dumps({
            'return_status': True,
            'user': str(review.user),
            'scores': scores,
            'weighted': weighted,
            'average': average,
            'date': review.date.strftime('%b %d, %Y'),
            'comments': comments,
            'overall': review.comments
        })
        return HttpResponse(result)


def weight_review(review):
    """
    takes a review and returns the weighted average
    """
    if review.weights:
        t = review.weights.teamwork_multiplier
        cs = review.weights.customer_service_multiplier
        d = review.weights.dependability_multiplier
        i = review.weights.integrity_multiplier
        c = review.weights.communication_multiplier
        ini = review.weights.initiative_multiplier
        a = review.weights.attitude_multiplier
        p = review.weights.productivity_multiplier
        tk = review.weights.technical_knowledge_multiplier
        r = review.weights.responsibility_multiplier
        po = review.weights.policies_multiplier
        pr = review.weights.procedures_multiplier
        numerator = t * review.teamwork + cs * review.customer_service + d * review.dependability + i * review.integrity + c * review.communication + ini * review.initiative + a * review.attitude + p * review.productivity + tk * review.technical_knowledge + r * review.responsibility + po * review.policies + pr * review.procedures
        denominator = t + cs + d + i + c + ini + a + p + tk + r + po + pr
        return round((numerator / denominator), 2)

    return "N/A"


def get_scores(review):
    """
    Takes a review and returns the scores as a dictionary
    """
    return {
        'Teamwork': review.teamwork,
        'Customer Service': review.customer_service,
        'Dependability': review.dependability,
        'Integrity': review.integrity,
        'Communication': review.communication,
        'Initiative': review.initiative,
        'Attitude': review.attitude,
        'Productivity': review.productivity,
        'Technical Knowledge': review.technical_knowledge,
        'Responsibility': review.responsibility,
        'Policies': review.policies,
        'Procedures': review.procedures,
    }


def get_comments(review):

    return {
        'Teamwork': review.teamwork_comments,
        'Customer Service': review.customer_service_comments,
        'Dependability': review.dependability_comments,
        'Integrity': review.integrity_comments,
        'Communication': review.communication_comments,
        'Initiative': review.initiative_comments,
        'Attitude': review.attitude_comments,
        'Productivity': review.productivity_comments,
        'Technical Knowledge': review.technical_knowledge_comments,
        'Responsibility': review.responsibility_comments,
        'Policies': review.policies_comments,
        'Procedures': review.procedures_comments,
    }
