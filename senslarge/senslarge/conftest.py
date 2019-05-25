from pytest_factoryboy import register

from senslarge.evaluations.factories import (
    FormulaireFactory,
    QuestionFactory,
    CategorieFactory,
    ChoiceFactory,
    UserFactory,
    ChoiceutilisateurFactory,
    TicketFactory
)


register(FormulaireFactory)
register(QuestionFactory)
register(CategorieFactory)
register(ChoiceFactory)
register(UserFactory)
register(ChoiceutilisateurFactory)
register(TicketFactory)
