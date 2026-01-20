from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = set()

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and getattr(u, "actif", True) and u.role in self.allowed_roles
