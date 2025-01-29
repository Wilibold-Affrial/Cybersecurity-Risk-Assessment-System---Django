from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    # Dashboard View (List of Risk Assessments)
    path('', views.DashboardView.as_view(template_name="dashboard.html"), name='dashboard'),

    # Risk Planning View (Create new Risk Assessment)
    path('planning/', views.RiskPlanningView.as_view(template_name="risk_planning.html"), name='risk_planning'),

    # Asset List View (List of all Assets)
    path('assets/', views.AssetListView.as_view(), name='asset_list'),

    # Vulnerability Analysis View (Create Vulnerabilities)
    path('vulnerabilities/', views.VulnerabilityAnalysisView.as_view(), name='vulnerability_analysis'),

    # Threat Analysis View (Create Threats)
    path('threats/', views.ThreatAnalysisView.as_view(), name='threat_analysis'),

    # Risk Calculation View (Calculate Risk Score)
    path('risks/calculate/', views.RiskCalculationView.as_view(), name='risk_calculation'),

    # Risk Prioritization View (List all Risks prioritized by risk score)
    path('risks/prioritize/', views.RiskPrioritizationView.as_view(), name='risk_prioritization'),

    # Risk Response View (Update Risk Response based on user input)
    path('risks/<int:risk_id>/response/', views.RiskResponseView.as_view(), name='risk_response'),


    # Risk Monitoring View (List all Risks for monitoring)
    path('risks/monitor/', views.RiskMonitoringView.as_view(), name='risk_monitoring'),

    # Impact Analysis View (Update Impact of Risk)
    path('risks/impact/<int:pk>/', views.ImpactAnalysisView.as_view(), name='impact_analysis'),

    # Risk Assessment Detail View (View detailed risk assessment)
    path('assessment/<int:pk>/', views.RiskAssessmentDetailView.as_view(), name='risk_assessment_detail'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
