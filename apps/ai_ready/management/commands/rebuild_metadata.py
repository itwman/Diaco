"""
Diaco MES - Rebuild AI Metadata
==================================
بروزرسانی metadata تمام رکوردهای تولید.
برای اجرای یکباره یا cron job.

Usage:
    python manage.py rebuild_metadata
    python manage.py rebuild_metadata --model spinning
"""
from django.core.management.base import BaseCommand

from apps.blowroom.models import Batch as BlowroomBatch
from apps.carding.models import Production as CardingProd
from apps.passage.models import Production as PassageProd
from apps.finisher.models import Production as FinisherProd
from apps.spinning.models import Production as SpinningProd
from apps.dyeing.models import Batch as DyeingBatch
from apps.maintenance.models import DowntimeLog


MODEL_MAP = {
    'blowroom': BlowroomBatch,
    'carding': CardingProd,
    'passage': PassageProd,
    'finisher': FinisherProd,
    'spinning': SpinningProd,
    'dyeing': DyeingBatch,
    'downtime': DowntimeLog,
}


class Command(BaseCommand):
    help = 'بروزرسانی metadata تمام رکوردهای تولید برای AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model', type=str, default='all',
            help='مدل مشخص (blowroom/carding/passage/finisher/spinning/dyeing/downtime) یا all',
        )

    def handle(self, *args, **options):
        target = options['model']
        models_to_process = MODEL_MAP if target == 'all' else {target: MODEL_MAP.get(target)}

        if None in models_to_process.values():
            self.stderr.write(self.style.ERROR(f'مدل نامعتبر: {target}'))
            return

        total = 0
        for name, Model in models_to_process.items():
            count = 0
            qs = Model.objects.all()
            self.stdout.write(f'  پردازش {name} ({qs.count()} رکورد)...')
            for obj in qs.iterator():
                obj.save()  # signal فعال می‌شود و metadata پر می‌شود
                count += 1
            total += count
            self.stdout.write(self.style.SUCCESS(f'    ✓ {count} رکورد بروز شد'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ کل: {total} رکورد metadata بروزرسانی شد'))
