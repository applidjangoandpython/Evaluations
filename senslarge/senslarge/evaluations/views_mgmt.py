import pygal

from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.staticfiles.finders import find
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DetailView
from django.db.models import Sum

# from django_weasyprint import WeasyTemplateResponseMixin

from pygal.style import DefaultStyle

from .models import (
    Choice,
    Question,
    Categorie,
    Formulaire,
    TicketFormulaire,
    ChoiceUtilisateur,
    FormUser,
)

from .forms import (
    ChoiceForm,
    ChoiceFormEdit,
    UserForm
)
from .mixins import SuperuserRequired


class Home(SuperuserRequired, TemplateView):
    template_name = 'evaluations/home.html'


class Liste_Formulaire(SuperuserRequired, ListView):
    model = Formulaire
    template_name = 'evaluations/liste_formulaire.html'

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        context['nombre'] = Formulaire.objects.count()
        return context


class Detail_Formulaire(SuperuserRequired, DetailView):
    model = Formulaire
    context_object_name = 'formulaire'
    template_name = 'evaluations/detail_formulaire.html'


class Creation_Formulaire(SuperuserRequired, CreateView):
    model = Formulaire
    context_object_name = 'formulaire'
    template_name = 'evaluations/creation_formulaire.html'
    fields = ['titre', 'introduction', 'type_form', 'typegraphe', 'nb_points']

    def get_success_url(self):
        pk = self.object.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Edition_Formulaire(SuperuserRequired, UpdateView):
    model = Formulaire
    template_name = 'evaluations/edition_formulaire.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Creation_Question(SuperuserRequired, CreateView):
    model = Question
    template_name = 'evaluations/creation_question.html'
    fields = ['question_text']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulaire'] = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.formulaire = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        self.object.save()
        return super(Creation_Question, self).form_valid(form)

    def get_success_url(self):
        pk = self.object.formulaire.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Edition_Question(SuperuserRequired, UpdateView):
    model = Question
    template_name = 'evaluations/edition_question.html'
    fields = ['question_text']

    def get_success_url(self):
        pk = self.object.formulaire.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Creation_Choices(SuperuserRequired, CreateView):
    model = Choice
    form_class = ChoiceForm
    template_name = 'evaluations/creation_choix.html'

    def get_form_kwargs(self):
        context_form = super().get_form_kwargs()
        context_form['my_formulaire'] = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        return context_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(
            pk=self.kwargs['question_pk']
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = Question.objects.get(
            pk=self.kwargs['question_pk']
        )
        self.object.save()
        return super(Creation_Choices, self).form_valid(form)

    def get_success_url(self):
        pk = self.object.question.formulaire.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Edition_Choices(SuperuserRequired, UpdateView):
    model = Choice
    form_class = ChoiceFormEdit
    template_name = 'evaluations/edition_choix.html'
    pk_url_kwarg = 'choice_pk'

    def get_form_kwargs(self):
        context_form = super().get_form_kwargs()
        context_form['formulaire'] = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        return context_form

    def get_success_url(self):
        pk = self.object.question.formulaire.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Creation_Categories(SuperuserRequired, CreateView):
    model = Categorie
    template_name = 'evaluations/creation_categorie.html'
    fields = ['categorie_text']

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        context['formulaire'] = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.formulaire = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        self.object.save()
        return super(Creation_Categories, self).form_valid(form)

    def get_success_url(self):
        pk = self.object.formulaire.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Edition_Categories(SuperuserRequired, UpdateView):
    model = Categorie
    template_name = 'evaluations/edition_categorie.html'
    fields = ['categorie_text']

    def get_success_url(self):
        pk = self.object.formulaire.pk
        return reverse('evaluations:formulaire', kwargs={'pk': pk})


class Liste_Repondant(SuperuserRequired, ListView):
    model = User
    template_name = 'evaluations/listerepondant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulaires'] = Formulaire.objects.all()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_superuser=False)


class Creation_Repondant(SuperuserRequired, CreateView):
    model = User
    template_name = 'evaluations/creation_repondant.html'
    form_class = UserForm
    success_url = reverse_lazy('evaluations:liste_repondant')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.object.email
        self.object.password = self.object.email
        self.object.save()
        ticket = TicketFormulaire.objects.create(
                    users_lien=self.object,
        )
        for formulaire in self.request.POST.getlist('formulaires'):
            ticket.formul.add(formulaire)

        ticket.send_to_user(self.request)

        return super(Creation_Repondant, self).form_valid(form)


class Edition_Repondant(SuperuserRequired, UpdateView):
    model = User
    template_name = 'evaluations/edition_repondant.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('evaluations:liste_repondant')


class BaseDetailRepondant(ListView):
    model = ChoiceUtilisateur
    template_name = 'evaluations/detail_repondant.html'

    def get_formulaire(self):
        return Formulaire.objects.get(pk=self.kwargs['formulaire_pk'])

    def get_categorie_sum(self):
        pk_formulaire = self.kwargs.get('formulaire_pk')
        formulaire = Formulaire.objects.get(pk=pk_formulaire)
        user = User.objects.get(pk=self.kwargs['user_pk'])
        categorie = formulaire.categories.all()
        tab2 = []
        for categ in categorie:
            tab = []
            for question in formulaire.questions.all():
                valeurs = ChoiceUtilisateur.objects.filter(
                    reference_user=user.pk,
                    reference_choice__in=Choice.objects.filter(
                        categorie=categ,
                        question=question
                    )
                ).aggregate(Sum('valeur_entier'))
                value = valeurs['valeur_entier__sum']
                if value:
                    tab.append(value)
            tab2.append(sum(tab))
        val = [tab2[0], tab2[1], tab2[3], tab2[2]]
        return val

    def get_context_data(self, **kwargs):
        formulaire = self.get_formulaire()
        context = super().get_context_data(**kwargs)
        formulaire = Formulaire.objects.get(
            pk=self.kwargs['formulaire_pk']
        )
        user = User.objects.get(
            pk=self.kwargs['user_pk']
        )
        context['formulaire'] = formulaire
        context['utilisateur'] = user
        context['form_user'] = FormUser(formulaire, user)

        context['categorie'] = self.get_categorie_sum()

        return context


class Detail_Repondant(SuperuserRequired, BaseDetailRepondant):
    pass


class Creation_PDF(SuperuserRequired,
                   BaseDetailRepondant):
    pdf_attachment = True
    pdf_stylesheets = [
        find('bootstrap/css/bootstrap.min.css'),
        find('fontawesome/css/font-awesome.min.css'),
    ]

    def get_pdf_filename(self):
        pk_formulaire = self.kwargs.get('formulaire_pk')
        formulaire = Formulaire.objects.get(pk=pk_formulaire)
        user = User.objects.get(pk=self.kwargs['user_pk'])
        return "{} {}.pdf".format(user.email, formulaire.titre)


class GrapheView(TemplateView):
    def get(self, request, *args, **kwargs):
        return self.graphe1()

    def graphe1(self):
        pk_formulaire = self.kwargs.get('formulaire_pk')
        formulaire = Formulaire.objects.get(pk=pk_formulaire)
        user = User.objects.get(pk=self.kwargs['user_pk'])
        categorie = formulaire.categories.all()
        tab2 = []
        for categ in categorie:
            tab = []
            for question in formulaire.questions.all():
                valeurs = ChoiceUtilisateur.objects.filter(
                    reference_user=user.pk,
                    reference_choice__in=Choice.objects.filter(
                        categorie=categ,
                        question=question
                    )
                ).aggregate(Sum('valeur_entier'))
                tab.append(valeurs['valeur_entier__sum'])
            tab2.append(sum(tab))
        val = [tab2[0], tab2[1], tab2[3], tab2[2]]

        style = DefaultStyle(colors=(
            '#AEEE00', '#046380', '#C72B10', '#05966D',
            '#000000', '#000000',
        ))
        axis_max = formulaire.nb_points * formulaire.questions.count()
        chart = pygal.XY(
            width=400,
            height=400,
            print_labels=True,
            print_values=False,
            print_values_position='bottom',
            xrange=(-1 * axis_max, axis_max),
            range=(-1 * axis_max, axis_max),
            fill=True,
            show_dots=False,
            inner_radius=20,
            show_x_labels=False,
            show_y_labels=False,
            show_legend=False,
            style=style,
            margin=0,
        )
        chart.add(
            'Analytique',
            [
                (0, 0),
                (0, -val[0]),
                {'value': (-val[0], -val[0]), 'label': str(val[0])},
                (-val[0], 0),
                (0, 0),
            ],
            dots_size=1
        )
        chart.add(
            'Relationnel individuel',
            [
                (0, 0),
                (0, -val[1]),
                {'value': (val[1], -val[1]), 'label': str(val[1])},
                (val[1], 0),
                (0, 0),
            ],
            dots_size=1
        )
        chart.add(
            'Centré resultat',
            [
                (0, 0),
                (0, val[2]),
                {'value': (-val[2], val[2]), 'label': str(val[2])},
                (-val[2], 0),
                (0, 0),
            ],
            dots_size=1
        )

        chart.add(
            'entraineur de groupe',
            [
                (0, 0),
                (0, val[3]),
                {'value': (val[3], val[3]), 'label': str(val[3])},
                (val[3], 0),
                (0, 0),
            ],
            dots_size=1
        )
        chart.add('', [(-1 * axis_max, 0), (axis_max, 0)], dots_size=0)
        chart.add('', [(0, -1 * axis_max), (0, axis_max)], dots_size=0)

        return HttpResponse(chart.render())


class GrapheView2(TemplateView):
    def get(self, request, *args, **kwargs):
        return self.graphe2()

    def graphe2(self):
        pk_formulaire = self.kwargs.get('formulaire_pk')
        formulaire = Formulaire.objects.get(pk=pk_formulaire)
        user = User.objects.get(pk=self.kwargs['user_pk'])
        categorie = formulaire.categories.all()
        tab2 = []
        for categ in categorie:
            tab = []
            for question in formulaire.questions.all():
                valeurs = ChoiceUtilisateur.objects.filter(
                    reference_user=user.pk,
                    reference_choice__in=Choice.objects.filter(
                        categorie=categ,
                        question=question
                    )
                ).aggregate(Sum('valeur_entier'))
                tab.append(valeurs['valeur_entier__sum'])
            tab2.append(sum(tab))
        val = [tab2[2], tab2[3], tab2[0], tab2[1]]

        style = DefaultStyle(
            colors=('#F44336', '#3F51B5', '#3F51B5', '#009688', '#009688')
        )

        axis_max = formulaire.nb_points * formulaire.questions.count()
        chart = pygal.XY(
            width=400,
            height=400,
            print_labels=True,
            print_values=False,
            xrange=(-1 * axis_max, axis_max),
            range=(-1 * axis_max, axis_max),
            fill=False,
            show_dots=True,
            inner_radius=20,
            show_x_labels=False,
            show_y_labels=False,
            show_legend=False,
            style=style,
            margin=0,
        )

        chart.add(
            '',
            [
                {'value': (-val[0], -val[0]), 'label': str(val[0])},
                {'value': (-val[1], val[1]), 'label': str(val[1])},
                {'value': (val[2], val[2]), 'label': str(val[2])},
                {'value': (val[3], -val[3]), 'label': str(val[3])},
                {'value': (-val[0], -val[0])},
            ],
            stroke_style={'width': 4},
            dots_size=2,
        )
        chart.add(
            '',
            [(-1 * axis_max, 0), (axis_max, 0)],
            show_dots=False,
            stroke_style={'width': 2}
        )
        chart.add(
            '',
            [(0, -1 * axis_max), (0, axis_max)],
            show_dots=False,
            stroke_style={'width': 2}
        )
        chart.add(
            '',
            [(i, i) for i in range(-1 * axis_max, 1 * axis_max, 10)],
            stroke_style={'width': 1},
            dots_size=1,
        )
        chart.add(
            '',
            [(-1 * i, i) for i in range(-1 * axis_max, 1 * axis_max, 10)],
            stroke_style={'width': 1},
            dots_size=1,
        )
        return HttpResponse(chart.render())


class GrapheView3(TemplateView):
    def get(self, request, *args, **kwargs):
        return self.graphe3()

    def graphe3(self):
        pk_formulaire = self.kwargs.get('formulaire_pk')
        formulaire = Formulaire.objects.get(pk=pk_formulaire)
        user = User.objects.get(pk=self.kwargs['user_pk'])
        categorie = formulaire.categories.all()
        tab = []
        tab2 = []
        for categ in categorie:
            for question in formulaire.questions.all():
                valeurs = ChoiceUtilisateur.objects.filter(
                    reference_user=user.pk,
                    reference_choice__in=Choice.objects.filter(
                        categorie=categ,
                        question=question
                    )
                ).aggregate(Sum('valeur_entier'))
                tab.append(valeurs['valeur_entier__sum'])
            tab2.append(sum(tab))
            del tab[:]
        valeurs = [tab2[0], tab2[1], tab2[2], tab2[3], tab2[4]]
        chart = pygal.Bar(
            print_values=True,
            style=DefaultStyle(
                value_font_family='googlefont:Raleway',
                value_font_size=16,
                labels_colors=('black'),
                labels_font_size=16,
            ),
            print_labels=False,
            print_values_position='top',
            show_legend=False,
            pretty_print=True,
            print_zeroes=False,
            margin=0,
            x_labels=[
                'Psychologique', 'Normalisante', 'Magique', 'Rationnelle',
                'Systémique'
            ],
        )

        colors = ('#5EB6DD', '#AEEE00', '#046380', '#C72B10', '#05966D')
        serie = []
        for value, color in zip(valeurs, colors):
            serie.append({'value': value, 'color': color})
        chart.add('', serie)

        return HttpResponse(chart.render())
