from store.services import config


class MenuMixin:
    def get_header_context(self, title: str, **kwargs) -> dict:
        context = kwargs
        context['title'] = title
        context['menu'] = config.BASE_MENU

        if self.request.user.is_authenticated:
            context['right_section'] = config.LOGOUT_MENU
        else:
            context['right_section'] = config.LOGIN_MENU

        return context
