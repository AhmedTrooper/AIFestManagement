from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserRole, Role, Fest, Item, ItemRule

class Command(BaseCommand):
	help = "Bootstrap demo data: authority user, one fest with items and rules"

	def handle(self, *args, **options):
		user, _ = User.objects.get_or_create(username="authority")
		if not user.has_usable_password():
			user.set_password("authority123")
			user.save()
		UserRole.objects.update_or_create(user=user, defaults={"role": Role.AUTHORITY})

		fest, _ = Fest.objects.get_or_create(
			name="AI Fest Demo",
			defaults={"description": "Demo fest", "created_by": user, "is_published": True},
		)
		item, _ = Item.objects.get_or_create(
			fest=fest,
			title="Hackathon",
			defaults={"description": "Build something cool", "max_team_size": 4},
		)
		ItemRule.objects.get_or_create(fest=fest, text="Follow the general rules")
		ItemRule.objects.get_or_create(item=item, fest=fest, text="Teams up to 4 members")
		self.stdout.write(self.style.SUCCESS("Bootstrapped demo data"))
