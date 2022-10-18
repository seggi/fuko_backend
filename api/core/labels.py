

class AppLabels:
    languages = ['Fr', 'En']

    @staticmethod
    def label(label: str, selected_language=None, ) -> str:

        if selected_language in AppLabels.languages:
            return
