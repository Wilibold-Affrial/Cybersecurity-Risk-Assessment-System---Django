# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
        self.risk_score = (self.likelihood * self.impact) / 2
        return self.risk_score

    def __str__(self):
        return f"{self.name} - {self.asset.name}"

class RiskAssessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    risks = models.ManyToManyField(Risk, related_name='assessments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title