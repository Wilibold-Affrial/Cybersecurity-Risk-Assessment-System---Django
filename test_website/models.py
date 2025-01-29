from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model

class Asset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Vulnerability(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='vulnerabilities')
    severity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.asset.name}"

class Threat(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    threat_type = models.CharField(max_length=100)
    likelihood = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Risk(models.Model):
    RISK_STATUS_CHOICES = [
        ('identified', 'Identified'),
        ('assessed', 'Assessed'),
        ('mitigated', 'Mitigated'),
        ('accepted', 'Accepted'),
        ('transferred', 'Transferred'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    threat = models.ForeignKey(Threat, on_delete=models.CASCADE)
    likelihood = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    impact = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    risk_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RISK_STATUS_CHOICES, default='identified')
    mitigation_plan = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_risk_score(self):
        if self.likelihood and self.impact:
            self.risk_score = (self.likelihood * self.impact) / 2
        return self.risk_score

    def __str__(self):
        return f"{self.name} - {self.asset.name}"

class RiskResponse(models.Model):
    RESPONSE_CHOICES = [
        ('mitigate', 'Mitigate'),
        ('accept', 'Accept'),
        ('transfer', 'Transfer'),
        ('avoid', 'Avoid'),
    ]

    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name='response')
    response_type = models.CharField(max_length=20, choices=RESPONSE_CHOICES)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.response_type} - {self.risk.name}"

class RiskAssessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50)
    risks = models.ManyToManyField(Risk, related_name='assessments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def summarize_risks(self):
        return {
            "total_risks": self.risks.count(),
            "by_status": self.risks.values('status').annotate(count=models.Count('status')),
            "by_severity": self.risks.values('impact').annotate(count=models.Count('impact')),
        }

    def __str__(self):
        return self.title
