from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Asset, Vulnerability, Threat, Risk, RiskAssessment, RiskResponse
from .forms import RiskAssessmentForm, AssetForm, VulnerabilityForm, ThreatForm, RiskForm, RiskResponseForm, ImpactForm

class DashboardView(LoginRequiredMixin, ListView):
    model = Risk
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['high_risks'] = Risk.objects.filter(risk_score__gt=50)
        context['recent_assessments'] = RiskAssessment.objects.all().order_by('-start_date')[:5]
        context['risk_status_summary'] = Risk.objects.values('status').annotate(count=Count('status'))
        # Add a default risk if needed
        context['risk'] = Risk.objects.first()  # Or some other way to determine the default risk
        return context



class RiskPlanningView(LoginRequiredMixin, CreateView):
    model = RiskAssessment
    form_class = RiskAssessmentForm
    template_name = 'risk_planning.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.assessor = self.request.user
        return super().form_valid(form)

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'asset_list.html'
    context_object_name = 'assets'

class VulnerabilityAnalysisView(LoginRequiredMixin, CreateView):
    model = Vulnerability
    form_class = VulnerabilityForm
    template_name = 'vulnerability_analysis.html'
    success_url = reverse_lazy('asset_list')

class ThreatAnalysisView(LoginRequiredMixin, CreateView):
    model = Threat
    form_class = ThreatForm
    template_name = 'threat_analysis.html'
    success_url = reverse_lazy('dashboard')

class RiskCalculationView(LoginRequiredMixin, CreateView):
    model = Risk
    form_class = RiskForm
    template_name = 'risk_calculation.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        risk = form.save(commit=False)
        risk.calculate_risk_score()
        risk.save()
        return super().form_valid(form)

class RiskPrioritizationView(LoginRequiredMixin, ListView):
    model = Risk
    template_name = 'risk_prioritization.html'
    context_object_name = 'risks'

    def get_queryset(self):
        return Risk.objects.all().order_by('-risk_score')

class RiskResponseView(LoginRequiredMixin, CreateView):
    model = RiskResponse
    form_class = RiskResponseForm
    template_name = 'risk_response.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        risk_id = self.kwargs.get('risk_id')  # 'risk_id' instead of 'pk'
        risk = get_object_or_404(Risk, id=risk_id)
        return {'risk': risk}


class RiskMonitoringView(LoginRequiredMixin, ListView):
    model = Risk
    template_name = 'risk_monitoring.html'
    context_object_name = 'risks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mitigated_risks'] = Risk.objects.filter(status='mitigated')
        context['pending_risks'] = Risk.objects.exclude(status='mitigated')
        return context

class RiskAssessmentDetailView(LoginRequiredMixin, DetailView):
    model = RiskAssessment
    template_name = 'risk_assessment_detail.html'
    context_object_name = 'assessment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['risk_summary'] = self.object.summarize_risks()
        return context

class ImpactAnalysisView(LoginRequiredMixin, UpdateView):  # New view
    model = Risk
    form_class = ImpactForm
    template_name = 'impact_analysis.html'
    success_url = reverse_lazy('risk_prioritization')

    def form_valid(self, form):
        risk = form.save(commit=False)
        risk.calculate_risk_score()
        risk.save()
        return super().form_valid(form)