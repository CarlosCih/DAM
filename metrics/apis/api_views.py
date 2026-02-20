from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Count,Avg, F, ExpressionWrapper, DurationField
from django.utils.timezone import make_aware, now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import SummarySerializer, ChartDataSerializer

from ..models import Ticket
from ..utils.utils import get_date_range

# Api views para las métricas, funcion: muestra un resumen de las métricas principales (total, abiertos, cerrados, etc) en un rango de fechas dado. Si no se dan fechas, se muestra el resumen de los últimos 30 días.
class MetricsSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            start, end = get_date_range(request)
            qs= Ticket.objects.filter(created_at__gte=start, created_at__lt=end)
            
            # Cálculo de métricas
            total = qs.count()
            open_count = qs.filter(status='open').count()
            in_progress_count = qs.filter(status='in_progress').count()
            closed_count = qs.filter(status='closed').count()
            reopened_count = qs.filter(status='reopened').count()
            
            # promedio de duración: tiempo entre creación y cierre (solo para tickets cerrados)
            closed_tickets = ExpressionWrapper(
                F("closed_at")-F("created_at"),
                output_field=DurationField()
            )
            
            # Cálculo del promedio de duración en horas
            avg_duration = (
                qs.filter(status='closed', closed_at__isnull=False)
                .annotate(duration=closed_tickets)
                .aggregate(avg=Avg('duration'))['avg']
            )
            
            avg_hours = (avg_duration.total_seconds() / 3600) if avg_duration else None
            
            payload = {
                "total": total,
                "open": open_count,
                "in_progress": in_progress_count,
                "closed": closed_count,
                "reopened": reopened_count,
                "avg_resolution_hours": round(avg_hours, 2) if avg_hours is not None else None,
            }
            
            return Response(payload)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Error interno del servidor"}, status=500)

# Api view para series temporales: muestra la cantidad de tickets creados o cerrados por día en un rango de fechas dado. El cliente puede elegir si quiere ver los tickets creados o cerrados.        
class MetricsTimeSeriesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Implementación de la vista para series temporales
            start, end = get_date_range(request)
            metric = request.GET.get('metric', 'created')
            
            if metric == 'closed':
                base = Ticket.objects.filter(
                    status='closed',
                    closed_at__isnull=False,
                    closed_at__gte=start,
                    closed_at__lt=end
                ).annotate(day=TruncDay("closed_at"))
            else:
                base = Ticket.objects.filter(
                    created_at__gte=start,
                    created_at__lt=end
                ).annotate(day=TruncDay("created_at"))
                
            rows = base.values("day").annotate(values=Count("id")).order_by("day")
            
            labels = [r["day"].strftime("%Y-%m-%d") for r in rows]
            
            values = [r["values"] for r in rows]
            
            payload = {
                "labels": labels,
                "datasets": [
                    {
                        "label": f"Tickets {metric}",
                        "data": values,
                    }
                ]
            }
            
            return Response(ChartDataSerializer(payload).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Error interno del servidor"}, status=500)

# Api view para breakdown: muestra la cantidad de tickets agrupados por una categoría 
class MetricsBreakdownView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Implementación de la vista para breakdown
            start, end = get_date_range(request)
            by = request.GET.get('by', 'status') # status, category,
            
            allowed = {
                'status',
                'category',
            }
            
            if by not in allowed:
                raise ValueError(f"Parámetro 'by' inválido. Valores permitidos: {', '.join(allowed)}")
            
            qs = Ticket.objects.filter(created_at__gte=start, created_at__lt=end)
            
            rows = qs.values(by).annotate(value=Count("id")).order_by("-value")
            
            labels = [str(r[by] or "Sin asignar") for r in rows]
            
            values = [r["value"] for r in rows]
            
            payload = {
                "labels": labels,
                "datasets": [
                    {
                        "label": f"Tickets por {by}",
                        "data": values,
                    }
                ]
            }
            
            return Response(ChartDataSerializer(payload).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Error interno del servidor"}, status=500)
        