from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q
from django.core.paginator import Paginator

import plotly.graph_objs as pgo
import plotly.io as pio
from django.db.models import Count

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_list.html'
    context_object_name = 'voters'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset().order_by('last_name')
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        if party_affiliation:
            queryset = queryset.filter(party_affiliation__icontains=party_affiliation)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=f"{min_dob}-01-01")
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=f"{max_dob}-12-31")
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state == 'on':
            queryset = queryset.filter(v20state=True)
        if v21town == 'on':
            queryset = queryset.filter(v21town=True)
        if v21primary == 'on':
            queryset = queryset.filter(v21primary=True)
        if v22general == 'on':
            queryset = queryset.filter(v22general=True)
        if v23town == 'on':
            queryset = queryset.filter(v23town=True)

        print(f"Queryset count: {queryset.count()}")
        print(f"Filters: party_affiliation={party_affiliation}, min_dob={min_dob}, max_dob={max_dob}, voter_score={voter_score}, v20state={v20state}, v21town={v21town}, v21primary={v21primary}, v22general={v22general}, v23town={v23town}")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.request.GET

        queryset = self.get_queryset()
        page = self.request.GET.get('page',1)
        paginator = Paginator(queryset,self.paginate_by)
        page_obj = paginator.get_page(page)

        context['voters_page_obj'] = page_obj
        return context

class VoterDetailView(DetailView):

    model = Voter
    template_name = 'voter_detail.html'
    context_object_name = 'voter'
    pk_url_kwarg = 'pk'

class GraphsView(ListView):
    model = Voter
    template_name = 'graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('last_name')
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        if party_affiliation:
            queryset = queryset.filter(party_affiliation__icontains=party_affiliation)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=f"{min_dob}-01-01")
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=f"{max_dob}-12-31")
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state == 'on':
            queryset = queryset.filter(v20state=True)
        if v21town == 'on':
            queryset = queryset.filter(v21town=True)
        if v21primary == 'on':
            queryset = queryset.filter(v21primary=True)
        if v22general == 'on':
            queryset = queryset.filter(v22general=True)
        if v23town == 'on':
            queryset = queryset.filter(v23town=True)

        print(f"Queryset count(graph): {queryset.count()}")
        print(f"Filters(graph): party_affiliation={party_affiliation}, min_dob={min_dob}, max_dob={max_dob}, voter_score={voter_score}, v20state={v20state}, v21town={v21town}, v21primary={v21primary}, v22general={v22general}, v23town={v23town}")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()


        dob_counts = voters.values('date_of_birth').annotate(count=Count('id')).order_by('date_of_birth')
        dob_labels = [str(v['date_of_birth'].year) for v in dob_counts]
        dob_values = [v['count'] for v in dob_counts]
        fig_dob = pgo.Figure(data=[pgo.Bar(x=dob_labels, y=dob_values)])
        fig_dob.update_layout(title='Distribution of Voters by Year of Birth')
        context['graph_dob'] = pio.to_html(fig_dob, full_html=False)

        
        party_counts = voters.values('party_affiliation').annotate(count=Count('id'))
        party_labels = [v['party_affiliation'] for v in party_counts]
        party_values = [v['count'] for v in party_counts]
        fig_party = pgo.Figure(data=[pgo.Pie(labels=party_labels, values=party_values)])
        fig_party.update_layout(title='Distribution of Voters by Party Affiliation')
        context['graph_party'] = pio.to_html(fig_party, full_html=False)

        
        election_counts = {
                '2020 State': voters.filter(v20state=True).count(),
                '2021 Town': voters.filter(v21town=True).count(),
                '2021 Primary': voters.filter(v21primary=True).count(),
                '2022 General': voters.filter(v22general=True).count(),
                '2023 Town': voters.filter(v23town=True).count(),
                }
        
        election_labels = list(election_counts.keys())
        election_values = list(election_counts.values())
        fig_election = pgo.Figure(data=[pgo.Bar(x=election_labels, y=election_values)])
        fig_election.update_layout(title='Distribution of Voters by Election Participation')
        context['graph_election'] = pio.to_html(fig_election, full_html=False)

        return context
