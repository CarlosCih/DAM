from django.core.management.base import BaseCommand
from metrics.models import Category, Ticket
import random


class Command(BaseCommand):
    help = 'Carga datos de prueba: 10 categorías y 50 tickets'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
        Ticket.objects.all().delete()
        Category.objects.all().delete()

        # Datos de categorías
        categorias_data = [
            ('Soporte Técnico', 'Problemas técnicos y solicitudes de soporte de TI'),
            ('Hardware', 'Incidencias relacionadas con equipos y componentes físicos'),
            ('Software', 'Problemas de aplicaciones y sistemas operativos'),
            ('Red', 'Problemas de conectividad y configuración de red'),
            ('Seguridad', 'Incidentes de seguridad y vulnerabilidades'),
            ('Desarrollo', 'Solicitudes y bugs del equipo de desarrollo'),
            ('Base de Datos', 'Problemas con bases de datos y consultas'),
            ('Infraestructura', 'Servidores, cloud y recursos de infraestructura'),
            ('Usuarios', 'Gestión de cuentas y permisos de usuarios'),
            ('Mantenimiento', 'Tareas de mantenimiento preventivo y correctivo'),
        ]

        self.stdout.write(self.style.SUCCESS('Creando 10 categorías...'))
        categorias = []
        for nombre, descripcion in categorias_data:
            categoria = Category.objects.create(
                name=nombre,
                description=descripcion
            )
            categorias.append(categoria)
            self.stdout.write(f'  ✓ Categoría creada: {nombre}')

        # Datos de tickets
        titulos = [
            'No puedo acceder al sistema',
            'Error al iniciar sesión',
            'Computadora no enciende',
            'Impresora sin conexión',
            'Internet lento',
            'Actualización de software requerida',
            'Password olvidado',
            'Sistema congelado',
            'Error en aplicación',
            'Solicitud de nuevo equipo',
            'Problema con el correo electrónico',
            'Base de datos no responde',
            'Servidor caído',
            'Backup fallido',
            'Virus detectado',
            'Acceso denegado',
            'Pantalla azul',
            'Teclado no funciona',
            'Mouse defectuoso',
            'Monitor no enciende',
            'Red wifi desconectada',
            'VPN no conecta',
            'Aplicación crashea',
            'Datos perdidos',
            'Sistema lento',
            'Disco duro lleno',
            'Migración de datos',
            'Instalación de software',
            'Configuración de equipos nuevos',
            'Auditoría de seguridad',
        ]

        nombres_asignados = [
            'Juan Pérez',
            'María González',
            'Carlos Rodríguez',
            'Ana Martínez',
            'Luis Sánchez',
            'Carmen López',
            'José Fernández',
            'Laura García',
        ]

        contenidos = [
            'Necesito ayuda urgente con este problema.',
            'El problema comenzó esta mañana.',
            'No puedo completar mi trabajo debido a este inconveniente.',
            'Varios usuarios están reportando el mismo problema.',
            'Es un problema recurrente que necesita solución definitiva.',
            'Solicito revisión y solución a la brevedad posible.',
            'El problema afecta la productividad del equipo.',
            'Necesito apoyo técnico especializado.',
            'Ya intenté reiniciar pero el problema persiste.',
            'Es crítico resolver este problema hoy.',
        ]

        status_choices = ['open', 'in_progress', 'closed', 'reopened']

        self.stdout.write(self.style.SUCCESS('Creando 50 tickets...'))
        for i in range(50):
            titulo = random.choice(titulos) + f' #{i+1}'
            ticket = Ticket.objects.create(
                title=titulo,
                status=random.choice(status_choices),
                category=random.choice(categorias),
                assigned_to=random.choice(nombres_asignados),
                content=random.choice(contenidos)
            )
            status_display = dict(Ticket.STATUS_CHOICES)[ticket.status]
            self.stdout.write(f'  ✓ Ticket creado: {titulo} - [{status_display}]')

        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS CREADOS:'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'Total de categorías: {Category.objects.count()}')
        self.stdout.write(f'Total de tickets: {Ticket.objects.count()}')
        self.stdout.write('')
        self.stdout.write('Tickets por estado:')
        for status_code, status_name in Ticket.STATUS_CHOICES:
            count = Ticket.objects.filter(status=status_code).count()
            self.stdout.write(f'  • {status_name}: {count}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✓ Datos de prueba cargados exitosamente!'))
