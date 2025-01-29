"""
URL configuration for test_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(template_name="dashboard.html"), name='dashboard'),
    path('planning/', views.RiskPlanningView.as_view(), name='risk_planning'),
    path('assets/', views.AssetListView.as_view(), name='asset_list'),
    path('vulnerabilities/', views.VulnerabilityAnalysisView.as_view(), name='vulnerability_analysis'),
    path('threats/', views.ThreatAnalysisView.as_view(), name='threat_analysis'),
    path('risks/calculate/', views.RiskCalculationView.as_view(), name='risk_calculation'),
    path('risks/prioritize/', views.RiskPrioritizationView.as_view(), name='risk_prioritization'),
    path('risks/<int:pk>/response/', views.RiskResponseView.as_view(), name='risk_response'),
    path('risks/monitor/', views.RiskMonitoringView.as_view(), name='risk_monitoring'),
]
