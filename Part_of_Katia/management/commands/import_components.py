import pandas as pd
from django.core.management.base import BaseCommand
from components.models import Component, ComponentAlias, DataSource, ImportLog

class Command(BaseCommand):
    help = 'Импорт компонентов из CSV/Excel файла'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к файлу .csv или .xlsx')
    
    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        self.stdout.write(f'Начинаю импорт из файла: {file_path}')
        
        # Создаём источник данных
        source, created = DataSource.objects.get_or_create(
            name='Учебный набор данных',
            defaults={'description': 'Импортированные компоненты для практики', 'url': ''}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Создан новый источник данных'))
        
        # Читаем файл
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                self.stdout.write(self.style.ERROR('Поддерживаются только .csv и .xlsx'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка чтения файла: {e}'))
            return
        
        self.stdout.write(f'Найдено строк: {len(df)}')
        
        # Проверяем обязательные колонки
        required_columns = ['name', 'formula', 'molar_mass']
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            self.stdout.write(self.style.ERROR(f'Отсутствуют обязательные колонки: {missing}'))
            return
        
        errors = []
        success_count = 0
        
        # Импортируем данные
        for index, row in df.iterrows():
            try:
                if pd.isna(row['name']) or str(row['name']).strip() == '':
                    errors.append(f'Строка {index+2}: пустое имя')
                    continue
                
                if pd.isna(row['formula']) or str(row['formula']).strip() == '':
                    errors.append(f'Строка {index+2}: пустая формула')
                    continue
                
                try:
                    molar_mass = float(row['molar_mass'])
                except:
                    errors.append(f'Строка {index+2}: молярная масса должна быть числом')
                    continue
                
                cas = str(row['cas_number']).strip() if pd.notna(row.get('cas_number')) else ''
                if cas and Component.objects.filter(cas_number=cas).exists():
                    errors.append(f'Строка {index+2}: CAS {cas} уже существует')
                    continue
                
                # Создаём компонент
                component = Component.objects.create(
                    name=str(row['name']).strip(),
                    formula=str(row['formula']).strip(),
                    cas_number=cas,
                    molar_mass=molar_mass,
                    substance_class=str(row['substance_class']).strip() if pd.notna(row.get('substance_class')) else '',
                    normal_boiling_point=float(row['normal_boiling_point']) if pd.notna(row.get('normal_boiling_point')) else None,
                    critical_temperature=float(row['critical_temperature']) if pd.notna(row.get('critical_temperature')) else None,
                    critical_pressure=float(row['critical_pressure']) if pd.notna(row.get('critical_pressure')) else None,
                    acentric_factor=float(row['acentric_factor']) if pd.notna(row.get('acentric_factor')) else None,
                )
                
                # Добавляем синонимы
                if 'alias_ru' in df.columns and pd.notna(row['alias_ru']):
                    ComponentAlias.objects.create(
                        component=component,
                        alias_name=str(row['alias_ru']).strip(),
                        alias_type='ru'
                    )
                
                if 'alias_en' in df.columns and pd.notna(row['alias_en']):
                    ComponentAlias.objects.create(
                        component=component,
                        alias_name=str(row['alias_en']).strip(),
                        alias_type='en'
                    )
                
                if 'alias_aspen' in df.columns and pd.notna(row['alias_aspen']):
                    ComponentAlias.objects.create(
                        component=component,
                        alias_name=str(row['alias_aspen']).strip(),
                        alias_type='aspen'
                    )
                
                if 'alias_hysys' in df.columns and pd.notna(row['alias_hysys']):
                    ComponentAlias.objects.create(
                        component=component,
                        alias_name=str(row['alias_hysys']).strip(),
                        alias_type='hysys'
                    )
                
                success_count += 1
                
                if success_count % 10 == 0:
                    self.stdout.write(f'Импортировано {success_count} компонентов...')
                
            except Exception as e:
                errors.append(f'Строка {index+2}: {str(e)}')
        
        # Сохраняем лог импорта
        ImportLog.objects.create(
            file_name=file_path.split('/')[-1],
            total_rows=len(df),
            success_count=success_count,
            error_count=len(errors),
            errors='\n'.join(errors[:50])
        )
        
        self.stdout.write('=' * 50)
        self.stdout.write(self.style.SUCCESS(f'✅ Успешно импортировано: {success_count} компонентов'))
        if errors:
            self.stdout.write(self.style.WARNING(f'❌ Ошибок: {len(errors)}'))
            for err in errors[:5]:
                self.stdout.write(self.style.ERROR(f'  • {err}'))
        self.stdout.write('=' * 50)
        
        total = Component.objects.count()
        self.stdout.write(f'Всего компонентов в базе: {total}')