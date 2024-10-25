class UserDisplayMixin:
    def get_user_name(self, obj):
        """Retorna o first_name do usuário ou username como fallback"""
        # Verifica se o objeto tem acesso direto ao user ou através de person
        if hasattr(obj, 'user'):
            user = obj.user
        elif hasattr(obj, 'person'):
            user = obj.person.user
        else:
            return '-'
        
        return user.first_name + ' ' + user.last_name
    get_user_name.short_description = 'Name'