from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la categoría")
    description = models.TextField(verbose_name="Descripción de la categoría")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        
    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Abierto'),
        ('in_progress', 'En progreso'),
        ('closed', 'Cerrado'),
        ('reopened', 'Reabierto'),
    ]
    
    title = models.CharField(max_length=250, verbose_name="Título")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Estado")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tickets', verbose_name="Categoría")
    assigned_to = models.CharField(max_length=100, verbose_name="Asignado a")
    content = models.TextField(verbose_name="Contenido")
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
    
    def __str__(self):
        return self.title
