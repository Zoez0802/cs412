# File: views.py
# Author: Minjie Zuo (minjiez@bu.edu), 3/16/2026
# Description: Views for the voter_analytics application.
# This file defines the list view for all voters and the detail view for a single voter record.

from django.views.generic import ListView, DetailView
from .models import Voter

class VotersListView(ListView):
    """View to display voter records."""

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Return the voters that match the selected filters."""

        # Start with all voter records.
        voters = super().get_queryset()

        # party affiliation.
        party_affiliation = self.request.GET.get('party_affiliation')
        if party_affiliation:
            voters = voters.filter(party_affiliation=party_affiliation)

        # minimum birth year.
        min_birth_year = self.request.GET.get('min_birth_year')
        if min_birth_year:
            voters = voters.filter(date_of_birth__year__gte=min_birth_year)

        # maximum birth year.
        max_birth_year = self.request.GET.get('max_birth_year')
        if max_birth_year:
            voters = voters.filter(date_of_birth__year__lte=max_birth_year)

        # voter score.
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            voters = voters.filter(voter_score=voter_score)

        # whether the voter participated in each election.
        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state=True)
        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general=True)
        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        """Provide extra context variables for the search form."""

        context = super().get_context_data(**kwargs)

        #a list of years for the search form.
        years = []
        for year in range(1900, 2026):
            years.append(year)

        context['years'] = years
        return context
    
class VoterDetailView(DetailView):
    """View to show one voter record."""

    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'