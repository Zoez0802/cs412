# File: views.py
# Author: Minjie Zuo (minjiez@bu.edu), 3/16/2026
# Description: Views for the voter_analytics application.
# This file defines the list view for all voters and the detail view for a single voter record.

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go #task 3

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


class GraphsListView(ListView):
    """View to display graphs about voter records."""

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        """Return the voters that match the selected filters."""

        # Start with all voter records.
        voters = super().get_queryset()

        party_affiliation = self.request.GET.get('party_affiliation')
        if party_affiliation:
            voters = voters.filter(party_affiliation=party_affiliation)

        min_birth_year = self.request.GET.get('min_birth_year')
        if min_birth_year:
            voters = voters.filter(date_of_birth__year__gte=min_birth_year)

        max_birth_year = self.request.GET.get('max_birth_year')
        if max_birth_year:
            voters = voters.filter(date_of_birth__year__lte=max_birth_year)

        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            voters = voters.filter(voter_score=voter_score)

        # Filter by whether the voter participated in each election.
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
        """Provide context variables needed for the graphs page."""
        context = super().get_context_data(**kwargs)

        #a list of years for the birth-year dropdown menus.
        years = []
        for year in range(1900, 2026):
            years.append(year)

        context['years'] = years
        voters = context['voters']
        
        # graph 1: 
        # Count how many voters were born in each year.
        year_count = {}
        for voter in voters:
            y = voter.date_of_birth.year

            if y in year_count:
                year_count[y] += 1
            else:
                year_count[y] = 1

        years = list(year_count.keys())
        counts = list(year_count.values())

        # a bar chart for year of birth.
        birth_fig = go.Bar(x=years, y=counts)
        title_text = 'Voter Distribution by Year of Birth'

        graph_div_birth = plotly.offline.plot(
            {'data': [birth_fig], 'layout_title_text': title_text},
            auto_open=False,
            output_type='div'
        )

        context['graph_div_birth'] = graph_div_birth

    # Graph 2: distribution of voters by party affiliation
        # Count how many voters belong to each party.
        party_count = {}
        for voter in voters:
            party = voter.party_affiliation

            if party in party_count:
                party_count[party] += 1
            else:
                party_count[party] = 1

        years = list(party_count.keys())
        counts = list(party_count.values())

        # Create a pie chart for party affiliation.
        party_fig = go.Pie(labels=years, values=counts)
        title_text = 'Voter Distribution by Party Affiliation'

        graph_div_party = plotly.offline.plot(
            {'data': [party_fig], 'layout_title_text': title_text},
            auto_open=False,
            output_type='div'
        )

        context['graph_div_party'] = graph_div_party    
        
        
    # Graph 3: vote count by election    
        # Count how many voters participated in each election.
        election_labels = ['v20state', 'v21town', 'v21primary',
                          'v22general', 'v23town']

        vote_counts = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]

        #a bar chart for election participation.
        elections_fig = go.Bar(x=election_labels, y=vote_counts)
        title_text = 'Vote Count by Election'

        graph_div_elections = plotly.offline.plot(
            {'data': [elections_fig], 'layout_title_text': title_text},
            auto_open=False,
            output_type='div'
        )

        context['graph_div_elections'] = graph_div_elections

        return context