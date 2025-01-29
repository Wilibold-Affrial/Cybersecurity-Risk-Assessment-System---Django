# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Asset, Vulnerability, Threat, Risk, RiskAssessment
from .forms import RiskAssessmentForm, AssetForm, VulnerabilityForm, ThreatForm, RiskForm

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'risk_assessment/dashboard.html'
    model = RiskAssessment
    context_object_name = 'assessments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['high_risks'] = Risk.objects.filter(risk_score__gte=7).order_by('-risk_score')[:5]
        context['recent_assessments'] = RiskAssessment.objects.order_by('-created_at')[:5]
        return context

class RiskPlanningView(LoginRequiredMixin, CreateView):
    model = RiskAssessment
    form_class = RiskAssessmentForm
    template_name = 'risk_assessment/risk_planning.html'
    success_url = reverse_lazy('dashboard')

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'risk_assessment/asset_list.html'
    context_object_name = 'assets'

class VulnerabilityAnalysisView(LoginRequiredMixin, CreateView):
    model = Vulnerability
    form_class = VulnerabilityForm
    template_name = 'risk_assessment/vulnerability_analysis.html'
    success_url = reverse_lazy('asset_list')

class ThreatAnalysisView(LoginRequiredMixin, CreateView):
    model = Threat
    form_class = ThreatForm
    template_name = 'risk_assessment/threat_analysis.html'
    success_url = reverse_lazy('dashboard')

class RiskCalculationView(LoginRequiredMixin, CreateView):
    model = Risk
    form_class = RiskForm
    template_name = 'risk_assessment/risk_calculation.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        risk = form.save(commit=False)
        risk.calculate_risk_score()
        return super().form_valid(form)

class RiskPrioritizationView(LoginRequiredMixin, ListView):
    model = Risk
    template_name = 'risk_assessment/risk_prioritization.html'
    context_object_name = 'risks'

    def get_queryset(self):
        return Risk.objects.all().order_by('-risk_score')

class RiskResponseView(LoginRequiredMixin, UpdateView):
    model = Risk
    fields = ['status', 'mitigation_plan']
    template_name = 'risk_assessment/risk_response.html'
    success_url = reverse_lazy('dashboard')

class RiskMonitoringView(LoginRequiredMixin, ListView):
    model = Risk
    template_name = 'risk_assessment/risk_monitoring.html'
    context_object_name = 'risks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mitigated_risks'] = Risk.objects.filter(status='mitigated')
        context['pending_risks'] = Risk.objects.exclude(status='mitigated')
        return context