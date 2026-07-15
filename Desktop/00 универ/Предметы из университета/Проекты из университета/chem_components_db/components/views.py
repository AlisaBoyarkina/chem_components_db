from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Component


def component_list(request):
    """Список компонентов с поиском и фильтрацией по классу вещества."""
    search = request.GET.get('q', '').strip()
    substance_class = request.GET.get('substance_class', '').strip()

    components = Component.objects.all()

    if search:
        components = components.filter(
            Q(name__icontains=search)
            | Q(formula__icontains=search)
            | Q(cas_number__icontains=search)
            | Q(aliases__alias_name__icontains=search)
        ).distinct()

    if substance_class:
        components = components.filter(substance_class=substance_class)

    substance_classes = (
        Component.objects.exclude(substance_class="")
        .order_by('substance_class')
        .values_list('substance_class', flat=True)
        .distinct()
    )

    paginator = Paginator(components.order_by('name'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'search': search,
        'substance_class': substance_class,
        'substance_classes': substance_classes,
        'total_count': components.count(),
    }
    return render(request, 'components/list.html', context)


def component_detail(request, pk):
    """Карточка компонента со всеми свойствами и синонимами."""
    component = get_object_or_404(
        Component.objects.prefetch_related('aliases', 'properties__source'),
        pk=pk,
    )
    return render(request, 'components/detail.html', {'component': component})
