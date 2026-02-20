from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now

#===========================================
# Utils para manejo de fechas en las vistas de métricas
#===========================================
def parse_date(date_str: str):
    # Espera YYYY-MM-DD
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return make_aware(dt)
    except ValueError:
        raise ValueError("Fecha inválida. Formato esperado: YYYY-MM-DD")

def get_date_range(request):
    # Si no se proporcionan fechas, usar el rango de los últimos 30 días
    to_str = request.GET.get('to')
    from_str = request.GET.get('from')
    
    if to_str:
        end = parse_date(to_str) + timedelta(days=1)  # Incluir el día final
    else:
        end = now()
        
    if from_str:
        start = parse_date(from_str)
    else:
        start = end - timedelta(days=30)
        
    if start > end:
        raise ValueError("La fecha 'from' no puede ser posterior a la fecha 'to'.")
    
    return start, end
