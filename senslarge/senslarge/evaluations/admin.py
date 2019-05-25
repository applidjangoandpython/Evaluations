from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .models import (
    Question,
    Choice,
    ChoiceUtilisateur,
    Categorie,
    Formulaire,
    TicketFormulaire
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    fields = ['choice_text', 'categorie', 'valorisation']


class QuestionAdmin(OrderedModelAdmin):
    list_display = ('question_text', 'formulaire', 'move_up_down_links')
    inlines = [ChoiceInline]


class ChoiceAdmin(OrderedModelAdmin):
    list_filter = ['question__formulaire', 'question']
    list_display = (
        "choice_text", "question", 'move_up_down_links'
    )
    search_fields = ['choice_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Categorie)
admin.site.register(Formulaire)
admin.site.register(ChoiceUtilisateur)
admin.site.register(TicketFormulaire)
